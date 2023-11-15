package main

import (
	"fmt"
	"math/rand"
	"os"
	"testing"
	"time"

	"github.com/stretchr/testify/require"
)

func TestGetValidInputs(t *testing.T) {

	// GIVEN
	inputFileHandler, err := os.CreateTemp("", "test_*.yaml")
	require.NoErrorf(t, err, "error creating input file")
	defer inputFileHandler.Close()
	inputFile := inputFileHandler.Name()

	outputDir := fmt.Sprintf("%s/test_%d_%d",
		os.TempDir(),
		time.Now().UnixNano(),
		rand.Int31(),
	)
	err = os.Mkdir(outputDir, 0755)
	require.NoErrorf(t, err, "error creating output directory")

	defer os.RemoveAll(inputFile)
	defer os.RemoveAll(outputDir)

	testcases := []struct {
		name      string
		args      []string
		setupFunc func()
		assertErr require.ErrorAssertionFunc
	}{
		{
			name:      "valid inputs",
			args:      []string{"-i", inputFile, "-o", outputDir},
			assertErr: require.NoError,
		},
		{
			name:      "missing all flags",
			args:      []string{},
			assertErr: require.Error,
		},
		{
			name:      "missing input file",
			args:      []string{"-o", outputDir},
			assertErr: require.Error,
		},
		{
			name:      "missing output directory",
			args:      []string{"-i", inputFile},
			assertErr: require.Error,
		},
		{
			name:      "non-existent input file",
			args:      []string{"-i", "nonexistent.yaml", "-o", outputDir},
			assertErr: require.Error,
		},
		{
			name:      "non-existent output directory",
			args:      []string{"-i", inputFile, "-o", "nonexistent"},
			assertErr: require.Error,
		},
		{
			name:      "non-directory output directory",
			args:      []string{"-i", inputFile, "-o", inputFile},
			assertErr: require.Error,
		},
		{
			name:      "non-writable output directory",
			args:      []string{"-i", inputFile, "-o", "/root"},
			assertErr: require.Error,
		},
		{
			name: "non-empty output directory",
			args: []string{"-i", inputFile, "-o", outputDir},
			setupFunc: func() {
				err = os.WriteFile(outputDir+"/file.txt", []byte("test"), 0644)
				require.NoErrorf(t, err, "error creating file in output directory")
			},
			assertErr: require.Error,
		},
	}

	for _, testcase := range testcases {
		t.Run(testcase.name, func(t *testing.T) {
			// GIVEN
			if testcase.setupFunc != nil {
				testcase.setupFunc()
			}

			// WHEN
			_, _, err := getValidInputs(testcase.args)

			// THEN
			testcase.assertErr(t, err)
		})
	}
}
