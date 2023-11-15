.PHONY: clean test

all: dist/openapi-splitter


dist/openapi-splitter: $(wildcard *.go)
	mkdir -p dist
	go build -o dist/openapi-splitter .

clean:
	rm -rfv dist/ tmp/ build/

test:
	go test -short -coverprofile coverage.out -v ./...
