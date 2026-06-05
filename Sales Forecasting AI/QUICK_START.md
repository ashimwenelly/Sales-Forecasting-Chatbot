# 🚀 Quick Start Guide - Sales Forecasting AI Chatbot

## Installation & Setup (One-time)

### Option 1: Using PowerShell (Recommended)
```powershell
# Navigate to the project directory
cd "path\to\Sales Forecasting AI"

# Run the startup script
.\run_chatbot.ps1
```

### Option 2: Using Batch File (Windows)
```cmd
# Navigate to the project directory
cd "path\to\Sales Forecasting AI"

# Run the startup script
run_chatbot.bat
```

### Option 3: Manual Setup
```powershell
# Install dependencies
python -m pip install -r requirements.txt

# Start the server
python -m uvicorn chatbot_backend:app --reload --host 0.0.0.0 --port 8000
```

---

## 🌐 Access the Chatbot

Once the server is running, open your browser and go to:
```
http://localhost:8000/static/index.html
```

---

## 💬 Example Conversations

### Example 1: Generate a Forecast
```
You: Generate a 12-month forecast
Bot: ✅ Forecast generated for the next 12 months!
     [Displays table with monthly sales and quantity forecasts]
```

### Example 2: View Statistics
```
You: Show me statistics
Bot: 📊 Sales Data Statistics:
     • Total Records: 500
     • Total Sales: $125,450.00
     • Average Sale: $250.90
     • Total Quantity: 2,500
     • Date Range: 2022-01-01 to 2024-12-31
```

### Example 3: Different Forecast Duration
```
You: Forecast the next 6 months
Bot: ✅ Forecast generated for the next 6 months!
     [Displays table with 6 months of predictions]
```

### Example 4: View Forecast
```
You: Show me the forecast
Bot: Here's your forecast data:
     [Displays current forecast table]
```

---

## 🎮 UI Controls

### Main Chat Area
- **Message Input**: Type your message and press Enter or click Send
- **Quick Commands**: Sidebar buttons for common tasks
- **Loading Indicator**: Shows when processing requests

### Header Buttons
- **📈 Stats**: View data statistics in a modal
- **🗑️ Clear**: Clear chat history

### Sidebar Quick Commands
- 📅 12-Month Forecast
- 📅 6-Month Forecast
- 👁️ View Forecast
- 📊 Statistics
- ❓ Help

---

## ✅ Chatbot Capabilities

### Forecasting
- ✓ Generate forecasts for 1-36 months
- ✓ Specify custom month ranges (e.g., "24-month forecast")
- ✓ View formatted forecast tables

### Data Analysis
- ✓ Display sales statistics
- ✓ Show data date ranges
- ✓ Calculate totals and averages

### User Assistance
- ✓ Help menu with command guide
- ✓ Natural language understanding
- ✓ Context-aware responses

---

## 🔧 Troubleshooting

### Issue: "Cannot GET /static/index.html"
**Solution**: Make sure you're accessing the correct URL:
```
http://localhost:8000/static/index.html
```

### Issue: "Connection refused" or "Connection timed out"
**Solution**: Ensure the server is running:
1. Check the terminal shows "Uvicorn running on http://0.0.0.0:8000"
2. If port 8000 is busy, run on a different port:
   ```
   python -m uvicorn chatbot_backend:app --reload --host 0.0.0.0 --port 8001
   ```
   Then access: `http://localhost:8001/static/index.html`

### Issue: "Module not found" errors
**Solution**: Reinstall dependencies:
```powershell
python -m pip install -r requirements.txt --upgrade
```

### Issue: Data file not found
**Solution**: Ensure `stores_sales_forecasting.csv` is in the same directory as `chatbot_backend.py`

---

## 📊 Sample Commands to Try

1. **"Hello"** - Friendly greeting and options
2. **"Generate a forecast"** - Default 12-month forecast
3. **"Create a 3-month forecast"** - Specific duration
4. **"Show statistics"** - Data overview
5. **"Help"** - Command guide
6. **"Display forecast"** - View current forecast
7. **"Show me data statistics"** - Another way to request stats

---

## 🛑 Stopping the Server

Press `CTRL+C` in the terminal/PowerShell where the server is running.

---

## 📱 Mobile Access

To access the chatbot from other devices on your network:

1. Find your computer's IP address:
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. From another device, navigate to:
   ```
   http://192.168.1.100:8000/static/index.html
   ```

---

## 🎨 UI Features

- **Dark Theme**: Modern, easy-on-the-eyes color scheme
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Chat**: Messages appear instantly
- **Table Formatting**: Forecast data displayed in easy-to-read tables
- **Loading Indicators**: Visual feedback during processing
- **Modal Statistics**: Pop-up window for detailed statistics

---

## 📝 File Structure

```
static/
├── index.html       ← Main chatbot UI
├── style.css        ← Styling and layout
└── script.js        ← Chat logic and API calls
```

---

## 🔌 API Endpoints (Advanced)

If you want to integrate the chatbot API with external applications:

```
POST   http://localhost:8000/api/chat           - Send message
GET    http://localhost:8000/api/forecast       - Get forecast data
GET    http://localhost:8000/api/statistics     - Get statistics
GET    http://localhost:8000/api/history        - Get chat history
POST   http://localhost:8000/api/clear          - Clear history
```

---

## 💡 Tips

- Use quick command buttons for instant access to common tasks
- Type partial messages and the chatbot will try to understand your intent
- Forecasts are cached, so generating the same duration is instant
- The sidebar info box provides helpful tips

Enjoy using your Sales Forecasting AI Chatbot! 🎉
