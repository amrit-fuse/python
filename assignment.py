# Q1 >> http://127.0.0.1:5000/comments/int:id
# Q2 >> http://127.0.0.1:5000/comments/int:id
# Q3 >> http://127.0.0.1:5000/comments/int:id
# Q4 >> http://127.0.0.1:5000/comments/int:id/string:body/int:postId/int:u_id/string:username

# 123456
# using flask_restful
import json
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Comments(Resource):
    # 1. Create an API to return  body ,username based on comments id.
    def get(self, id):
        with open('comments.json', 'r') as f:
            data = json.load(f)
            # only select list with comments key from data dictionay
            for i in data['comments']:
                if i['id'] == id:
                    return jsonify({'body': i['body'], 'username': i['user']['username']})
            return jsonify({'message': 'No comment found!'})

    # 2. Create an API to update the body of the comment into uppercase and return comment id, body and status in json format based on  comment id provided.
    def put(self, id):  # edit comments.json
        with open('comments.json', 'r+') as f:  # open file in read and write mode
            data = json.load(f)  # load json file
            for i in data['comments']:  # loop through comments list
                if i['id'] == id:  # check if id is equal to id provided
                    i['body'] = i['body'].upper()  # update body to uppercase
                    f.seek(0)  # set file cursor to 0
                    json.dump(data, f, indent=4)  # dump data to file
                    f.truncate()  # truncate file
                    # return id, body and status
                    return jsonify({'id': i['id'], 'body': i['body'], 'status': 'updated'})
            # return message if id not found
            return jsonify({'message': 'No comment found!'})

    # 3. Create an API that delete record and return response message based on comment id.
    def delete(self, id):  # delete  a nested dict from comments.json
        with open('comments.json', 'r+') as f:  # open file in read and write mode
            data = json.load(f)  # load json file
            for i in data['comments']:  # loop through comments list
                if i['id'] == id:  # check if id is equal to id provided
                    # remove only particular dictionary matching the id provided
                    data['comments'].remove(i)
                    f.seek(0)  # set file cursor to 0
                    json.dump(data, f, indent=4)  # dump data to file
                    f.truncate()  # truncate file means delete  extra data from file
                    # return  message if id found and deleted successfully from file
                    return jsonify({'message': 'Comment deleted!'})
            # return message if id not found
            return jsonify({'message': 'No comment found!'})

    # 4. Create an API to insert new record and display response message along with data that has been inserted.

    def post(self, id, body, postId, u_id, username):  # add new dict to comments.json
        with open('comments.json', 'r+') as f:  # open file in read and write mode
            data = json.load(f)  # load json file
            for i in data['comments']:  # loop through comments list
                if i['id'] == id:  # check if id is equal to id provided
                    # return message if id already exist
                    return jsonify({'message': 'Comment already exist!'})

                # check if user id exist or not
                if i['user']['id'] == u_id:
                    # if user id exist then replace new uswername with old username existing in file
                    username = i['user']['username']

            # create new dictionary
            new_dict = {'id': id, 'body': body,  'postId': postId, 'user': {
                'id': u_id, 'username': username}}
            # append new dictionary to comments list
            data['comments'].append(new_dict)
            f.seek(0)
            json.dump(data, f, indent=4)  # dump data to file
            f.truncate()  # truncate file means delete  extra data from file
            # return message if id not found and new comment added successfully
            return jsonify({'message': 'Comment added sucessfully '})


# multiple url pointing to same class
# maps multiple url to same class
api.add_resource(Comments, '/comments/<int:id>',
                 '/comments/<int:id>/<string:body>/<int:postId>/<int:u_id>/<string:username>')

# driver function
if __name__ == '__main__':
    app.run(debug=True)
