from flask import Flask
from flask import jsonify
from flask import render_template
# from flask import request

from app.models.dfcandles import DataFrameCandle
from app.models.base import Session

import settings


app = Flask(__name__, template_folder='../../templates')


@app.teardown_appcontext
def remove_session(ex=None):
    Session.remove()


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/candle', methods=['GET'])
def cnadle_api():
    df = DataFrameCandle()
    df.set_all_candle_cls()

    return jsonify(df.values), 200


def run():
    app.run(host='127.0.0.1', port=settings.web_port, threaded=True)
