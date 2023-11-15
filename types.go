package main

import "gopkg.in/yaml.v3"

type outputDocument struct {
	file string
	node *yaml.Node
}
