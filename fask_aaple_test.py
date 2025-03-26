from flask import Flask, render_template_string
import yfinance as yf
import pandas as pd
import webbrowser
import threading

app = Flask(__name__)

# HTML Template with Tailwind CSS for a clean look
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AAPL Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-800">
    <div class="max-w-6xl mx-auto p-6">
        <h1 class="text-3xl font-bold mb-4">Apple Inc. (AAPL) – Last 30 Days</h1>
        <div class="overflow-x-auto">
            <table class="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
                <thead>
                    <tr>
                        {% for col in columns %}
                        <th class="px-6 py-3 border-b-2 text-left text-sm font-semibold text-gray-600">{{ col }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for row in rows %}
                    <tr class="hover:bg-gray-50">
                        {% for item in row %}
                        <td class="px-6 py-3 border-b text-sm">{{ item }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    ticker = yf.Ticker("AAPL")
    df = ticker.history(period="30d", interval="1d")
    df = df[["Open", "High", "Low", "Close"]].reset_index()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df = df[["Date", "Open", "High", "Low", "Close"]]

    columns = df.columns.tolist()
    rows = df.values.tolist()

    return render_template_string(HTML_TEMPLATE, columns=columns, rows=rows)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)