import random
from datetime import datetime
from app import db
from app.models import Blocks, Conditions, Block_Stats
from flask import render_template, request, jsonify
from sqlalchemy import func
from app.blueprints import main

@main.route("/")
def index():
    blocks = Blocks.query.all()
    conditions = Conditions.query.all()
    total_selections = db.session.query(func.sum(Block_Stats.times_chosen)).scalar() or 1

    today_seed = datetime.now().strftime("%Y-%m-%d")
    random.seed(today_seed)

    valid_board = False
    while not valid_board:
        selected_conditions = random.sample(conditions, 6)
        top_row = selected_conditions[:3]
        side_col = selected_conditions[3:]

        is_solvable = True
        for top in top_row:
            for side in side_col:
                match_exists = any(
                    str(top.condition_id) in b.condition_compatibility.split(",") and 
                    str(side.condition_id) in b.condition_compatibility.split(",")
                    for b in blocks)
                if not match_exists:
                    is_solvable = False
                    break
            if not is_solvable:
                break
        if is_solvable:
            valid_board = True

    return render_template("index.html", blocks=blocks, top_row=top_row, side_col=side_col, max_durability=9)

@main.route("/friends")
def friends():
    friends_list = ["Alice", "Bob", "Charlie", "Dana"]
    friends_scores = [
        {"name": "Alice", "score": 1200},
        {"name": "Bob", "score": 950},
        {"name": "Charlie", "score": 870}
    ]
    all_time_scores = [
        {"name": "ProGamer1", "score": 5000},
        {"name": "SpeedKing", "score": 4800},
        {"name": "LegendX", "score": 4500}
    ]

    return render_template(
        "friends.html",
        page_title="MINEDOKU",
        friends_list=friends_list,
        friends_scores=friends_scores,
        all_time_scores=all_time_scores
    )

@main.route("/account")
def account():
    return render_template("account.html")

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/signup")
def signup():
    return render_template("signup.html")

@main.route("/end_game")
def end_game_page():
        return render_template("end_game.html")

@main.route("/finish_game", methods=["POST"])
def finish_game():
    data = request.get_json()

    score = data.get("us_score")
    blocks = data.get("chosen_blocks")

    return jsonify({"success": True})