package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	inputFile, outputDir, err := getValidInputs(os.Args[1:])
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		flag.Usage()
		os.Exit(1)
	}

	fmt.Printf("Input file: %s\n", inputFile)
	fmt.Printf("Output directory: %s\n", outputDir)
}
