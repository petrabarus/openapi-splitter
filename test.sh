#/usr/bin/env bash
# This script runs test for the samples YAML files.

rm -rfv tmp/output > /dev/null 2>&1
mkdir -p tmp/output > /dev/null 2>&1

# Run the test
TEST_FILES=$(find res/samples -name "*.yaml" -type f)

for TEST_FILE in $TEST_FILES; do
    echo "Testing $TEST_FILE"
    # Remove .yaml part from file
    # No changes needed here
    OUTPUT_DIR=tmp/output/$(basename $TEST_FILE .yaml)
    mkdir -p $OUTPUT_DIR
    go run . -i $TEST_FILE -o $OUTPUT_DIR
    #swagger-cli validate $OUTPUT_DIR/main.yaml
done
