from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route("/current_time")
def display_current_time():
    current_time = datetime.now().strftime("%H:%M")
    return f"<p>{current_time}</p>"


if __name__ == '__main__':
    app.run(debug=True)