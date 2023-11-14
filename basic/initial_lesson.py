from flask import Flask, request


app = Flask(__name__)

@app.route('/')
def index():
    return '<h3>Goodbye, World!</h3>'

@app.route('/spam')
def spam():
    person = { "name": "John", "age": 17 }
    return person

@app.errorhandler(404)
def not_found(error):
    return { "error": str(error) }, 404

@app.route("/hello")
def hello():
    name = request.args.get("name")
    # name = "jack"
    return {"message": f"Hello, {name}!"}



if __name__ == '__main__':
    app.run(debug=True)