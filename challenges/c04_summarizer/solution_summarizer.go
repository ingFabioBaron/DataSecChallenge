package main

import (
	"fmt"
	"os"

	"DataSecChallenge/challenges/c04_summarizer/summarizer" // Import our summarizer package

	"github.com/spf13/cobra"

	"github.com/joho/godotenv" // Importar godotenv
)

// GoLang version used: 1.25.5

const envFile = ".env"

var (
	inputFile   string
	summaryType string
	model       string
	apiToken    string
)

var rootCmd = &cobra.Command{
	Use:   "summarize",
	Short: "CLI for text summarization using Hugging Face GenAI",
	Long: `A command-line application that summarizes the contents of a text file using a free, public GenAI API (HuggingFace Inference API).
Requirements:
The CLI must be written in Go.
The CLI must accept:
  --input or a positional argument: path to the text file to summarize.
  --type or -t : summary type, one of short, medium, or bullet.
The CLI must call a free, public GenAI API for summarization (e.g., HuggingFace Inference API).
The prompt sent to the API should be engineered to match the summary type:
  short : a concise summary (1-2 sentences)
  medium : a paragraph summary
  bullet : a list of bullet points
The CLI should output the summary to stdout.
The CLI should handle API errors gracefully and print user-friendly messages.
Document the Go version used in your code comments.`,
	Run: func(cmd *cobra.Command, args []string) {
		if summaryType == "" {
			fmt.Println("Error: --type is required (short, medium, bullet)")
			os.Exit(1)
		}

		// Handle default input file if not provided as flag, check positional args
		if inputFile == "" && len(args) > 0 {
			inputFile = args[0]
		}

		if inputFile == "" {
			fmt.Println("[CLI] No input provided → defaulting to article.txt")
			// Note: The LoadArticle function handles the full path for the default article.
		}

		// Load article content
		articleContent, err := summarizer.LoadArticle(inputFile)
		if err != nil {
			fmt.Printf("Error loading article: %v\n", err)
			os.Exit(1)
		}

		finalToken := apiToken
		if finalToken == "" {
			finalToken = os.Getenv("HF_API_TOKEN")
		}

		// Perform summarization
		summaryResult, err := summarizer.SummarizeText(articleContent, summaryType, model, finalToken, nil)
		if err != nil {
			fmt.Printf("Error during summarization: %v\n", err)
			os.Exit(1)
		}

		// Output result
		fmt.Println("\n=== SUMMARY RESULT ===")
		fmt.Println(summaryResult)
	},
}

func init() {
	rootCmd.PersistentFlags().StringVarP(&inputFile, "input", "i", "", "Path to the article file.")
	rootCmd.PersistentFlags().StringVarP(&summaryType, "type", "t", "", "Type of summary to generate (short, medium, bullet).")
	rootCmd.PersistentFlags().StringVarP(&model, "model", "m", "", "Hugging Face model override (optional).")
	rootCmd.PersistentFlags().StringVar(&apiToken, "api-token", "", "Hugging Face API token override (optional).")
}

func main() {
	/* Como este programa es un CLI, se ejecuta desde el directorio raiz
	 * del proyecto, se carga el archivo .env desde el directorio raiz.
	 * este es el valor si se corre desde dentro del directorio "c04-summarizer"
	 *antes _ = godotenv.Load("../../.env")
	 */
	// Intentamos cargar el .env
	err := godotenv.Load(envFile)

	// Si hay un error, verificamos si es porque el archivo no existe
	if err != nil {
		// Imprimimos un mensaje amigable pero informativo
		fmt.Println("💡 [INFO] No se encontró el archivo .env. Se usarán las variables de entorno del sistema.")
		fmt.Println("   (Si necesitas configurar HF_API_TOKEN, crea un archivo .env en la raíz")
		fmt.Println("   usa .env.exmaple como referencia)")
		fmt.Println("-----------------------------------------------------------------------")
	}

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
