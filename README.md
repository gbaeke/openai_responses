# OpenAI API Responses Examples

This repository contains examples of using the OpenAI API's new Responses feature, which provides a more streamlined way to interact with OpenAI's models.

## Setup

1. Make sure you have Python installed
2. Install the required packages:
   ```
   pip install openai rich pydantic
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Examples

### 1. Basics (`1_basics.py`)

This script demonstrates the basic usage of the OpenAI Responses API:
- Creating simple responses with instructions
- Using the traditional messages array format
- Maintaining conversation context with `previous_response_id`
- Converting responses to dictionaries for inspection

### 2. Interactive Chat (`2_chat.py`)

A command-line chat interface built with the Rich library:
- Maintains conversation context across multiple exchanges
- Streams responses for a more interactive experience
- Displays token usage statistics
- Supports exiting the chat with the 'exit' command

### 3. Image Analysis (`3_images.py`)

Shows how to use the API to analyze images:
- Sends an image URL to the model
- Requests a description of the image content
- Uses the gpt-4o-mini model for efficient image analysis

### 4. Structured Outputs (`4_structured_outputs.py`)

Demonstrates how to get structured data from the API:
- Uses JSON Schema to define the expected output format
- Extracts structured information from natural language
- Shows integration with Pydantic for type validation
- Compares different methods for structured output

### 5. Web Search Integration (`5_built_in_web_search.py`)

Showcases the built-in web search capability:
- Configures the web search tool with user location
- Extracts and displays search results with annotations
- Uses Rich library to format and display the results in a visually appealing way
- Demonstrates how to parse the complex response structure

## Usage

Run any example with Python:

```
python 1_basics.py
```

For the interactive chat example:

```
python 2_chat.py
```

## Notes

- These examples use the latest OpenAI API features as of February 2025
- The Responses API provides a more streamlined interface compared to the older Chat Completions API
- The older Chat Completions API is still available and is still supported