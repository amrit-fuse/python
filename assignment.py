# Q1>> http://127.0.0.1:5000/comments?id=1

from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# 1. Create an API to return  body ,username based on comments id.


@app.route('/comments', methods=['GET'])
def get_comment():
    print(request.url)
    # exception handling
    try:
        id = int(request.args.get('id'))  # get id from url
        if id < 1:
            raise ValueError  # raise value error if id is less than 1
    except ValueError:
        return jsonify({'message': 'Invalid id! has to be an +ve integer'})
    except Exception as e:  # handle other exceptions
        return jsonify({'message': e.args})
    else:  # if no exception
        with open('comments.json', 'r') as f:  # open file in read mode
            data = json.load(f)  # load json file   as dictionary
            try:
                # only select list with comments key from data dictionay
                for i in data['comments']:
                    if i['id'] == id:
                        return jsonify({'body': i['body'], 'username': i['user']['username']})
            except Exception as e:
                return jsonify({'message': e.args})  # handle other exceptions
            else:   # if no exception
                return jsonify({'message': 'No comment found! with  id = {}'.format(id)})


# 2. Create an API to update the body of the comment into uppercase and return comment id, body and status in json format based on  comment id provided.

@app.route('/update', methods=['PUT'])
def put_comment():
    print(request.url)
    # exception handling
    try:
        id = int(request.args.get('id'))  # get id from url
        if id < 1:
            raise ValueError  # raise value error if id is less than 1
    except ValueError:
        return jsonify({'message': 'Invalid id! has to be an +ve integer'})
    except Exception as e:  # handle other exceptions
        return jsonify({'message': e.args})
    else:  # if no exception
        with open('comments.json', 'r+') as f:  # open file in read and write mode
            data = json.load(f)  # load json file   as dictionary
            try:
                # only select list with comments key from data dictionay
                for i in data['comments']:
                    if i['id'] == id:
                        # update body to uppercase
                        i['body'] = i['body'].upper()
                        # set file pointer to 0 position in file to overwrite file content
                        f.seek(0)
                        # dump updated data to file
                        json.dump(data, f, indent=4)
                        f.truncate()  # truncate file means remove extra data from file after updating data
                        return jsonify({'id': i['id'], 'body': i['body'], 'status': 'updated'})
            except Exception as e:
                return jsonify({'message': e.args})
            else:
                return jsonify({'message': 'No comment found! with  id = {}'.format(id)})


# 3. Create an API that delete record and return response message based on comment id.


@app.route('/delete', methods=['DELETE'])
def delete_comment():
    print(request.url)
    # exception handling
    try:
        id = int(request.args.get('id'))  # get id from url
        if id < 1:
            raise ValueError  # raise value error if id is less than 1
    except ValueError:
        return jsonify({'message': 'Invalid id! has to be an +ve integer'})
    except Exception as e:  # handle other exceptions
        return jsonify({'message': e.args})
    else:  # if no exception
        with open('comments.json', 'r+') as f:  # open file in read and write mode
            data = json.load(f)  # load json file   as dictionary
            try:
                # only select list with comments key from data dictionay
                for i in data['comments']:
                    if i['id'] == id:
                        # remove comment from list
                        data['comments'].remove(i)
                        # set file pointer to 0 position in file to overwrite file content
                        f.seek(0)
                        # dump updated data to file
                        json.dump(data, f, indent=4)
                        f.truncate()  # truncate file means remove extra data from file after updating data
                        return jsonify({'message': 'comment deleted! with id = {}'.format(id)})
            except Exception as e:
                return jsonify({'message': e.args})
            else:
                return jsonify({'message': 'No comment found! with  id = {}'.format(id)})


# 4. Create an API to insert new record and display response message along with data that has been inserted.


@app.route('/insert', methods=['POST'])
def insert_comment():
    print(request.url)
    # exception handling
    try:
        id = int(request.args.get('id'))  # get id from url
        body = request.args.get('body')
        post_id = int(request.args.get('post_id'))
        user_id = int(request.args.get('user_id'))
        username = request.args.get('username')

        if id < 1 or post_id < 1 or user_id < 1:
            raise ValueError  # raise value error if id is less than 1
    except ValueError:
        return jsonify({'message': 'Invalid id! , has to be an +ve integer'})
    # except Exception as e:  # handle other exceptions
    #     return jsonify({'message': e.args})
    else:  # if no exception
        with open('comments.json', 'r+') as f:  # open file in read and write mode
            data = json.load(f)  # load json file   as dictionary
            try:
                # only select list with comments key from data dictionay
                for i in data['comments']:
                    if i['id'] == id:
                        return jsonify({'message': 'comment already exist! with id = {}'.format(id)})
                # create new comment dictionary
                new_comment = {'id': id, 'body': body, 'post_id': post_id, 'user': {
                    'id': user_id, 'username': username}}
                # append new comment to list
                data['comments'].append(new_comment)
                # set file pointer to 0 position in file to overwrite file content
                f.seek(0)
                # dump updated data to file
                json.dump(data, f, indent=4)
                f.truncate()  # truncate file means remove extra data from file after updating data
                return jsonify({'message': 'comment inserted! with id = {}'.format(id)})
            except Exception as e:
                return jsonify({'message': e.args})


# 5. Create an API that returns count of comments along with username and status in JSON format.
@app.route('/count', methods=['GET'])
def count_comment():
    print(request.url)
    with open('comments.json', 'r') as f:
        data = json.load(f)
        try:
            # create new dictionary to store count of comments for each username and status
            count = {}
            # only select list with comments key from data dictionay
            for i in data['comments']:
                # if username is not in count dictionary then add username as key and set count to 1
                if i['user']['username'] not in count:
                    count[i['user']['username']] = 1
                else:
                    # if username is already in count dictionary then increment count by 1
                    count[i['user']['username']] += 1

            return jsonify(count)
        except Exception as e:
            return jsonify({'message': e.args})


if __name__ == '__main__':
    app.run(debug=True)
