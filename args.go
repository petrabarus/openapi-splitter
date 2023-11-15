package main

import (
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
)

func getValidInputs(args []string) (inputFile string, outputDir string, err error) {
	flags := flag.NewFlagSet("openapi-splitter", flag.ContinueOnError)

	flags.StringVar(&inputFile, "i", "", "Input YAML file")
	flags.StringVar(&outputDir, "o", "", "Output directory")

	err = flags.Parse(args)
	if err != nil {
		err = fmt.Errorf("error parsing flags: %v", err)
		return
	}

	if inputFile == "" {
		err = fmt.Errorf("input file is required")
		return
	}

	if outputDir == "" {
		err = fmt.Errorf("output directory is required")
		return
	}

	if _, err = os.Stat(inputFile); os.IsNotExist(err) {
		err = fmt.Errorf("input file does not exist")
		return
	}

	if _, err = os.Stat(outputDir); os.IsNotExist(err) {
		err = fmt.Errorf("output directory does not exist")
		return
	}

	if !isDirectory(outputDir) {
		err = fmt.Errorf("output directory is not a directory")
		return
	}

	if !isWritable(outputDir) {
		err = fmt.Errorf("output directory is not writable")
		return
	}

	empty, err := isEmptyDirectory(outputDir)
	if err != nil {
		err = fmt.Errorf("error checking if output directory is empty: %v", err)
		return
	}
	if !empty {
		err = fmt.Errorf("output directory is not empty")
		return
	}

	return
}

func isDirectory(path string) bool {
	fileInfo, err := os.Stat(path)
	if err != nil {
		return false
	}
	return fileInfo.IsDir()
}

func isWritable(path string) bool {
	fileInfo, err := os.Stat(path)
	if err != nil {
		return false
	}
	return fileInfo.Mode().Perm()&(1<<(uint(7))) != 0
}

func isEmptyDirectory(path string) (bool, error) {
	fileInfo, err := os.Stat(path)
	if err != nil {
		return false, err
	}

	if !fileInfo.IsDir() {
		return false, fmt.Errorf("%s is not a directory", path)
	}

	path = filepath.Clean(path)
	dir, err := os.Open(path)
	if err != nil {
		return false, err
	}
	defer dir.Close()

	_, err = dir.Readdir(1)
	if err == io.EOF {
		return true, nil
	}
	if err != nil {
		return false, err
	}

	return false, nil
}
