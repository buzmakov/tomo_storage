from flask import Flask, request, make_response, jsonify
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": "tomo_admin",
    "user": "tomo_user"
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


def get_list_of_experiments():
    return 'Get list of all experiments'


@app.route('/', methods=['GET'])
@auth.login_required
def hello_world():
    return jsonify(user=auth.username())


@app.route('/experiments', methods=['GET'])
@app.route('/experiments/<experiment_id>', methods=['GET', 'POST'])
def experiments(experiment_id=None):
    if experiment_id is None:
        return get_list_of_experiments()
    else:
        if request.method == 'POST':
            return 'This should create new experiment: {}'.format(
                experiment_id)
        elif request.method == 'GET':
            return 'This should return information on experiment: {}'.format(
                experiment_id)
        else:
            return make_response(jsonify({'error': 'Unsupported method'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
