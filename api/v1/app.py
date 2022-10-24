#!/usr/bin/python3
"""
entry point of our application
"""

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def api_error(error):
    """a method that handles 404 error"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def tear_down(exception):
    """
     a method that closes the storage
    """
    storage.close()


if __name__ == "__main__":
    app.run(
            host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', 5000),
            threaded=True
        )
