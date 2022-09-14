from flask import Flask
app = Flask(__name__)  # Create a new instance of the Flask class called "app"

# add vaiable rules to the route decorator /<variable_name>/


@app.route('/<int:number>/')
def incrementer(number):
    return "Incremented number is " + str(number+1)


# add vaiable rules to the route decorator /<variable_name>/
@app.route('/<string:name>/')
def hello(name):
    return "Hello " + name


if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode.
