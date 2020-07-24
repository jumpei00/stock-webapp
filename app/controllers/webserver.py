from flask import Flask
from flask import jsonify
from flask import render_template
# from flask import request

from app.models.dfcandles import DataFrameCandle
from app.models.base import Session

import settings


app = Flask(__name__, static_folder='../../static', template_folder='../../templates')


@app.teardown_appcontext
def remove_session(ex=None):
    Session.remove()


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/candle', methods=['GET'])
def cnadle_api():
    df = DataFrameCandle()

    return jsonify(df.values), 200


def run():
    app.run(host='0.0.0.0', port=settings.web_port, threaded=True)
