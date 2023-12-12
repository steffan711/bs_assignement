# AI Assistant Application

## Overview

The AI Assistant Application is an interactive, AI-powered interface designed to assist users with their queries over IBM Generative AI Python SDK (Tech Preview) using advanced natural language processing techniques. Built with Python, the application integrates various components such as a repository manager, HTML parser, Pinecone manager for vector storage, and a chat agent to provide a comprehensive AI-driven experience.

### Prerequisites

- Python 3.8 or higher
- langchain
- pinecone
- streamlit
- sphynx (shall be added to PATH to automatically build the documentation)
- packages needed for the build of the documentation

## Configuration

Before running the application, ensure all necessary API keys and configurations are set:

- OpenAI API Key
- Pinecone API Key

Search pine_api_key and openai_api_key in mainUI.py.

## Usage

streamlit run mainUI.py 

## Features

- **Repository Management**: Automates the cloning of git repository and build of documentation.
- **HTML Parsing**: Extracts and processes information from HTML documents.
- **Vector Storage Management**: Utilizes Pinecone for efficient vector storage and retrieval.
- **AI Chat Agent**: Answers user queries by leveraging a sophisticated AI model.
