from flask import Blueprint, jsonify, request
from flask_login import login_required
from . import app, db

api = Blueprint("api", __name__)

@api.route("/query", methods=["POST"])
@login_required
def query():
	result = db.engine.execute(request.json["query"])
	rows = [list(row) for row in result]
	return jsonify({"results": rows}), 200
