package summarizer

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath" // ESENCIAL: Necesario para la resolución de rutas en el futuro
	"strings"
	"time" // Añadir time para el timeout del HTTP client
	// Importar godotenv
)

// Default model to use if not overridden
const DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct:together"              // <-- DEFAULT_MODEL actualizado con :together
const HF_API_URL = "https://router.huggingface.co/v1/chat/completions" // <-- URL DE LA API ACTUALIZADA

// LoadArticle loads the text from a file.
// It uses a default article path if no path is provided.
func LoadArticle(path string) (string, error) {
	var filePath string
	if path != "" {
		filePath = path
	} else {
		// Attempt to load default path from environment variable
		envFilePath := os.Getenv("ARTICLE_PATH")
		if envFilePath != "" {
			filePath = envFilePath
			fmt.Printf("[summarizer] No file provided → using default from ARTICLE_PATH: %s\n", filePath)
		} else {
			// Fallback to hardcoded default if env var is not set, assuming CLI is run from c04_summarizer
			filePath = filepath.Join("articles", "article.txt")
			fmt.Printf("[summarizer] No input or ARTICLE_PATH provided → defaulting to: %s\n", filePath)
		}
	}

	// Check if file exists
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		return "", fmt.Errorf("ERROR: File not found → %s", filePath)
	}

	fmt.Printf("[summarizer] Loading article from: %s\n", filePath)
	content, err := os.ReadFile(filePath)
	if err != nil {
		return "", fmt.Errorf("failed to read file %s: %w", filePath, err)
	}

	return string(content), nil
}

// SummarizeText performs the summarization using Hugging Face Inference API.
// It handles token validation, model selection, prompt engineering, API call,
// response parsing, and metrics calculation.
func SummarizeText(
	articleContent string,
	summaryType string,
	cliModel string,
	cliToken string,
	httpClient *http.Client, // Add this parameter
) (string, error) {
	// Cargar variables de entorno desde .env en la raíz del proyecto

	// --- Token validation ---
	token := cliToken
	if token == "" {
		return "", fmt.Errorf(
			"\n❌ ERROR: No HF_API_TOKEN detected.\n\n" +
				"Please set it before continuing:\n" +
				"    setx HF_API_TOKEN \"your_token_here\"   (Windows)\n" +
				"    export HF_API_TOKEN=\"your_token_here\" (Linux/Mac)\n\n" +
				"Obtain your token at: https://huggingface.co/settings/tokens",
		)
	}

	// --- Model selection ---
	model := cliModel
	if model == "" {
		model = os.Getenv("HF_MODEL")
	}
	if model == "" {
		model = DEFAULT_MODEL // Ahora DEFAULT_MODEL ya incluye ":together"
	}
	fmt.Printf("[HF] Using model: %s\n", model)

	// --- System prompts ---
	systemPrompts := map[string]string{
		"short":  "You create very concise summaries (1–2 sentences).",
		"medium": "You create paragraph-length summaries.",
		"bullet": "You create bullet-point summaries using dashes (-).",
	}

	// --- User prompts ---
	userPrompts := map[string]string{
		"short":  fmt.Sprintf("Summarize in 1–2 sentences:\n\n%s", articleContent),
		"medium": fmt.Sprintf("Summarize this text into one paragraph:\n\n%s", articleContent),
		"bullet": fmt.Sprintf("Summarize this text into bullet points using dashes (-):\n\n%s", articleContent),
	}

	systemPrompt := systemPrompts[summaryType]
	userPrompt := userPrompts[summaryType]

	// --- API Request Structure ---
	requestBody := map[string]interface{}{
		"model": model, // <-- Ahora el 'model' ya debe incluir el sufijo ":together"
		"messages": []map[string]string{
			{"role": "system", "content": systemPrompt},
			{"role": "user", "content": userPrompt},
		},
		"parameters": map[string]interface{}{
			"max_new_tokens": 300,
			"temperature":    0.0,
		},
	}
	jsonBody, err := json.Marshal(requestBody)
	if err != nil {
		return "", fmt.Errorf("failed to marshal request body: %w", err)
	}

	// --- Make HTTP Request ---
	client := httpClient // Use the provided client
	if client == nil {
		client = &http.Client{Timeout: 30 * time.Second} // Create a default client if none is provided
	} // Add a timeout for robustness
	req, err := http.NewRequest("POST", HF_API_URL, bytes.NewBuffer(jsonBody)) // <-- URL sin el nombre del modelo
	if err != nil {
		return "", fmt.Errorf("failed to create API request: %w", err)
	}
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")

	fmt.Println("[HF] Sending summarization request to Hugging Face API...")

	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("API request failed: %w", err)
	}
	defer resp.Body.Close()

	// 1. LEER UNA SOLA VEZ
	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read response body: %w", err)
	}

	// 2. VALIDAR STATUS (Usando los bytes ya leídos)
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("API error (%d): %s", resp.StatusCode, string(bodyBytes))
	}

	// --- Parse API Response ---
	var apiResponse map[string]interface{} // La respuesta de OpenAI es un objeto, no un array
	err = json.Unmarshal(bodyBytes, &apiResponse)
	if err != nil {
		return "", fmt.Errorf("failed to unmarshal API response: %w", err)
	}

	// Parseo de la respuesta de OpenAI-like API
	choices, ok := apiResponse["choices"].([]interface{})
	if !ok || len(choices) == 0 {
		return "", fmt.Errorf("API response did not contain choices")
	}

	firstChoice, ok := choices[0].(map[string]interface{})
	if !ok {
		return "", fmt.Errorf("API response did not contain a valid first choice")
	}

	message, ok := firstChoice["message"].(map[string]interface{})
	if !ok {
		return "", fmt.Errorf("API response did not contain a valid message in first choice")
	}

	summary, ok := message["content"].(string)
	if !ok {
		return "", fmt.Errorf("API response did not contain content in message")
	}

	summary = strings.TrimSpace(summary) // Trim leading/trailing whitespace

	// The Qwen model might include the instruction in the response, let's try to remove it
	// Example: <s>[INST] Summarize in 1-2 sentences: ... [/INST] Summary Text
	// We need to find the last [/INST] and take the part after it.
	if idx := strings.LastIndex(summary, "[/INST]"); idx != -1 {
		summary = summary[idx+len("[/INST]"):]
		summary = strings.TrimSpace(summary)
	}

	// --- Format bullets if requested ---
	if summaryType == "bullet" {
		summary = FormatBullets(summary)
	}

	// --- Metrics calculation ---
	originalChars := len(articleContent)
	summaryChars := len(summary)
	reduction := 0
	if originalChars > 0 {
		reduction = 100 - int((float64(summaryChars)/float64(originalChars))*100)
	}

	metricsMsg := fmt.Sprintf(
		"\n\n--- SUMMARY METRICS ---\n"+
			"Type           : %s\n"+
			"Original length: %d chars\n"+
			"Summary length : %d chars\n"+
			"Reduced        : %d%%\n",
		summaryType,
		originalChars,
		summaryChars,
		reduction,
	)

	return summary + metricsMsg, nil
}

// FormatBullets ensures each line is formatted as a bullet point prefixed with '- '.
func FormatBullets(text string) string {
	lines := []string{}
	for _, line := range strings.Split(text, "\n") {
		trimmedLine := strings.TrimSpace(line)
		trimmedLine = strings.TrimPrefix(trimmedLine, "• ") // Remove existing bullet point if it's '• '

		if trimmedLine != "" {
			if !strings.HasPrefix(trimmedLine, "- ") { // Only add if it doesn't already have "- "
				lines = append(lines, "- "+trimmedLine)
			} else {
				lines = append(lines, trimmedLine) // Keep existing "- " if it's already there
			}
		}
	}
	return strings.Join(lines, "\n")
}
