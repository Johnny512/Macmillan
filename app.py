from flask import Flask, request, render_template, jsonify, make_response
import json

app = Flask(__name__)

@app.route("/sreapi/v1/users", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return get_users()
    else:
        return add_user()

def get_users():
    with open('openapi.json', 'r') as file:
        data = json.loads(file.read())
        # Returns the list of users
        users = data['components']['schemas']['sreapi_v1_userlist']['example']['users']
        response = make_response(
            jsonify(
                users
            )
        )
        response.headers["Content-Type"] = "application/json"
    return response

def add_user():
    with open('openapi.json', 'r+') as file:
        data = json.load(file)
        # Grab the user to add
        user = data['components']['schemas']['sreapi_v1_user']['example']
        # Append the user
        data['components']['schemas']['sreapi_v1_userlist']['example']['users'].append(user)
        # Increase the user count by 1
        data['components']['schemas']['sreapi_v1_userlist']['example']['count'] += 1
        file.seek(0)
        # Save changes to file
        json.dump(data, file, indent=4)
        response = make_response(
            jsonify(
                data['components']['schemas']['sreapi_v1_userlist']['example']
            )
        )
        response.headers["Content-Type"] = "application/json"
    return response

@app.route('/')
def get_root():
    print('sending root')
    return render_template('index.html')

@app.route('/api/docs')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')
