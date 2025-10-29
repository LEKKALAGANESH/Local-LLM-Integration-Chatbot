# Recipe Chatbot Frontend

This is the React-based web interface for the Local LLM Recipe Chatbot. It provides a modern chat UI for interacting with the backend API.

## Overview

Features:
- **Chat Interface**: Glassmorphism design with animations
- **Real-time Messaging**: Instant display with typing indicators
- **Responsive**: Works on desktop and mobile
- **Auto-scroll**: Scrolls to latest messages
- **Error Handling**: Shows connection errors gracefully

## Prerequisites

- Node.js 14+
- Backend running on port 8000

## Installation

1. Navigate to frontend:
   ```bash
   cd task2_chatbot/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm start
   ```
   Opens at http://localhost:3000

## Building

```bash
npm run build
```

## Testing

```bash
npm test
```

## Project Structure

```
frontend/
├── public/          # Static assets
├── src/
│   ├── App.js       # Main component
│   ├── App.css      # Styles
│   └── ...          # Other React files
├── package.json     # Dependencies
└── README.md        # This file
```

## Configuration

Backend URL in `src/App.js` (default: http://localhost:8000)

## Troubleshooting

- Ensure backend is running
- Check port 3000 is free
- Clear node_modules if build issues
