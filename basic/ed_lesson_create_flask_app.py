from flask import Flask
from datetime import datetime
import random

app = Flask(__name__)

@app.route("/current_time")
def display_current_time():
    current_time = datetime.now().strftime("%H:%M")
    return f"<p>{current_time}</p>"

@app.route("/coinflip")
def coin_flip():
    coin_list = ["Heads", "Tails"]
    return { "result": random.choice(coin_list) }


if __name__ == '__main__':
    app.run(debug=True)