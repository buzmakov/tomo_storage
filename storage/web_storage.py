from flask import Flask, url_for, request, make_response, jsonify

app = Flask(__name__)


def get_list_of_experiments():
    return 'Get list of all experiments'


@app.route('/')
def hello_world():
    with app.test_request_context():
        return '\n'.join([url_for('experiment'), ])


@app.route('/experiment', methods=['GET'])
@app.route('/experiment/<experiment_id>', methods=['GET', 'POST'])
def experiment(experiment_id=None):
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
