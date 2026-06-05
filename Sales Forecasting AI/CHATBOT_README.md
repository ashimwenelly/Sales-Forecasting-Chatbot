# Sales Forecasting AI Chatbot

A web-based chatbot interface for interacting with the sales forecasting model. Users can generate forecasts, view statistics, and analyze sales data through a conversational interface.

## Features

- 💬 **Interactive Chat Interface** - Natural language conversation with the forecasting AI
- 📊 **Sales Forecasting** - Generate 1-36 month forecasts with a simple command
- 📈 **Statistics Dashboard** - View comprehensive data statistics
- 🎨 **Modern UI** - Beautiful, responsive web interface with dark theme
- ⚡ **Real-time Processing** - Fast forecast generation powered by FastAPI
- 📱 **Mobile Responsive** - Works on desktop, tablet, and mobile devices

## Quick Start

### 1. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 2. Run the Backend Server

```powershell
python -m uvicorn chatbot_backend:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
Uvicorn running on http://0.0.0.0:8000
Press CTRL+C to quit
```

### 3. Open the Chatbot UI

Open your browser and navigate to:
```
http://localhost:8000/static/index.html
```

Or simply access:
```
http://localhost:8000
```

## Usage Examples

### Generate a Forecast
- "Generate a 12-month forecast"
- "Create a 6-month forecast"
- "Forecast the next 24 months"

### View Data
- "Show me the forecast"
- "Display the forecast data"
- "View the forecast"

### Get Statistics
- "Show statistics"
- "Display statistics"
- "Show me data statistics"

### Get Help
- "Help"
- "What can you do?"
- "Commands"

## API Endpoints

The chatbot backend provides the following REST API endpoints:

### Chat
**POST** `/api/chat`
- Send a message to the chatbot
- Request body: `{ "user_message": "your message" }`
- Response: `{ "response": "chatbot response" }`

### Forecast
**GET** `/api/forecast?months=12`
- Get forecast data for specified number of months
- Query params: `months` (1-36, default: 12)
- Response: Forecast data with sales and quantity forecasts

### Statistics
**GET** `/api/statistics`
- Get statistics about the sales data
- Response: Total records, sales, quantity, date range, etc.

### Conversation History
**GET** `/api/history`
- Get all messages in current conversation
- Response: Array of conversation history

### Clear History
**POST** `/api/clear`
- Clear conversation history
- Response: `{ "status": "success" }`

## Project Structure

```
Sales Forecasting AI/
├── sales_forecasting.py          # Original forecasting script
├── chatbot_backend.py            # FastAPI backend for chatbot
├── static/
│   ├── index.html               # Chatbot UI
│   ├── style.css                # Styling
│   └── script.js                # Frontend logic
├── stores_sales_forecasting.csv  # Input data
├── forecast_results.csv          # Forecast output
├── forecast_plots/              # Generated charts
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## How It Works

1. **Frontend (HTML/CSS/JavaScript)**
   - User types a message in the chat interface
   - JavaScript sends the message to the backend API
   - Response is displayed in the chat

2. **Backend (FastAPI)**
   - Receives user message
   - Parses message using natural language patterns
   - Executes appropriate action (forecast generation, statistics, etc.)
   - Returns formatted response

3. **Forecasting Engine**
   - Uses the existing `sales_forecasting.py` module
   - Applies ExponentialSmoothing from statsmodels
   - Generates time-series predictions for sales and quantity

## Chatbot Commands

The chatbot understands natural language and responds to various commands:

| Intent | Example | Result |
|--------|---------|--------|
| Forecast | "Generate a 12-month forecast" | Creates forecast for 12 months |
| View Data | "Show me the forecast" | Displays forecast in table format |
| Statistics | "Show statistics" | Displays data overview |
| Help | "Help" or "?" | Shows available commands |
| Greeting | "Hello" | Friendly greeting with options |

## Tips

💡 **Forecast Months**: You can specify any number of months (1-36) in your request:
- "3-month forecast"
- "Generate a 24-month forecast"
- "Predict the next 18 months"

💡 **Quick Commands**: Use the sidebar buttons for quick access to common tasks

💡 **Statistics**: Click the "📈 Stats" button anytime to view data statistics

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, run on a different port:
```powershell
python -m uvicorn chatbot_backend:app --reload --host 0.0.0.0 --port 8001
```

### Data File Not Found
Ensure `stores_sales_forecasting.csv` is in the same directory as `chatbot_backend.py`

### CORS Errors
The backend is configured to accept requests from any origin. If you still see CORS errors, ensure:
1. Backend is running on `localhost:8000`
2. Frontend is accessing the correct API URL
3. Check browser console for specific error messages

### Import Errors
If you get import errors, make sure all dependencies are installed:
```powershell
python -m pip install -r requirements.txt --upgrade
```

## Performance Notes

- Initial forecast generation may take a few seconds
- Forecasts are cached and reused for the same month duration
- Clearing chat history doesn't affect forecast cache
- Statistics are computed on-demand from the source data

## Future Enhancements

Potential features to add:
- User authentication and session management
- Save/export conversation history
- Custom date range forecasting
- Comparison between different forecast periods
- Chart visualization in the chat
- Batch forecast requests
- Advanced natural language understanding (NLP)

## License

This project extends the original sales forecasting script with a web-based chatbot interface.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the chatbot responses for hints
3. Check the browser console (F12) for JavaScript errors
4. Check the terminal output for backend errors
