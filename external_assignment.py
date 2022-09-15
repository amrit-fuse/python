# 6. Find any external API besides that given in the assignment. Retrieve the data from that api with the GET operation, clean the data and load it in your local as "example.json" file. Finally, perform all crud operations in that data.

# example.json is created in check.ipynb file (6)

from flask import Flask, jsonify, request
import json


app = Flask(__name__)


@app.route('/art', methods=['GET'])
def get_art():
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
        with open('example.json', 'r') as f:  # open file in read mode
            Art_dict = json.load(f)  # load json file   as dictionary
            try:
                # only select list with comments key from data dictionay
                for i in Art_dict['data']:
                    if i['id'] == id:
                        return jsonify({'id': id, 'title': i['title'], 'date_diaplay': i['date_display']})
            except Exception as e:
                return jsonify({'message': e.args})
            else:
                return jsonify({'message': 'No art found! with  id = {}'.format(id)})


@app.route('/update', methods=['PUT'])
def put_art():
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
        with open('example.json', 'r+') as f:  # open file in read and write mode
            Art_dict = json.load(f)  # load json file   as dictionary
            try:
                # only select list with comments key from data dictionay
                for i in Art_dict['data']:
                    if i['id'] == id:
                        # update body to uppercase
                        i['title'] = i['title'].upper()
                        # set file pointer to 0 position in file to overwrite file content
                        f.seek(0)
                        # write updated data to file
                        json.dump(Art_dict, f, indent=4)
                        f.truncate()  # truncate file to remove extra data
                        return jsonify({'id': id, 'title': i['title'], 'date_diaplay': i['date_display']})
            except Exception as e:
                return jsonify({'message': e.args})
            else:
                return jsonify({'message': 'No art found! with  id = {}'.format(id)})


@app.route('/delete', methods=['DELETE'])
def delete_art():
    print(request.url)
    # exception handling
    try:
        id = int(request.args.get('id'))  # get id from url
        if id < 1:
            raise ValueError  # raise value error if id is less than 1
    except ValueError:
        return jsonify({'message': 'Invalid id! has to be an +ve integer'})
    except Exception as e:
        return jsonify({'message': e.args})
    else:
        with open('example.json', 'r+') as f:
            Art_dict = json.load(f)
            try:
                for i in Art_dict['data']:
                    if i['id'] == id:
                        # delete list with id from data list
                        Art_dict['data'].remove(i)
                        # set file pointer to 0 position in file to overwrite file content
                        f.seek(0)
                        # write updated data to file
                        json.dump(Art_dict, f, indent=4)
                        f.truncate()  # truncate file to remove extra data
                        return jsonify({'message': 'Art with id = {} deleted!'.format(id)})
            except Exception as e:
                return jsonify({'message': e.args})
            else:
                return jsonify({'message': 'No art found! with  id = {}'.format(id)})


@app.route('/create', methods=['POST'])
def post_art():
    print(request.url)
    # exception handling
    try:
        id = int(request.args.get('id'))  # get id from url
        title = request.args.get('title')  # get title from url
        date_display = request.args.get(
            'date_display')  # get date_display from url
        if id < 1:
            raise ValueError  # raise value error if id is less than 1
    except ValueError:
        return jsonify({'message': 'Invalid id! has to be an +ve integer'})
    except Exception as e:
        return jsonify({'message': e.args})
    else:
        with open('example.json', 'r+') as f:
            Art_dict = json.load(f)
            try:
                # return if id already exists
                for i in Art_dict['data']:
                    if i['id'] == id:
                        return jsonify({'message': 'Art with id = {} already exists!'.format(id)})
                # create new list with id, title and date_display
                new_art = {'id': id, 'title': title,
                           'date_display': date_display}
                # append new list to data list
                Art_dict['data'].append(new_art)
                # set file pointer to 0 position in file to overwrite file content
                f.seek(0)
                # write updated data to file
                json.dump(Art_dict, f, indent=4)
                f.truncate()  # truncate file to remove extra data
                return jsonify({'id': id, 'title': title, 'date_display': date_display})
            except Exception as e:
                return jsonify({'message': e.args})


if __name__ == '__main__':
    app.run(debug=True)
