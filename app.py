from flask import Flask, render_template, jsonify
import threading

from sniffer import start_sniffing, data_store

app = Flask(__name__)

sniffing = True


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/network")
def network():
    return render_template("network.html")


@app.route("/data")
def data():
    return jsonify(data_store)

import sniffer  # 🔥 ADD THIS


if __name__ == "__main__":
    t = threading.Thread(target=start_sniffing)
    t.daemon = True
    t.start()

    app.run(debug=True)