package main

import (
	"fmt"
)

func generate(inputFile string, outputDir string) (err error) {
	document, err := readInputDocumentFromFile(inputFile)
	if err != nil {
		err = fmt.Errorf("error reading document from file: %v", err)
		return
	}
	outputDocuments := make([]*outputDocument, 0)
	fmt.Printf("Document: %v\n", document)

	err = writeOutputDocumentsToFiles(outputDocuments, outputDir)
	if err != nil {
		err = fmt.Errorf("error writing output documents to files: %v", err)
		return
	}

	return
}
