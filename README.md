# Text Analysis System

This project implements a Text Analysis System using LangChain, Cohere, Pinecone, and Gradio. It allows users to upload various types of documents (PDF, CSV, Excel, TXT, MD, JSON) and ask questions about their content using natural language.

## Features

- Supports multiple file formats: PDF, CSV, Excel, TXT, MD, JSON
- Uses Cohere for embeddings and language model
- Stores document vectors in Pinecone for efficient retrieval
- Provides a user-friendly interface with Gradio
- Automatically resets when a new file is uploaded

## Demo

Try out the Text Analysis System in Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/your-repo-name/blob/main/text_analysis_system.ipynb)

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Install the required packages:
   ```
   pip install langchain-cohere langchain langchain-core sentence-transformers pinecone-client==2.2.4 gradio pypdf
   ```

3. Set up your API keys:
   - Get a Cohere API key from [Cohere](https://cohere.ai/)
   - Get a Pinecone API key from [Pinecone](https://www.pinecone.io/)

4. Update the `cohere_api_key` and `pinecone_api_key` variables in the script with your API keys.

## Usage

1. Run the script:
   ```
   python text_analysis_system.py
   ```

2. Open the provided Gradio interface URL in your web browser.

3. Upload a supported file (PDF, CSV, Excel, TXT, MD, or JSON).

4. Enter your question about the file's content in the text box.

5. Click "Submit" to get the AI's response and the retrieved document text.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
