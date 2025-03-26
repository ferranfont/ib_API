from flask import Flask, render_template_string
import yfinance as yf
import pandas as pd
import webbrowser
import threading

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>AAPL - Notebook Style</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 30px; background-color: #f5f5f5; }
        h1 { font-size: 28px; color: #333; }
        .df-table { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <h1>AAPL – Last 30 Days (Jupyter Style)</h1>
    <div class="df-table">
        {{ table | safe }}
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    # Get data
    ticker = yf.Ticker("AAPL")
    df = ticker.history(period="30d", interval="1d")
    df = df[["Open", "High", "Low", "Close"]].reset_index()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df = df[["Date", "Open", "High", "Low", "Close"]]

    # Style it like Jupyter
    styled_table = df.style.set_table_attributes("border='1' class='dataframe'").hide(axis="index").to_html()

    return render_template_string(HTML_TEMPLATE, table=styled_table)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
