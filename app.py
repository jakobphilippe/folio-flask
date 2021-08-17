from flask import Flask, request, jsonify
import yfinance as yf
from multiprocessing.dummy import Pool as ThreadPool

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/stock/card_data', methods=['POST'])
def stock_card_data():
    tickers = request.json['tickers']
    pool = ThreadPool(100)
    results = pool.map(set_card_data, tickers)
    return jsonify(results)


def set_card_data(ticker):
    data_dict = {}
    t = yf.Ticker(ticker)
    info = t.info
    print(info)
    data_dict["ticker"] = ticker
    data_dict["name"] = info['shortName']
    if "sector" in info:
        data_dict["sector"] = info['sector']
    if "longBusinessSummary" in info:
        data_dict["desc"] = info['longBusinessSummary']
    price = info['regularMarketPrice']
    open_price = info['open']
    percent_change = (price - open_price) / open_price * 100
    data_dict["price"] = "%.2f" % price
    data_dict["percent_change"] = "%.2f" % percent_change
    data_dict["price_change"] = "%.2f" % (price - open_price)

    return data_dict


if __name__ == '__main__':
    app.run(threaded=True, port=5000)