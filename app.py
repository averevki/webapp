#!/usr/bin/env python3
"""PA053 HW3 - xverevk 555098"""
import requests

import yfinance as yf
from flask import Flask, request, jsonify


AIRPORT_URL = "https://www.airport-data.com/api/ap_info.json"

WEATHER_URL = "https://api.weatherapi.com/v1/current.json"
WEATHER_API_KEY = "bbb6de131963415e848183854242804"

app = Flask(__name__)


@app.route("/")
def root():
    temp_q = request.args.get("queryAirportTemp", None)
    stock_q = request.args.get("queryStockPrice", None)
    eval_q = request.args.get("queryEval", None)

    if [temp_q, stock_q, eval_q].count(None) != 2:
        return jsonify({"error": "Bad query parameters combination"}), 400

    if temp_q is not None:
        iata = temp_q.strip("\"")
        try:
            airport_res = requests.get(f"{AIRPORT_URL}?iata={iata}").json()
            lat = airport_res["latitude"]
            long = airport_res["longitude"]

            weather_res = requests.get(f"{WEATHER_URL}?key={WEATHER_API_KEY}&q={lat},{long}").json()
            temperature = weather_res["current"]["temp_c"]
        except Exception:
            return jsonify({"error": "Data for the airport unavailable"}), 404
        return jsonify(temperature), 200

    if stock_q is not None:
        try:
            stock_price = yf.Ticker(stock_q).fast_info.last_price
        except Exception:
            return jsonify({"error": "Invalid stock"}), 404

        return jsonify(stock_price), 200

    if eval_q is not None:
        eval_q = eval_q.strip("\"")
        return jsonify(eval(eval_q)), 200


if __name__ == '__main__':
    app.run()
