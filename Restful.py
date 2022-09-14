# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.


class Hello(Resource):
    #  this method is called whenever there is GET request for this resource
    def get(self):
        return jsonify({'message': 'hello world'})

    # Corresponds to POST request
    def post(self):
        data = request.get_json()	 # status code
        # 201 is the status code for created resource
        return jsonify({'status code': data}), 201


# another resource to calculate the square of a number
class Square(Resource):
    def get(self, num):
        return jsonify({'square': num**2})


# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/')        # map '/' to Hello Resource

# map '/square/<int:num>' to Square Resource
api.add_resource(Square, '/square/<int:num>')


# driver function
if __name__ == '__main__':
    app.run(debug=True)
