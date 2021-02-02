from flask import Flask, render_template, jsonify, request
from src.users import get_paginated_users

app = Flask(__name__)


@app.route("/ping")
@app.route("/index")
def index():
    # Health Check
    return "Hello, World!"


@app.route("/", methods=["GET"])
def profiles():
    rows_per_page_arg = int(request.args.get("rows", 25))
    page_number_arg = int(request.args.get("page", 1))
    users, rows_per_page, page_number = get_paginated_users(
        rows_per_page_arg, page_number_arg
    )

    return render_template(
        "profiles.html",
        users=users,
        rows_per_page=rows_per_page,
        page_number=page_number,
    )


@app.route("/api/profiles", methods=["GET"])
def api_profiles():
    rows_per_page_arg = int(request.args.get("rows", 25))
    page_number_arg = int(request.args.get("page", 1))
    users, rows, page = get_paginated_users(rows_per_page_arg, page_number_arg)
    result = {"users": users, "rows": rows, "page": page}
    return jsonify(result)
