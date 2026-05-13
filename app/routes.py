import random
from datetime import datetime
from app import db
from app.models import Blocks, Conditions, Block_Stats, Personal_Stats, Game_Stats, User, Inventory
from app.blueprints import main
from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from app.forms import LoginForm, SignupForm

@main.route("/")
def index():
    blocks = Blocks.query.all()
    conditions = Conditions.query.all()
    total_selections = db.session.query(func.sum(Block_Stats.times_chosen)).scalar() or 1

    today_seed = datetime.now().strftime("%Y-%m-%d")
    random.seed(today_seed)

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

    for block in blocks:
            count = db.session.query(func.sum(Block_Stats.times_chosen)).filter(Block_Stats.block_id == block.block_id).scalar() or 0
            block.selection_percentage = (count / total_selections) * 100

    return render_template("index.html", blocks=blocks, top_row=top_row, side_col=side_col, max_durability=9, US=900)

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

        if user is None or not check_password_hash(user.password_hash, password):
            flash("Invalid username/email or password.")
            return redirect(url_for("main.login"))

        login_user(user)
        return redirect(url_for("main.index"))

    if request.method == "POST":
        print("LOGIN FORM ERRORS:", form.errors)

    return render_template("login.html", form=form)

@main.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.")
            return redirect(url_for("main.signup"))

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
            lowest_uniqueness=None,
            average_uniqueness=None,
            daily_uniqueness=None
        )

        db.session.add(new_stats)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("main.index"))

    if request.method == "POST":
        print("SIGNUP FORM ERRORS:", form.errors)

    return render_template("signup.html", form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@main.route("/end_game")
def end_game_page():
        return render_template("end_game.html")

@main.route("/finish_game", methods=["POST"])
def finish_game():
    data = request.get_json()    
    final_us = data.get("us_score")
    blocks_placed = data.get("chosen_blocks")
    today_seed = datetime.now().strftime("%Y-%m-%d")

    # game stats update
    global_stats = Game_Stats.query.first()

    if not global_stats:
        global_stats = Game_Stats(global_games_played=1,lowest_uniqueness=final_us, average_uniqueness=final_us, last_reset_date=today_seed)
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