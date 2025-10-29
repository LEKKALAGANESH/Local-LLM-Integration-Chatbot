# Task 2: Local LLM Recipe Chatbot

This project implements a comprehensive recipe suggestion chatbot with both backend API and web interface. The system uses local large language model integration via Ollama and provides intelligent recipe recommendations based on user-provided ingredients.

## Overview

The chatbot combines:
- **Ingredient-based recipe matching** using fuzzy string similarity on a curated recipe dataset
- **Local LLM integration** for generating detailed recipe instructions
- **Conversational AI** for general queries and greetings
- **Modern web interface** with responsive design

## Features

- **Smart Ingredient Detection**: Automatically identifies ingredient queries vs. general conversation
- **Recipe Database**: Pre-trained on diverse culinary dataset with cuisine classification
- **Local LLM**: Uses Ollama's Mistral model for recipe generation (runs entirely offline)
- **Fallback Responses**: Graceful handling when LLM is unavailable
- **Web Interface**: Modern chat UI resembling popular messaging applications
- **API-First Design**: RESTful API for easy integration

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Node.js 14+ (for frontend)
- Ollama CLI installed

### Model Requirements
- Ollama Mistral model: `ollama pull mistral`

## Installation and Setup

### Backend Setup

1. Navigate to the task2_chatbot directory:
   ```bash
   cd task2_chatbot
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install and configure Ollama:
   ```bash
   # Download Ollama from https://ollama.ai/
   ollama pull mistral
   ollama serve  # Start Ollama server in background
   ```

5. Start the backend server:
   ```bash
   python app.py
   ```
   The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```
   The interface will be available at http://localhost:3000

## Usage

### Web Interface
1. Ensure both backend (port 8000) and frontend (port 3000) are running
2. Open http://localhost:3000 in your browser
3. Enter ingredients (e.g., "egg, onion") for recipe suggestions
4. Ask general questions for conversational responses

### API Usage
Send POST requests to `http://localhost:8000/chat` with JSON payload:
```json
{
  "query": "egg, onion"
}
```

## Sample Interactions

### Recipe Query
**Input:** "egg, onion"  
**Output:** "Try making Egg Curry. Ingredients: Eggs, onions, tomatoes, spices. Instructions: Sauté onions, add tomatoes and spices, crack eggs into the mixture and cook until done."

### General Conversation
**Input:** "Hello"  
**Output:** "Hello! How can I help you today? Try entering some ingredients for recipe suggestions!"

## API Endpoints

### POST /chat
Main endpoint for chatbot interactions.

**Request Body:**
```json
{
  "query": "string"  // User input (ingredients or general query)
}
```

**Response:**
```json
{
  "response": "string"  // Chatbot response
}
```

## Testing

### Backend API Tests (using curl)

1. **Recipe Suggestion**:
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "egg, onion"}'
   ```

2. **General Query**:
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "Hello"}'
   ```

### Frontend Tests
- Load http://localhost:3000 and verify interface renders
- Test ingredient queries and general conversation
- Verify responsive design on different screen sizes

## Architecture

- **Backend**: FastAPI server with CORS enabled
- **Recipe Matching**: Fuzzy similarity search on JSON dataset
- **LLM Integration**: Ollama for local model inference
- **Frontend**: React with modern CSS (glassmorphism effects)
- **Data**: Recipe dataset with ingredients and cuisine classification

## Configuration

- **Similarity Threshold**: Configurable in `find_best_match()` function
- **LLM Model**: Change model name in Ollama calls (default: mistral)
- **Ports**: Backend (8000), Frontend (3000) - configurable in respective code

## Troubleshooting

- **LLM Errors**: Ensure Ollama is running (`ollama serve`)
- **Connection Issues**: Verify ports are available and services are started
- **Frontend Not Loading**: Check Node.js version and npm install completion

## Notes

- All processing occurs locally - no external API calls required
- Recipe suggestions improve with better ingredient matching
- LLM provides creative recipe variations based on cuisine inspiration
- System gracefully degrades when LLM is unavailable
