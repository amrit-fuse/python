from flask import Flask  # Import Flask to allow us to create our app
app = Flask(__name__)   # Create a new instance of the Flask class called "app"


# The "@" decorator associates this route with the function immediately following
@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"  # Return the string 'Hello World!' as a response


if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode.
