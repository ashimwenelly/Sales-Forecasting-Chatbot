"""
Sales Forecasting Chatbot Backend using FastAPI
Provides API endpoints for the chatbot UI to interact with the forecasting model
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
from datetime import datetime
import re
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

from sales_forecasting import load_sales_data, build_monthly_series, create_forecast_report


app = FastAPI(title="Sales Forecasting Chatbot")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatMessage(BaseModel):
    user_message: str


class ChatResponse(BaseModel):
    response: str
    data: dict = None


# Global state for chatbot
conversation_history = []
forecast_data = None


def generate_forecast(months: int = 12):
    """Generate forecast data"""
    global forecast_data
    csv_path = Path('stores_sales_forecasting.csv')
    
    if not csv_path.exists():
        raise FileNotFoundError(f"Data file not found: {csv_path}")
    
    df = load_sales_data(csv_path)
    monthly = build_monthly_series(df)
    forecast = create_forecast_report(monthly, months)
    
    forecast_data = {
        'monthly': monthly,
        'forecast': forecast,
        'months': months,
        'generated_at': datetime.now().isoformat()
    }
    
    return forecast_data


def extract_months_from_message(message: str) -> int:
    """Extract number of months from user message"""
    numbers = re.findall(r'\d+', message)
    if numbers:
        return min(int(numbers[0]), 36)  # Max 36 months
    return 12


def format_forecast_table(forecast_df: pd.DataFrame) -> str:
    """Format forecast dataframe as HTML table"""
    html = "<table border='1' cellpadding='5' style='border-collapse: collapse;'>"
    html += "<tr><th>Month</th><th>Sales Forecast</th><th>Quantity Forecast</th></tr>"
    
    for idx, row in forecast_df.head(12).iterrows():
        month = idx.strftime('%Y-%m')
        sales = f"${row['Sales Forecast']:,.2f}"
        quantity = f"{row['Quantity Forecast']:,.0f}"
        html += f"<tr><td>{month}</td><td>{sales}</td><td>{quantity}</td></tr>"
    
    html += "</table>"
    return html


def generate_forecast_chart(forecast_df: pd.DataFrame) -> str:
    """Generate interactive forecast chart and return as base64 embedded image"""
    try:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.patch.set_facecolor('#ffffff')
        
        # Sales Forecast Chart
        dates = [d.strftime('%Y-%m') for d in forecast_df.index]
        sales = forecast_df['Sales Forecast'].values
        
        ax1.plot(dates, sales, marker='o', linewidth=2, markersize=6, color='#4a90e2', label='Sales Forecast')
        ax1.fill_between(range(len(dates)), sales, alpha=0.3, color='#4a90e2')
        ax1.set_title('Monthly Sales Forecast', fontsize=14, fontweight='bold', pad=15)
        ax1.set_ylabel('Sales ($)', fontsize=11)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.set_xticklabels(dates, rotation=45, ha='right')
        for i, (d, v) in enumerate(zip(dates, sales)):
            ax1.text(i, v + max(sales)*0.02, f'${v:,.0f}', ha='center', fontsize=9)
        
        # Quantity Forecast Chart
        quantity = forecast_df['Quantity Forecast'].values
        
        ax2.plot(dates, quantity, marker='s', linewidth=2, markersize=6, color='#f39c12', label='Quantity Forecast')
        ax2.fill_between(range(len(dates)), quantity, alpha=0.3, color='#f39c12')
        ax2.set_title('Monthly Quantity Forecast', fontsize=14, fontweight='bold', pad=15)
        ax2.set_xlabel('Month', fontsize=11)
        ax2.set_ylabel('Quantity (units)', fontsize=11)
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.set_xticklabels(dates, rotation=45, ha='right')
        for i, (d, v) in enumerate(zip(dates, quantity)):
            ax2.text(i, v + max(quantity)*0.02, f'{v:,.0f}', ha='center', fontsize=9)
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return f'<img src="data:image/png;base64,{image_base64}" style="width: 100%; max-width: 900px; height: auto; border-radius: 8px; margin: 15px 0;">'
    except Exception as e:
        return f"<p style='color: red;'>Error generating chart: {str(e)}</p>"


def generate_historical_chart(monthly_df: pd.DataFrame) -> str:
    """Generate historical data chart and return as base64 embedded image"""
    try:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.patch.set_facecolor('#ffffff')
        
        # Historical Sales Chart
        dates = [d.strftime('%Y-%m') for d in monthly_df.index]
        sales = monthly_df['Sales'].values
        
        ax1.plot(dates, sales, marker='o', linewidth=2, markersize=5, color='#27ae60', label='Historical Sales')
        ax1.fill_between(range(len(dates)), sales, alpha=0.3, color='#27ae60')
        ax1.set_title('Historical Monthly Sales', fontsize=14, fontweight='bold', pad=15)
        ax1.set_ylabel('Sales ($)', fontsize=11)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.tick_params(axis='x', rotation=45)
        
        # Historical Quantity Chart
        quantity = monthly_df['Quantity'].values
        
        ax2.plot(dates, quantity, marker='s', linewidth=2, markersize=5, color='#e74c3c', label='Historical Quantity')
        ax2.fill_between(range(len(dates)), quantity, alpha=0.3, color='#e74c3c')
        ax2.set_title('Historical Monthly Quantity', fontsize=14, fontweight='bold', pad=15)
        ax2.set_xlabel('Month', fontsize=11)
        ax2.set_ylabel('Quantity (units)', fontsize=11)
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return f'<img src="data:image/png;base64,{image_base64}" style="width: 100%; max-width: 900px; height: auto; border-radius: 8px; margin: 15px 0;">'
    except Exception as e:
        return f"<p style='color: red;'>Error generating chart: {str(e)}</p>"


def generate_comparison_chart(monthly_df: pd.DataFrame, forecast_df: pd.DataFrame) -> str:
    """Generate comparison chart (historical + forecast) and return as base64 embedded image"""
    try:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9))
        fig.patch.set_facecolor('#ffffff')
        
        # Sales Comparison
        historical_dates = [d.strftime('%Y-%m') for d in monthly_df.index]
        forecast_dates = [d.strftime('%Y-%m') for d in forecast_df.index]
        all_dates = list(historical_dates) + list(forecast_dates)
        
        hist_sales = monthly_df['Sales'].values
        fore_sales = forecast_df['Sales Forecast'].values
        
        x_hist = range(len(historical_dates))
        x_fore = range(len(historical_dates) - 1, len(all_dates))
        
        ax1.plot(x_hist, hist_sales, marker='o', linewidth=2.5, markersize=6, color='#27ae60', label='Historical Sales')
        ax1.plot(x_fore, fore_sales, marker='x', linewidth=2.5, markersize=8, color='#e74c3c', linestyle='--', label='Forecasted Sales')
        ax1.axvline(x=len(historical_dates)-1, color='gray', linestyle=':', alpha=0.5, linewidth=2)
        ax1.text(len(historical_dates)-1, ax1.get_ylim()[1]*0.95, 'Forecast Start', ha='center', fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax1.set_title('Sales: Historical vs Forecast Comparison', fontsize=14, fontweight='bold', pad=15)
        ax1.set_ylabel('Sales ($)', fontsize=11)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.legend(loc='upper left', fontsize=10)
        
        # Quantity Comparison
        hist_qty = monthly_df['Quantity'].values
        fore_qty = forecast_df['Quantity Forecast'].values
        
        ax2.plot(x_hist, hist_qty, marker='o', linewidth=2.5, markersize=6, color='#3498db', label='Historical Quantity')
        ax2.plot(x_fore, fore_qty, marker='x', linewidth=2.5, markersize=8, color='#f39c12', linestyle='--', label='Forecasted Quantity')
        ax2.axvline(x=len(historical_dates)-1, color='gray', linestyle=':', alpha=0.5, linewidth=2)
        ax2.set_title('Quantity: Historical vs Forecast Comparison', fontsize=14, fontweight='bold', pad=15)
        ax2.set_xlabel('Period', fontsize=11)
        ax2.set_ylabel('Quantity (units)', fontsize=11)
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.legend(loc='upper left', fontsize=10)
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return f'<img src="data:image/png;base64,{image_base64}" style="width: 100%; max-width: 900px; height: auto; border-radius: 8px; margin: 15px 0;">'
    except Exception as e:
        return f"<p style='color: red;'>Error generating chart: {str(e)}</p>"


def process_user_message(message: str) -> tuple:
    """Process user message and generate appropriate response with charts"""
    message_lower = message.lower()
    
    # Greeting
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return ("Hello! 👋 I'm your Sales Forecasting AI Chatbot. I can help you:\n"
                "• Generate sales forecasts with charts\n"
                "• View forecast data\n"
                "• Analyze trends\n"
                "\nTry asking: 'Generate a 12-month forecast' or 'Show me the forecast'", None)
    
    # Forecast generation requests
    if any(word in message_lower for word in ['forecast', 'predict', 'generate', 'create']):
        months = extract_months_from_message(message)
        try:
            generate_forecast(months)
            forecast_table = format_forecast_table(forecast_data['forecast'])
            forecast_chart = generate_forecast_chart(forecast_data['forecast'])
            response = f"✅ Forecast generated for the next {months} months!\n\n{forecast_chart}\n\n{forecast_table}"
            return (response, None)
        except Exception as e:
            return (f"❌ Error generating forecast: {str(e)}", None)
    
    # Show existing forecast
    if any(word in message_lower for word in ['show', 'display', 'view', 'see']) and 'forecast' in message_lower:
        if forecast_data:
            forecast_table = format_forecast_table(forecast_data['forecast'])
            forecast_chart = generate_forecast_chart(forecast_data['forecast'])
            response = f"Here's your forecast data:\n\n{forecast_chart}\n\n{forecast_table}"
            return (response, None)
        else:
            return ("No forecast data available. Try generating one first: 'Generate a 12-month forecast'", None)
    
    # Historical data with charts
    if any(word in message_lower for word in ['history', 'historical', 'trend', 'past']) and any(w in message_lower for w in ['chart', 'graph', 'visualize']):
        try:
            csv_path = Path('stores_sales_forecasting.csv')
            df = load_sales_data(csv_path)
            monthly = build_monthly_series(df)
            historical_chart = generate_historical_chart(monthly)
            response = f"📊 Historical Sales Trends:\n\n{historical_chart}"
            return (response, None)
        except Exception as e:
            return (f"❌ Error generating historical chart: {str(e)}", None)
    
    # Comparison chart
    if any(word in message_lower for word in ['compare', 'comparison', 'versus', 'vs']) or (any(word in message_lower for word in ['historical', 'history']) and 'forecast' in message_lower):
        try:
            if not forecast_data:
                generate_forecast(12)
            csv_path = Path('stores_sales_forecasting.csv')
            df = load_sales_data(csv_path)
            monthly = build_monthly_series(df)
            comparison_chart = generate_comparison_chart(monthly, forecast_data['forecast'])
            response = f"📊 Historical vs Forecast Comparison:\n\n{comparison_chart}"
            return (response, None)
        except Exception as e:
            return (f"❌ Error generating comparison chart: {str(e)}", None)
    
    # Statistics with chart
    if 'statistics' in message_lower or 'stats' in message_lower or 'summary' in message_lower:
        try:
            csv_path = Path('stores_sales_forecasting.csv')
            df = load_sales_data(csv_path)
            stats = {
                'total_records': len(df),
                'total_sales': df['Sales'].sum(),
                'avg_sales': df['Sales'].mean(),
                'total_quantity': df['Quantity'].sum(),
                'date_range': f"{df['Order Date'].min().date()} to {df['Order Date'].max().date()}"
            }
            response = (f"📊 Sales Data Statistics:\n"
                       f"• Total Records: {stats['total_records']:,}\n"
                       f"• Total Sales: ${stats['total_sales']:,.2f}\n"
                       f"• Average Sale: ${stats['avg_sales']:,.2f}\n"
                       f"• Total Quantity: {stats['total_quantity']:,.0f}\n"
                       f"• Date Range: {stats['date_range']}")
            
            # Generate historical chart for context
            monthly = build_monthly_series(df)
            historical_chart = generate_historical_chart(monthly)
            return (response + f"\n\n{historical_chart}", None)
        except Exception as e:
            return (f"❌ Error retrieving statistics: {str(e)}", None)
    
    # Help
    if any(word in message_lower for word in ['help', '?', 'what can', 'commands']):
        return ("🤖 I can help you with:\n"
                "1. **Forecast with Chart**: 'Generate a 12-month forecast'\n"
                "2. **View Forecast Data**: 'Show me the forecast'\n"
                "3. **Historical Trends**: 'Show historical chart'\n"
                "4. **Compare Data**: 'Compare historical vs forecast'\n"
                "5. **Statistics**: 'Show me statistics'\n"
                "6. **Help**: Just ask 'Help' for this menu", None)
    
    # Default response
    return ("I didn't quite understand. Try asking:\n"
            "• 'Generate a forecast'\n"
            "• 'Show me the forecast'\n"
            "• 'Show historical chart'\n"
            "• 'Statistics'\n"
            "• 'Help'", None)


@app.post("/api/chat")
async def chat(message: ChatMessage):
    """Chat endpoint - processes user message and returns response"""
    try:
        user_msg = message.user_message.strip()
        
        if not user_msg:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Add to conversation history
        conversation_history.append({"user": user_msg, "timestamp": datetime.now().isoformat()})
        
        # Generate response
        response_text, _ = process_user_message(user_msg)
        
        return ChatResponse(response=response_text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/forecast")
async def get_forecast(months: int = 12):
    """Get forecast data endpoint"""
    try:
        if not forecast_data or forecast_data['months'] != months:
            generate_forecast(months)
        
        return {
            "status": "success",
            "forecast": forecast_data['forecast'].to_dict(orient='index'),
            "months": months,
            "generated_at": forecast_data['generated_at']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/statistics")
async def get_statistics():
    """Get data statistics endpoint"""
    try:
        csv_path = Path('stores_sales_forecasting.csv')
        df = load_sales_data(csv_path)
        
        return {
            "total_records": int(len(df)),
            "total_sales": float(df['Sales'].sum()),
            "average_sales": float(df['Sales'].mean()),
            "total_quantity": float(df['Quantity'].sum()),
            "date_range": {
                "start": df['Order Date'].min().isoformat(),
                "end": df['Order Date'].max().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def get_conversation_history():
    """Get conversation history endpoint"""
    return {"history": conversation_history}


@app.post("/api/clear")
async def clear_history():
    """Clear conversation history endpoint"""
    global conversation_history
    conversation_history = []
    return {"status": "success", "message": "Conversation history cleared"}


@app.get("/health")
async def health():
    """Lightweight check that the API server is running."""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Open the chatbot UI (avoids blank JSON at localhost:8000)."""
    return RedirectResponse(url="/static/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
