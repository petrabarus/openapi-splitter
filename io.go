package main

import (
	"fmt"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

func readInputDocumentFromFile(file string) (document *yaml.Node, err error) {
	file = filepath.Clean(file)
	data, err := os.ReadFile(file)
	if err != nil {
		err = fmt.Errorf("error reading file: %v", err)
		return
	}

	var node yaml.Node
	err = yaml.Unmarshal(data, &node)
	document = &node
	if err != nil {
		err = fmt.Errorf("error unmarshalling yaml: %v", err)
		return
	}
	return
}

func writeOutputDocumentsToFiles(outputDocuments []*outputDocument, outputDir string) (err error) {
	for _, outputDocument := range outputDocuments {
		err = writeOutputDocumentToFile(outputDocument, outputDir)
		if err != nil {
			err = fmt.Errorf("error writing output document %s to file: %v", outputDocument.file, err)
			return
		}
	}
	return
}

func writeOutputDocumentToFile(outputDocument *outputDocument, outputDir string) (err error) {
	file := filepath.Clean(outputDir + "/" + outputDocument.file)
	data, err := yaml.Marshal(outputDocument.node)
	if err != nil {
		err = fmt.Errorf("error marshalling yaml: %v", err)
		return
	}

	err = os.WriteFile(file, data, 0600)
	if err != nil {
		err = fmt.Errorf("error writing file: %v", err)
		return
	}

	return
}
