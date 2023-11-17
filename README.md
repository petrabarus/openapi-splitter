# OpenAPI Splitter

This is a command line to split a single large OpenAPI3 file into multiple files.

Usually when a team started to use OpenAPI, they started with a single YAML file. With the grow of the requirements, this YAML file soon will grow into thousands or ten of thousands of lines. This will give challenge to them to manage, maintain, and collaborate on the OpenAPI specification effectively. This tool addresses this challenge by providing a straightforward solution to break down a monolithic OpenAPI3 file into smaller, more manageable pieces.

## 1. Usage

### 1.1. Requirements

TBD

### 1.2. Installation

To install this, you can clone the code and run `make dist`. You can find the executable `openapi-splitter` in the `dist` directory.

```bash
make dist
```

### 1.3. Usage

Once installed, you can use the tool with the following command:

```bash
openapi-splitter -i api.yaml -o split_output
```

Replace the `input.yaml` with your large OpenAPI3 file and replace the `split_output` with empty directory where the tool will output the splitted files.

## 2. Development

TBD

## 3. Contributing

If you find any issues or have suggestions for improvements, please feel free to contribute! Create an issue, fork the repository, make your changes, and submit a pull request. Your feedback and contributions are highly appreciated.

## 4. License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](/LICENSE) file for details.

## 5. Acknowledgments

Special thanks to the OpenAPI community for their continuous support and feedback.

---

Happy API documentation splitting!
