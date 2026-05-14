import random
from datetime import datetime
from markupsafe import Markup
from app import db
from app.models import Blocks, Conditions, Block_Stats, Personal_Stats, Game_Stats, User, Inventory
from app.blueprints import main
from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from app.forms import LoginForm, SignupForm

global_friends = ["Alice", "Bob"]

def get_daily_puzzle():
    blocks = Blocks.query.all()
    conditions = Conditions.query.all()
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
    return top_row, side_col

@main.route("/")
def index():
    blocks = Blocks.query.all()
    today_seed = datetime.now().strftime("%Y-%m-%d")
    total_selections = db.session.query(func.sum(Block_Stats.times_chosen)).scalar() or 1
    top_row, side_col = get_daily_puzzle()

    global_stats = Game_Stats.query.first()
    if not global_stats:
        global_stats = Game_Stats(global_games_played=0, last_reset_date=today_seed)
        db.session.add(global_stats)
        db.session.commit()
    elif global_stats.last_reset_date != today_seed:
        db.session.query(Block_Stats).delete()

        global_stats.lowest_uniqueness = 900
        global_stats.average_uniqueness = 0
        global_stats.global_games_played = 0

        db.session.query(Personal_Stats).update({Personal_Stats.daily_uniqueness: 900})
        global_stats.last_reset_date = today_seed
        db.session.commit()

    for block in blocks:
            count = db.session.query(func.sum(Block_Stats.times_chosen)).filter(Block_Stats.block_id == block.block_id).scalar() or 0
            block.selection_percentage = (count / total_selections) * 100

    return render_template("index.html", blocks=blocks, top_row=top_row, side_col=side_col, max_durability=9, US=900)

@main.route("/friends")
@login_required
def friends():

    friends_list = [friend.username for friend in current_user.friends if friend != current_user.username]

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

    # LOWEST -> HIGHEST
    friends_scores = sorted(
        friends_scores,
        key=lambda player: player["score"]
    )

    all_time_scores = sorted(
        all_time_scores,
        key=lambda player: player["score"]
    )

    return render_template("friends.html", friends_list=friends_list, friends_scores=friends_scores, all_time_scores=all_time_scores)

@main.route("/search_friends")
def search_friends():

    query = request.args.get("q", "").lower()

    if len(query) < 2:
        return jsonify([])

    users = User.query.filter(
        User.username.ilike(f"%{query}%")
    ).limit(5).all()

    matches = [
        user.username for user in users
        if user.username.lower() != current_user.username.lower()
    ]

    return jsonify(matches)


@main.route("/add_friend", methods=["POST"])
def add_friend():
    from flask_login import current_user
    from app.models import User, db  # Fix import

    global global_friends

    data = request.get_json()

    friend_name = data["friend_name"]

    if (friend_name and friend_name not in global_friends and friend_name != current_user.username):
        global_friends.append(friend_name)
        print(global_friends)
        return jsonify({"success": True})
    
    data = request.get_json()
    friend_name = data["friend_name"]
    
    # Find the friend in database
    friend = User.query.filter_by(username=friend_name).first()
    
    if not friend:
        return jsonify({"success": False, "error": "User not found"}), 404
    
    # Check if trying to add self
    if friend.user_id == current_user.user_id:  # Use user_id, not id
        return jsonify({"success": False, "error": "Cannot add yourself"}), 400
    
    # Check if already friends
    if friend in current_user.friends:
        return jsonify({"success": False, "error": "Already friends"}), 400
    
    # Add the friend
    current_user.friends.append(friend)
    db.session.commit()
    
    print(f"Added friend: {friend_name}")
    return jsonify({"success": True})

@main.route("/account")
@login_required
def account():
    blocks = Blocks.query.all()

    unlocked_inventory = Inventory.query.filter_by(
        user_id=current_user.user_id
    ).all()

    unlocked_block_ids = [
        item.block_id for item in unlocked_inventory
    ]

    return render_template(
        "account.html",
        blocks=blocks,
        unlocked_block_ids=unlocked_block_ids
    )

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username_or_email = form.username.data
        password = form.password.data

        user = User.query.filter(
            (User.username == username_or_email) |
            (User.email == username_or_email)
        ).first()

        if user is None:
            form.username.errors.append("An account with that username/email does not exist!")
        elif not check_password_hash(user.password_hash, password):
            form.password.errors.append("Incorrect password!")
        
        if form.errors:
            return render_template("login.html", form=form)
        
        login_user(user)
        return redirect(url_for("main.index"))

    return render_template("login.html", form=form)

@main.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if request.method == "POST":
        form.validate()

        username = form.username.data
        email = form.email.data
        password = form.email.data

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            if existing_user.username == username:
                form.username.errors.append("An account with that username already exists!")

            if existing_user.email == email:
                form.email.errors.append("An account with that email already exists!")
            
        if form.errors:
            return render_template("signup.html", form=form)

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        new_stats = Personal_Stats(
            user_id=new_user.user_id,
            total_games_played=0,
            total_games_won=0,
            lowest_uniqueness=0,
            average_uniqueness=0,
            daily_uniqueness=0
        )

        db.session.add(new_stats)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("main.index"))

    return render_template("signup.html", form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@main.route("/end_game")
def end_game_page():
    blocks = Blocks.query.all()
    top_row, side_col = get_daily_puzzle()
    raw_total = db.session.query(func.sum(Block_Stats.times_chosen)).scalar() or 0
    global_stats = Game_Stats.query.first()

    no_blocks_placed = (raw_total == 0)
    total_selections = raw_total if raw_total > 0 else 1
        
    for block in blocks:
        count = db.session.query(func.sum(Block_Stats.times_chosen)).filter(Block_Stats.block_id == block.block_id).scalar() or 0
        block.selection_percentage = (count / total_selections) * 100

    results = {}

    for i, side in enumerate(side_col):
        for j, top in enumerate(top_row):
            sqaure_id = (i * 3) + j + 1
            square_total = db.session.query(func.sum(Block_Stats.times_chosen)).filter(Block_Stats.square_id == sqaure_id).scalar() or 0
            
            if square_total == 0:
                results[str(sqaure_id)] = {
                    "least": "assets/blank.png",
                    "least_name": "",
                    "least_percent": 0,
                    "most": 'assets/blank.png',
                    "most_name": "",
                    "most_percent": 0,
                }
                continue
        
            square_results = []
            valid_options = [b for b in blocks if
                            str(top.condition_id) in b.condition_compatibility.split(",") and
                            str(side.condition_id) in b.condition_compatibility.split(",") 
                            ]
            
            for block in valid_options:
                count = db.session.query(func.sum(Block_Stats.times_chosen))\
                    .filter(Block_Stats.block_id == block.block_id, Block_Stats.square_id == sqaure_id).scalar() or 0
                block_percent = round((count / square_total) * 100, 1) if square_total > 0 else 0

                if block_percent > 0:
                    square_results.append({
                        "texture": block.face_texture_path,
                        "name": block.block_name,
                        "percent": block_percent
                    })

            square_results.sort(key=lambda x: x["percent"])

            results[str(sqaure_id)] = {
                "least": square_results[0]["texture"],
                "least_name": square_results[0]["name"],
                "least_percent":square_results[0]["percent"],

                "most": square_results[-1]["texture"],
                "most_name": square_results[-1]["name"],
                "most_percent":square_results[-1]["percent"]
            }

    return render_template("end_game.html", results=results, no_blocks_placed=no_blocks_placed, top_row=top_row, side_col=side_col, global_stats=global_stats, max_durability=9, US=900)

@main.route("/finish_game", methods=["POST"])
def finish_game():
    data = request.get_json()    
    final_us = data.get("us_score")
    blocks_placed = data.get("chosen_blocks")
    today_seed = datetime.now().strftime("%Y-%m-%d")

    # game stats update
    global_stats = Game_Stats.query.first()

    if not global_stats:
        global_stats = Game_Stats(global_games_played=1, lowest_uniqueness=final_us, average_uniqueness=final_us, last_reset_date=today_seed)
        db.session.add(global_stats)
    else:
        global_stats.global_games_played += 1

        if global_stats.lowest_uniqueness is None or final_us < global_stats.lowest_uniqueness:
            global_stats.lowest_uniqueness = final_us

        if global_stats.average_uniqueness is None:
            global_stats.average_uniqueness = final_us
        else:
            global_stats.average_uniqueness = round(((global_stats.average_uniqueness + final_us) / 2), 0)

    # person stats update
    if not current_user.is_authenticated:
        p_stats = None
    else:
        p_stats = Personal_Stats.query.filter_by(user_id=current_user.user_id).first()
        if not p_stats:
            p_stats = Personal_Stats(user_id=current_user.user_id, total_games_played=0, total_games_won=0)
            db.session.add(p_stats)
        
        p_stats.total_games_played += 1
        p_stats.daily_uniqueness = final_us

        if len(blocks_placed) == 9:
            p_stats.total_games_won += 1

        if p_stats.lowest_uniqueness is None or final_us < p_stats.lowest_uniqueness:
            p_stats.lowest_uniqueness = final_us

        if p_stats.average_uniqueness:
            p_stats.average_uniqueness = round(((p_stats.average_uniqueness + final_us) / 2), 0)
        else:
            p_stats.average_uniqueness = final_us

    # block stats update 
    for pair in blocks_placed:
        b_id = pair.get("block_id")
        s_id = pair.get("cell_id")

        b_stat = Block_Stats.query.filter_by(block_id=b_id, square_id=s_id).first()
        if b_stat:
            b_stat.times_chosen += 1
        else:
            new_b_stat = Block_Stats(block_id=b_id, square_id=s_id, times_chosen=1)
            db.session.add(new_b_stat)

        # inventory update
        # If the user is logged in, remember that they have used this block before.
        if current_user.is_authenticated:
            inventory_item = Inventory.query.filter_by(
                user_id=current_user.user_id,
                block_id=b_id
            ).first()

            if not inventory_item:
                new_inventory_item = Inventory(
                    user_id=current_user.user_id,
                    block_id=b_id
                )
                db.session.add(new_inventory_item)

    db.session.commit()
    return jsonify({"success": True})