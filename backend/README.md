# Task 2: Local LLM Recipe Chatbot Backend

This is the FastAPI-based backend for the Local LLM Recipe Chatbot. It provides RESTful endpoints for recipe suggestions and general chat interactions using local LLM integration via Ollama.

## Overview

The backend features:
- **Recipe Matching**: Fuzzy similarity search on a JSON recipe dataset
- **LLM Integration**: Uses Ollama's Mistral model for recipe generation
- **Dual Endpoints**: Separate endpoints for detailed recipes and unified chat
- **CORS Support**: Enabled for frontend integration
- **Error Handling**: Graceful fallbacks when LLM is unavailable

## Prerequisites

- Python 3.8+
- Ollama CLI installed
- Ollama Mistral model: `ollama pull mistral`

## Installation

1. Navigate to the backend directory:
   ```bash
   cd task2_chatbot/backend
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start Ollama server:
   ```bash
   ollama serve
   ```

5. Run the server:
   ```bash
   uvicorn app:app --reload
   ```
   API available at http://localhost:8000

## API Endpoints

### POST /get_recipe
Returns detailed recipe information based on ingredients.

**Request:**
```json
{
  "ingredients": "egg, onion, tomato"
}
```

**Response:**
```json
{
  "best_cuisine": "greek",
  "matched_ingredients": ["egg", "onion", "tomato"],
  "similarity_score": 87,
  "llm_recipe": "Full recipe description..."
}
```

### POST /chat
Unified endpoint for recipes and general chat.

**Request:**
```json
{
  "query": "egg, onion"  // or "Hello"
}
```

**Response:**
```json
{
  "response": "Recipe suggestion or chat reply..."
}
```

## Testing

Use curl or Postman:

```bash
# Recipe request
curl -X POST http://localhost:8000/get_recipe \
  -H "Content-Type: application/json" \
  -d '{"ingredients": "egg, onion"}'

# Chat request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello"}'
```

## Configuration

- **Model**: Change in Ollama calls (default: mistral)
- **Similarity Threshold**: Adjustable in `find_best_match()`
- **Ports**: Default 8000, configurable in uvicorn command

## Troubleshooting

- Ensure Ollama is running for LLM features
- Check ports are free
- Verify train.json is present
