package main

import (
	"fmt"
	"math/rand"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/stretchr/testify/require"
)

func TestReadInputDocumentFromFile(t *testing.T) {

	testcases := []struct {
		inputFile string
		assertErr require.ErrorAssertionFunc
	}{
		{
			inputFile: "res/samples/petstore.yaml",
			assertErr: require.NoError,
		},
		{
			inputFile: "res/samples/api-with-example.yaml",
			assertErr: require.NoError,
		},
		{
			inputFile: "res/samples/petstore-expanded.yaml",
			assertErr: require.NoError,
		},
		{
			inputFile: "res/samples/nonexistent.yaml",
			assertErr: require.Error,
		},
	}

	for _, testcase := range testcases {
		t.Run(testcase.inputFile, func(t *testing.T) {
			document, err := readInputDocumentFromFile(testcase.inputFile)
			testcase.assertErr(t, err)
			if err == nil {
				require.NotNil(t, document)
			}
		})
	}
}
func TestWriteOutputDocumentsToFiles(t *testing.T) {
	testfile := "res/samples/petstore.yaml"
	document, err := readInputDocumentFromFile(testfile)
	require.NoError(t, err)

	// jsonData, err := json.Marshal(document)
	// require.NoError(t, err)
	// fmt.Printf("Document: %s\n", string(jsonData))

	outputDir := fmt.Sprintf("%s/test_%d_%d",
		os.TempDir(),
		time.Now().UnixNano(),
		rand.Int31(),
	)
	err = os.Mkdir(outputDir, 0755)
	require.NoErrorf(t, err, "error creating output directory")

	testcases := []struct {
		name            string
		outputDocuments []*outputDocument
		outputDir       string
		assertErr       require.ErrorAssertionFunc
	}{
		{
			name: "success writing file",
			outputDocuments: []*outputDocument{
				{
					file: "file1.yaml",
					node: document,
				},
				{
					file: "file2.yaml",
					node: document,
				},
			},
			outputDir: outputDir,
			assertErr: require.NoError,
		},
		{
			name: "error writing file",
			outputDocuments: []*outputDocument{
				{
					file: "file1.yaml",
					node: document,
				},
				{
					file: "file2.yaml",
					node: document,
				},
			},
			outputDir: "/nonexistent",
			assertErr: require.Error,
		},
	}

	for _, testcase := range testcases {
		t.Run(testcase.name, func(t *testing.T) {
			err := writeOutputDocumentsToFiles(testcase.outputDocuments, testcase.outputDir)
			testcase.assertErr(t, err)
			if err != nil {
				return
			}

			for _, outputDocument := range testcase.outputDocuments {
				path := filepath.Clean(testcase.outputDir + "/" + outputDocument.file)
				//fmt.Printf("Output document: %s\n", path)
				content, err := os.ReadFile(path)
				require.NoError(t, err)
				require.NotNil(t, content)
				require.True(t, len(content) > 1)
				err = os.Remove(path)
				require.NoError(t, err)
			}
		})
	}
}
