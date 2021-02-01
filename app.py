from flask import Flask, render_template, jsonify, request
from src.models import GitHubUserOrm, GitHubUser
from src.db import session

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"


@app.route("/profiles", methods=["GET"])
def profiles():
    rows_per_page_arg = int(request.args.get("rows", 25))
    rows_per_page = rows_per_page_arg if rows_per_page_arg > 0 else 1

    page_number_arg = int(request.args.get("page", 1))
    page_number = page_number_arg if page_number_arg > 0 else 1

    raw_users = (
        session.query(GitHubUserOrm)
        .limit(rows_per_page)
        .offset((page_number - 1) * rows_per_page)
        .all()
    )
    users = [GitHubUser.from_orm(user).dict() for user in raw_users]
    return render_template(
        "profiles.html",
        users=users,
        rows_per_page=rows_per_page,
        page_number=page_number,
    )


@app.route("/api/profiles", methods=["GET"])
def api_profiles():
    raw_users = session.query(GitHubUserOrm).all()
    users = [GitHubUser.from_orm(user).dict() for user in raw_users]
    return jsonify(users)
