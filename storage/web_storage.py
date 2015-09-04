# encoding: utf-8
import os
import tempfile

from flask import Flask, request, make_response, jsonify, send_file, abort
# from werkzeug import secure_filename,
from flask.ext.httpauth import HTTPBasicAuth

import users
import storage_core

app = Flask(__name__)

# configuration for uploads
UPLOAD_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), '../data/files/tmp')
)

ALLOWED_EXTENSIONS = {'txt', 'py'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# configuration for auth
auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    if username in users.users_list:
        return users.users_list.get(username)
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


# @app.route("/upload", methods=['GET', 'POST'])
# @auth.login_required
# def upload():
#     if request.method == 'POST':
#         file = request.files['file']
#         response = {}
#         if file and allowed_file(file.filename):
#             filename = tempfile.mkstemp(dir=app.config['UPLOAD_FOLDER'])
#             # filename = secure_filename(file.filename)
#             # filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filename)
#             return redirect(url_for('upload'))
#         else:
#             return make_response(jsonify(
#                 {'error': 'Unsupported file extension'}), 400)
#         return make_response(jsonify(response))
#     elif request.method == 'GET':
#         return """
#             <!doctype html>
#             <title>Upload new File</title>
#             <h1>Upload new File</h1>
#             <form action="" method=post enctype=multipart/form-data>
#               <p><input type=file name=file>
#                  <input type=submit value=Upload>
#             </form>
#             <p>{}</p>
#             """ .format("<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))
#                       )


@app.route("/files", methods=['GET'])
@auth.login_required
def files_listfiles(file_id=None):
    return make_response(jsonify(
        {'status': 'ok', 'id': storage_core.get_files_list()}), 200)


@app.route("/files", methods=['POST'])
@auth.login_required
def post_file():
    file = request.files['file']
    response = {}
    if file and allowed_file(file.filename):
        file_tags = {'original_file_name': file.filename}
        file_tags.update(request.form)
        file_descr, file_path = tempfile.mkstemp(
            dir=app.config['UPLOAD_FOLDER'])
        file_obj = os.fdopen(file_descr, 'w')
        file.save(file_obj)
        file_obj.close()
        status = storage_core.store_file(file_path, file_tags)
        if os.path.exists(file_path):
            os.remove(file_path)
        response.update(status)
    else:
        return make_response(jsonify(
            {'error': 'Unsupported file extension'}), 400)
    return make_response(jsonify(response))


@app.route("/files/<file_id>", methods=['GET'])
@auth.login_required
def get_file(file_id):
    file_dict = storage_core.get_file_info(file_id)
    if not file_dict['status'] == 'ok':
        return abort(404)
    print file_dict['status'], file_dict['file_name']
    if os.path.isfile(file_dict['file_name']):
        return send_file(file_dict['file_name'], as_attachment=True)
    else:
        return abort(404)


@app.route("/files/<file_id>", methods=['DELETE'])
@auth.login_required
def delete_file(file_id):
    delete_info = storage_core.delete_file(file_id)
    return make_response(jsonify(delete_info))


if __name__ == '__main__':
    app.run(debug=True)
