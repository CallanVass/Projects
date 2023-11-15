from flask import Flask, request, abort


app = Flask(__name__)


# Calculator
@app.route("/<int:num1>/<operator>/<int:num2>")
def add_nums(num1, operator, num2):
    result_add = num1 + num2
    result_minus = num1 - num2
    result_multiply = num1 * num2
    result_divide = num1 // num2
    match operator:
        case "add": 
            return {
                "operation": f"{num1} plus {num2}",
                "result": result_add
            }
        case "subtract": 
            return {
                "operation": f"{num1} minus {num2}",
                "result": result_minus
            }
        case "divide": 
            return {
                "operation": f"{num1} divided by {num2}",
                "result": result_divide
            }
        case "multiply": 
            return {
                "operation": f"{num1} multiplied by {num2}",
                "result": result_multiply
            }
        case _:
            abort(404)
        
if __name__ == '__main__':
    app.run(debug=True)