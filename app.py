import requests
import datetime
import os

import yfinance as yf
from flask import Flask, render_template, request


app = Flask(__name__)

def get_stock_info(symbol):
    try:
        if not symbol or len(symbol.strip()) == 0:
            return {"error": "No symbol provided."}

        stock = yf.Ticker(symbol)

        try:
            info = stock.info
        except Exception:
            return {"error": f"Symbol '{symbol}' not found or not available on Yahoo Finance."}

        if not info or not isinstance(info, dict):
            return {"error": f"Symbol '{symbol}' not found or no data returned."}

        price = info.get("regularMarketPrice")
        previous_close = info.get("previousClose")

        if price is None or previous_close is None:
            return {"error": f"Market data for '{symbol}' not available."}

        change = price - previous_close
        change_percent = (change / previous_close) * 100 if previous_close else 0

        company_name = info.get("longName") or info.get("shortName") or symbol.upper()
        now = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")

        return {
            "datetime": now,
            "company": company_name,
            "symbol": symbol.upper(),
            "price": f"{price:.2f}",
            "change": f"{'+' if change >= 0 else ''}{change:.2f}",
            "percent": f"{change_percent:.2f}%"
        }

    except Exception as e:
        return {"error": f"Something went wrong: {str(e)}"}


@app.route("/", methods=["GET","POST"])
def index():
    stock_data = None
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        stock_data = get_stock_info(symbol)
    
    return render_template("index.html", stock_data=stock_data)

if __name__ == "__main__":
    app.run(debug=True)
# while True:
#     symbol = input("\nPlease enter a symbol: (or \"exit\" to end program)  ")
#     if symbol.lower() == "exit":
#         break
#     get_stock_info(symbol)
