#!/usr/bin/env python3
"""App module
"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """GET /
    Return:
      - welcome message
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
