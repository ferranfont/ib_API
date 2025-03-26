from flask import Flask, render_template_string
import yfinance as yf
import pandas as pd
import webbrowser
import threading

# Initialize Flask app
app = Flask(__name__)

# HTML template for the page
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>AAPL - Last 30 Days</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h1 { color: #333; }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 8px;
            text-align: center;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #fafafa;
        }
    </style>
</head>
<body>
    <h1>Apple Inc. (AAPL) – Last 30 Days</h1>
    {{ table | safe }}
</body>
</html>
"""

# Route for the main page
@app.route("/")
def index():
    # Fetch data from Yahoo
    ticker = yf.Ticker("AAPL")
    df = ticker.history(period="30d", interval="1d")
    
    # Clean and format
    df = df[["Open", "High", "Low", "Close"]].reset_index()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df = df[["Date", "Open", "High", "Low", "Close"]]

    # Convert to HTML table
    table_html = df.to_html(index=False, classes="data", border=0)
    return render_template_string(HTML_TEMPLATE, table=table_html)

# Function to auto-open the browser
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

# Start the app
if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
