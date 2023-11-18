
# nlrest

## Description

`nlrest` is a Python Command Line Interface (CLI) tool that allows users to convert natural language descriptions into REST API queries and execute them. It uses OpenAI's GPT-3.5 Turbo model to interpret natural language and generate the details of the REST API call, including the method, URL, headers, and request body.

## Installation

### Prerequisites

- Python 3.6 or higher
- An OpenAI API key

### Install from PyPI

You can install `nlrest` directly from PyPI:

```bash
pip install nlrest
```

### Set Up Environment Variable

Before using `nlrest`, set the `OPENAI_API_KEY` environment variable with your OpenAI API key:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

### Basic Usage

To use `nlrest`, run the command followed by the `-p` option and your natural language prompt:

```bash
nlrest -p "Your natural language instruction here"
```

Example:

```bash
nlrest -p "Fetch the latest news from NewsAPI"
```

The tool will output the response from the executed REST API call.

### Example Prompts

- "Fetch the latest stock prices from the Finance API."
- "Post a new message to my social media account saying 'Hello World!'."

## Features

- Converts natural language to REST API query details.
- Supports various HTTP methods (GET, POST, PUT, DELETE).
- Executes the REST API requests and displays the response.

## Contributing

Contributions to `nlrest` are welcome! Please feel free to submit pull requests or open issues to improve the tool or add new features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
