package summarizer_test

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"testing"

	. "DataSecChallenge/challenges/c04_summarizer/summarizer"
)

// MockRoundTripper es una implementación mock de http.RoundTripper para pruebas unitarias.
type MockRoundTripper struct {
	Handler func(*http.Request) (*http.Response, error)
}

// RoundTrip implementa la interfaz http.RoundTripper.
func (m *MockRoundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
	return m.Handler(req)
}

// TestLoadArticle_DefaultPath tests if LoadArticle loads the default article correctly.
func TestLoadArticle_DefaultPath(t *testing.T) {
	// Create a dummy article.txt for testing in a temporary directory
	tempDir := t.TempDir()
	articlesDir := filepath.Join(tempDir, "articles")
	err := os.MkdirAll(articlesDir, os.ModePerm)
	if err != nil {
		t.Fatalf("Failed to create temporary articles directory: %v", err)
	}
	testArticlePath := filepath.Join(articlesDir, "article.txt")
	expectedContent := "This is a test article for summarization."
	err = os.WriteFile(testArticlePath, []byte(expectedContent), 0644)
	if err != nil {
		t.Fatalf("Failed to create test article file: %v", err)
	}

	// Temporarily change the current working directory to the tempDir
	// to simulate the root of the CLI application for LoadArticle
	originalCwd, err := os.Getwd()
	if err != nil {
		t.Fatalf("Failed to get original working directory: %v", err)
	}
	defer os.Chdir(originalCwd) // Restore original working directory

	err = os.Chdir(tempDir)
	if err != nil {
		t.Fatalf("Failed to change directory to temporary directory: %v", err)
	}

	content, err := LoadArticle("") // Use default path, which should now resolve to articles/article.txt in tempDir
	if err != nil {
		t.Errorf("LoadArticle failed with default path: %v", err)
	}
	if !strings.Contains(content, expectedContent) {
		t.Errorf("LoadArticle with default path returned unexpected content. Got: %s, Want to contain: %s", content, expectedContent)
	}
}

// TestLoadArticle_SpecificPath tests if LoadArticle loads a specific article correctly.
func TestLoadArticle_SpecificPath(t *testing.T) {
	// Create a dummy article.txt for testing
	testArticlePath := "test_specific_article.txt"
	expectedContent := "This is a specific test article."
	err := os.WriteFile(testArticlePath, []byte(expectedContent), 0644)
	if err != nil {
		t.Fatalf("Failed to create test article file: %v", err)
	}
	defer os.Remove(testArticlePath) // Clean up after test

	content, err := LoadArticle(testArticlePath)
	if err != nil {
		t.Errorf("LoadArticle failed with specific path: %v", err)
	}
	if content != expectedContent {
		t.Errorf("LoadArticle with specific path returned unexpected content. Got: %s, Want: %s", content, expectedContent)
	}
}

// TestLoadArticle_NotFound tests if LoadArticle handles a non-existent file.
func TestLoadArticle_NotFound(t *testing.T) {
	_, err := LoadArticle("non_existent_file.txt")
	if err == nil {
		t.Errorf("LoadArticle did not return an error for a non-existent file.")
	}
	if !strings.Contains(err.Error(), "ERROR: File not found") {
		t.Errorf("LoadArticle returned unexpected error for non-existent file. Got: %s", err.Error())
	}
}

// TestFormatBullets tests the FormatBullets function.
func TestFormatBullets(t *testing.T) {
	testCases := []struct {
		input    string
		expected string
	}{
		{"- item 1\n- item 2", "- item 1\n- item 2"},
		{"item 1\nitem 2", "- item 1\n- item 2"},
		{"• item 1\n• item 2", "- item 1\n- item 2"},
		{"  item 1 with leading space\nitem 2", "- item 1 with leading space\n- item 2"},
		{"", ""},
		{"single line", "- single line"},
	}

	for i, tc := range testCases {
		t.Run(fmt.Sprintf("Case %d", i), func(t *testing.T) {
			result := FormatBullets(tc.input)
			if result != tc.expected {
				t.Errorf("For input:\n'%s'\nExpected:\n'%s'\nGot:\n'%s'", tc.input, tc.expected, result)
			}
		})
	}
}

// TestSummarizeText_NoToken tests if SummarizeText returns an error when no token is provided.
func TestSummarizeText_NoToken(t *testing.T) {
	// Clear any existing token to ensure the test fails without one
	os.Setenv("HF_API_TOKEN", "")
	defer os.Unsetenv("HF_API_TOKEN")

	// Pass nil for httpClient to use the default client logic, which will check for the token
	_, err := SummarizeText("some content", "short", "", "", nil)
	if err == nil {
		t.Errorf("SummarizeText did not return an error for missing token.")
	}
	if !strings.Contains(err.Error(), "❌ ERROR: No HF_API_TOKEN detected") {
		t.Errorf("SummarizeText returned unexpected error for missing token. Got: %s", err.Error())
	}
}

// TestSummarizeText_MockAPI tests SummarizeText with a mocked HTTP client.
func TestSummarizeText_MockAPI(t *testing.T) {
	// Setup a dummy token for the test, as the function requires one.
	os.Setenv("HF_API_TOKEN", "fake-token")
	defer os.Unsetenv("HF_API_TOKEN")

	// Define test cases for different summary types and expected mock responses
	testCases := []struct {
		name              string
		summaryType       string
		mockContent       string
		expectedInSummary string
		expectedReduction int // Expected reduction percentage, approximate for testing
	}{
		{
			name:              "Short Summary",
			summaryType:       "short",
			mockContent:       "This is a short mocked summary.",
			expectedInSummary: "This is a short mocked summary.",
			expectedReduction: 40, // Assuming original content length for calculation
		},
		{
			name:              "Medium Summary",
			summaryType:       "medium",
			mockContent:       "This is a medium mocked summary, providing a bit more detail about the original content.",
			expectedInSummary: "This is a medium mocked summary, providing a bit more detail about the original content.",
			expectedReduction: 20,
		},
		{
			name:              "Bullet Summary",
			summaryType:       "bullet",
			mockContent:       "• Mocked bullet one\n• Mocked bullet two", // Escapar el salto de línea para JSON
			expectedInSummary: "- Mocked bullet one\n- Mocked bullet two",
			expectedReduction: 30,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			mockRoundTripper := &MockRoundTripper{
				Handler: func(req *http.Request) (*http.Response, error) {
					// Optionally, inspect the request body and headers here
					body, _ := io.ReadAll(req.Body)
					_ = body // Suppress unused warning

					// Escapar el contenido del mock para que sea JSON válido
					jsonSafeContent := strings.ReplaceAll(tc.mockContent, "\n", "\\n")
					mockResponseJSON := fmt.Sprintf(`{"choices":[{"message":{"content":"%s"}}]}`, jsonSafeContent)
					return &http.Response{
						StatusCode: http.StatusOK,
						Body:       io.NopCloser(bytes.NewBufferString(mockResponseJSON)),
						Header:     make(http.Header),
					}, nil
				},
			}
			mockClient := &http.Client{Transport: mockRoundTripper}

			articleContent := "This is a much longer article content that will be summarized by the mocked API. It contains various details that should be condensed into different summary types: short, medium, and bullet points. The original content is quite extensive to ensure that the summarization process has enough text to work with for calculating metrics."

			summaryResult, err := SummarizeText(articleContent, tc.summaryType, "", "fake-token", mockClient)
			if err != nil {
				t.Fatalf("SummarizeText failed for %s: %v", tc.summaryType, err)
			}
			// Check if the expected summary content is present
			if !strings.Contains(summaryResult, tc.expectedInSummary) {
				t.Errorf("Expected summary for %s to contain '%s', but got: %s", tc.summaryType, tc.expectedInSummary, summaryResult)
			}

			// Check if metrics are present
			if !strings.Contains(summaryResult, "--- SUMMARY METRICS ---") {
				t.Errorf("Summary for %s did not contain metrics section.", tc.summaryType)
			}

			// Approximate check for reduction percentage (due to varying mocked content lengths)
			originalChars := len(articleContent)
			summaryLines := strings.Split(summaryResult, "\n")
			summaryContentEnd := len(summaryLines) - 6 // Assuming 6 lines for metrics at the end
			actualSummaryContent := strings.Join(summaryLines[:summaryContentEnd], "\n")
			actualSummaryChars := len(strings.TrimSpace(actualSummaryContent))

			if originalChars > 0 {
				actualReduction := 100 - int((float64(actualSummaryChars)/float64(originalChars))*100)
				// Allow for a small deviation in reduction percentage due to string trimming,
				// metric formatting and potential differences in line endings.
				if actualReduction < tc.expectedReduction-5 || actualReduction > tc.expectedReduction+5 {
					t.Logf("Warning: Actual reduction for %s (%d%%) is outside expected range (%d%% +/- 5%%). Original chars: %d, Actual Summary chars: %d", tc.summaryType, actualReduction, tc.expectedReduction, originalChars, actualSummaryChars)
				}
			}
		})
	}
}
