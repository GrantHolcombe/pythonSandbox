from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_cors import CORS
from markupsafe import escape

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
FlaskJSON(app)


@app.route('/', methods=['POST'])
def root():
    data = request.get_json(force=True)
    name = data['name']

    if name.lower() == 'corgi':
        msg = 'Wow what a majestic %s!' % escape(name)
    else:
        msg = '%s\'s are pretty cool dogs' % escape(name)

    return json_response(data=msg)
