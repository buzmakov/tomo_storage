# encoding: utf-8
import os

from flask import Flask, request, make_response, jsonify  # , redirect, url_for
from werkzeug import secure_filename
from flask.ext.httpauth import HTTPBasicAuth
import uuid
from users import users

app = Flask(__name__)

# configuration for uploads
UPLOAD_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), '../data/files')
)

ALLOWED_EXTENSIONS = {'txt', 'py'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# configuration for auth
auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


def get_list_of_phantoms():
    return 'Get list of all phantoms'


@app.route('/', methods=['GET'])
@auth.login_required
def hello_world():
    return jsonify(user=auth.username())


@app.route('/phantoms', methods=['GET'])
@app.route('/phantoms/<phantom_id>', methods=['GET', 'POST'])
def phantoms(phantom_id=None):
    if phantom_id is None:
        return get_list_of_phantoms()
    else:
        if request.method == 'POST':
            return 'This should create new phantom: {}'.format(
                phantom_id)
        elif request.method == 'GET':
            return 'This should return information on phantom: {}'.format(
                phantom_id)
        else:
            return make_response(jsonify({'error': 'Unsupported method'}), 400)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['GET', 'POST'])
@auth.login_required
def upload():
    if request.method == 'POST':
        file_id = uuid.uuid4()
        file = request.files['file']
        response = {}
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            response['filename'] = filename
            response['file_id'] = file_id
            # return redirect(url_for('upload'))
        else:
            return make_response(jsonify(
                {'error': 'Unsupported file extension'}), 400)
        # response.update(request.form)
        return make_response(jsonify(response))
    elif request.method == 'GET':
        return """
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form action="" method=post enctype=multipart/form-data>
              <p><input type=file name=file>
                 <input type=submit value=Upload>
            </form>
            <p>{}</p>
            """ .format("<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],)))


if __name__ == '__main__':
    app.run(debug=True)
