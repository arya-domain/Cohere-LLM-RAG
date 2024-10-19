# Cohere RAG Based Chat [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1qqqcmUYEFahgWubBc7k3xsXsQ2WJN3xb?usp=sharing)

This project implements a Text Analysis System using LangChain, Cohere, Pinecone, and Gradio. It allows users to upload various types of documents (PDF, CSV, Excel, TXT, MD, JSON) and ask questions about their content using natural language.

## Features

- Supports multiple file formats: PDF, CSV, Excel, TXT, MD, JSON
- Uses Cohere for embeddings and language model
- Stores document vectors in Pinecone for efficient retrieval
- Provides a user-friendly interface with Gradio
- Automatically resets when a new file is uploaded

## Get Free APIs

- Get a Cohere API key from [Cohere](https://cohere.ai/)
- Get a Pinecone API key from [Pinecone](https://www.pinecone.io/)

## Run the Code in Colab

Try out the Text Analysis System in Google Colab: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1qqqcmUYEFahgWubBc7k3xsXsQ2WJN3xb?usp=sharing)

_Note_: Update the `Cohere_api` and `Pinecone_api` variables in the `Script` with your API keys [Ref [Get Free APIs](#get-free-apis)].

## Run from Docker Image

1. Download the Docker image from [Google Drive](https://drive.google.com/file/d/1-1ic3N-TJJeLDepEvOPQye6EKEQoshB8/) directly, or using [gdown](https://github.com/wkentaro/gdown):

   ```bash
   gdown 1-1ic3N-TJJeLDepEvOPQye6EKEQoshB8
   ```

2. Load the Docker image:

   ```bash
   docker load -i ./hosting_image.tar
   ```

3. Run the Docker container:

   ```bash
   docker run -d -p 7860:7860 --name hosting_container hosting
   ```

## Installation for Local Setup

To run this project locally, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/arya-domain/Cohere-LLM-RAG.git
   cd Cohere-LLM-RAG
   ```

2. Install the required packages:

   ```
   pip install langchain-cohere langchain langchain-core sentence-transformers pinecone-client==2.2.4 gradio pypdf python-dotenv
   ```

3. Set up your API keys:

   - Get a Cohere API key from [Cohere](https://cohere.ai/)
   - Get a Pinecone API key from [Pinecone](https://www.pinecone.io/)

4. Update the `Cohere_api` and `Pinecone_api` variables in the `.env` with your API keys [Ref [Get Free APIs](#get-free-apis)].
5. Run the script:

   ```
   python main.py
   ```

6. In the Terminal you will get the Public and Localhost Links.

## Docker to Create Image From Docker File

1. Clone the repository:

   ```
   git clone https://github.com/arya-domain/Cohere-LLM-RAG.git
   ```

2. Navigate to the project directory:

   ```
   cd Cohere-LLM-RAG
   ```

3. Build the Docker image from the `Dockerfile`:

   ```
   cd hositng docker build -t hosting .
   ```

   ```
   docker run -d -p 7860:7860 --name hosting_container hosting
   ```

4. Open your browser and navigate to `http://localhost:7860` to access the app.

## Usage

1. Open the provided Gradio interface URL in your web browser.
2. Upload a supported file (PDF, CSV, Excel, TXT, MD, or JSON).
3. Enter your question about the file's content in the text box.
4. Click "Submit" to get the AI's response and the retrieved document text.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
