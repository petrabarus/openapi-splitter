#/usr/bin/env bash
# This script runs test for the samples YAML files.

echo "Cleaning up..."
rm -rfv tmp/output > /dev/null 2>&1
mkdir -p tmp/output > /dev/null 2>&1

# Run the test
echo "Running tests..."
TEST_FILES=$(find res/samples -name "*.yaml" -type f)

for TEST_FILE in $TEST_FILES; do
    echo "Testing $TEST_FILE"
    # Remove .yaml part from file
    # No changes needed here
    OUTPUT_DIR=tmp/output/$(basename $TEST_FILE .yaml)
    mkdir -p $OUTPUT_DIR
    python3 src/openapi_splitter/main.py $TEST_FILE $OUTPUT_DIR
    OUTPUT_FILE=$OUTPUT_DIR.yaml
    swagger-cli bundle -t yaml $OUTPUT_DIR/main.yaml > $OUTPUT_FILE
    swagger-cli validate $OUTPUT_DIR/main.yaml
    swagger-cli validate $OUTPUT_FILE
done
