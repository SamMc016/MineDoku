import random
from datetime import datetime

from flask import render_template, jsonify, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

from app import db
from app.blueprints import main
from app.forms import LoginForm, SignupForm
from app.models import *

def get_daily_puzzle(): # A function that determines the conditions of the board for the day
    blocks = Blocks.query.all()
    conditions = Conditions.query.all()
    today_seed = datetime.datetime.now().strftime("%Y-%m-%d")
    random.seed(today_seed)

    valid_board = False
    # Given 6 random conditions, 3 on the top row and 3 on the left column, find a board where there is at least 1 match for every square
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
                    break # Breaks out of inner loop
            if not is_solvable:
                break # Breaks out of outer loop

        if is_solvable:
            valid_board = True

    return top_row, side_col

@main.route("/api/save_game", methods=["POST"])
@login_required
def save_game(): # Saves game sessions for logged in users to their account rather than to local session data
    data = request.get_json()
    if not data or "board_state" not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    today_seed = datetime.datetime.now().strftime("%Y-%m-%d")
    game_session = Current_Game.query.filter_by(user_id=current_user.user_id).first()

    durability = data.get("durability", 9)
    us_score = data.get("us_score", 900)
    
    # If the user doesn't have a game session, create one
    if not game_session: 
        game_session = Current_Game(
            user_id = current_user.user_id,
            board_state = str(data["board_state"]),
            puzzle_date = today_seed,
            current_durability = durability,
            current_us = us_score
        )
        db.session.add(game_session)
    # If they do, update the session data
    else: 
        game_session.board_state = str(data["board_state"])
        game_session.puzzle_date = today_seed
        game_session.current_durability = durability
        game_session.current_us = us_score
    
    db.session.commit()
    return jsonify({"status": "success"})

@main.route("/api/get_game", methods=["GET"])
@login_required
def get_game(): # Retrieves saved game state tied to account 
    game_session = Current_Game.query.filter_by(user_id=current_user.user_id).first()
    today_seed = datetime.datetime.now().strftime("%Y-%m-%d")
    default_state = {"board_state": "none", "durability": 9, "us_score": 900}

    # If theres no game session saved, retrieve the default
    if not game_session: 
        return jsonify(default_state)
    
    # If there is a game session saved but the date is not today's date, retrieve the default
    if game_session.puzzle_date != today_seed: 
        db.session.delete(game_session)
        db.session.commit()
        return jsonify(default_state)

    # If theres is a game session saved but it is completely empty, retrieve the default
    if not game_session.board_state: 
        return jsonify(default_state)

    return jsonify({"board_state": game_session.board_state, "durability": game_session.current_durability, "us_score": game_session.current_us})

@main.route("/")
def index(): 
    blocks = Blocks.query.all()
    today_seed = datetime.datetime.now().strftime("%Y-%m-%d")
    top_row, side_col = get_daily_puzzle()

    global_stats = Game_Stats.query.first()
    # If there are no global stats for today's puzzle, create a blank slate
    if not global_stats: 
        global_stats = Game_Stats(global_games_played=0, last_reset_date=today_seed)
        db.session.add(global_stats)
        db.session.commit()
    # If there are global stats, but they aren't for today's puzzle, reset the data
    elif global_stats.last_reset_date != today_seed: 
        db.session.query(Block_Stats).delete()
        global_stats.lowest_uniqueness = 900
        global_stats.average_uniqueness = 0
        global_stats.global_games_played = 0
        db.session.query(Personal_Stats).update({Personal_Stats.daily_uniqueness: 900})
        global_stats.last_reset_date = today_seed
        db.session.commit()

    # Get all block stats 
    all_stats = db.session.query(
        Block_Stats.square_id, 
        Block_Stats.block_id, 
        func.sum(Block_Stats.times_chosen).label("total")
        ).group_by(Block_Stats.square_id, Block_Stats.block_id).all()
    
    square_totals = {}
    block_counts = {}
    
    # Pre-calculate totals per square and counts for each block 
    for stat in all_stats:
        square_totals[stat.square_id] = square_totals.get(stat.square_id, 0) + stat.total
        block_counts[(stat.square_id, stat.block_id)] = stat.total

    square_percentages = {}

    # loop through each square and each block in valid options to find percentages of the blocks
    for i in range(3):
        for j in range(3):
            square_id = (i * 3) + j + 1
            square_total = square_totals.get(square_id, 0)

            current_top_con = top_row[j].condition_id
            current_side_con = side_col[i].condition_id

            valid_options = [
                b for b in blocks if
                str(current_top_con) in b.condition_compatibility.split(",") and
                str(current_side_con) in b.condition_compatibility.split(",")
            ]

            num_options = len(valid_options)
            square_percentages[square_id] = []

            # for each block find its count, then use that to calculate the percentage of that block in that current square
            for block in blocks:
                count = block_counts.get((square_id, block.block_id), 0)
                
                if square_total == 0 or count == 0:
                    percentage = 0
                else:
                    percentage = ((count) / (square_total)) * 100

                square_percentages[square_id].append({
                    "block_id": block.block_id,
                    "name": block.block_name,
                    "percentage": round(percentage, 1)
                })
    
    # If the current user is logged in, save durability and unique score so that they can be grabbed by the get game function
    live_durability, live_us = 9, 900
    if current_user.is_authenticated:
        game_session = Current_Game.query.filter_by(user_id=current_user.user_id).first()

        if game_session: 
            if game_session.puzzle_date == today_seed:
                live_durability = game_session.current_durability
                live_us = game_session.current_us
            else:
                db.session.delete(game_session)
                db.session.commit()
        
    return render_template("index.html", blocks=blocks, square_percentages=square_percentages, top_row=top_row, side_col=side_col, max_durability=live_durability, US=live_us)


@main.route("/friends")
@login_required
def friends(): # A function that collates the leaderboards on the friends page 
    user_friend_ids = [friend.user_id for friend in current_user.friends]
    user_friend_ids.append(current_user.user_id)

    # Base query responsible for finding a user and their stats
    base_query = db.session.query(
        User.user_id,
        User.username,
        Personal_Stats.daily_uniqueness,
        Personal_Stats.lowest_uniqueness
    ).join(
        Personal_Stats, User.user_id == Personal_Stats.user_id
    ).filter(
        User.user_id.in_(user_friend_ids)
    )

    # Adaptions of the base query depending on which leaderboard it's needed for
    daily_leaderboard = base_query.filter(
        Personal_Stats.daily_uniqueness != 900).order_by(Personal_Stats.daily_uniqueness.asc()).all()
    all_time_leaderboard = base_query.filter(
        Personal_Stats.lowest_uniqueness != 0).order_by(Personal_Stats.lowest_uniqueness.asc()).all()

    return render_template("friends.html", daily=daily_leaderboard, all_time=all_time_leaderboard, friends_list=current_user.friends)


@main.route("/api/search_friends")
@login_required
def search_friends(): # A function responsible for searching for friends and adding them to the friends list
    query = request.args.get("q", "").lower().strip()
    if len(query) < 2:
        return jsonify([])

    # Checks the top 5 results in users and adds them to matches if they aren't the current users username
    users = User.query.filter(User.username.ilike(f"%{query}%")).limit(5).all()
    matches = [user.username for user in users if user.username.lower() != current_user.username.lower()]

    return jsonify(matches)


@main.route("/api/add_friend", methods=["POST"])
@login_required
def add_friend(): # A function responsible for adding a friend to the friends list
    data = request.get_json()
    friend_name = data.get("friend_name", "").strip()
    friend = User.query.filter_by(username=friend_name).first()

    # Error messages depending on different invalid inputs
    if not friend_name: 
        return jsonify({"success": False, "error": "Username required!"}), 400
    if not friend:
        return jsonify({"success": False, "error": "No user found with that username!"}), 404
    if friend_name.lower() == current_user.username.lower():
        return jsonify({"success": False, "error": "You cannot add yourself as a friend!"}), 400
    if friend in current_user.friends:
        return jsonify({"success": False, "error": "You are already friends with this user!"}), 400
    
    current_user.friends.append(friend)
    db.session.commit()
    return jsonify({"success": True})


@main.route("/account")
@login_required
def account(): # A function that checks a user's inventory against the blocks they've played, and changes the texture of the ones that they have played
    blocks = Blocks.query.all()
    unlocked_inventory = Inventory.query.filter_by(user_id=current_user.user_id).all()
    unlocked_block_ids = [item.block_id for item in unlocked_inventory]
    p_stats = Personal_Stats.query.filter_by(user_id=current_user.user_id).first()

    return render_template(
        "account.html",
        blocks=blocks,
        unlocked_block_ids=unlocked_block_ids,
        lowest_us=p_stats.lowest_uniqueness,
        average_us=p_stats.average_uniqueness,
        games_played=p_stats.total_games_played,
        games_won=p_stats.total_games_won,
    )


@main.route("/login", methods=["GET", "POST"])
def login(): # A function that handles logging in users
    form = LoginForm()
    if form.validate_on_submit(): 
        login_input = form.username.data
        user = User.query.filter(
            ((User.username == login_input) | (User.email == login_input))
        ).first()

        # Error messages depending on different invalid inputs
        if user is None:
            form.username.errors.append("An account with that username/email does not exist!")
        elif not check_password_hash(user.password_hash, form.password.data):
            form.password.errors.append("Incorrect password!")
        else:
            login_user(user)
            return redirect(url_for("main.index"))

    return render_template("login.html", form=form)


@main.route("/signup", methods=["GET", "POST"])
def signup(): # A function that handles signing up users
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        
        # Error messages depending on different invalid inputs
        if existing_user:
            if existing_user.username == username:
                form.username.errors.append("An account with that username already exists!")
            if existing_user.email == email:
                form.email.errors.append("An account with that email already exists!")

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(form.password.data)
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
def logout(): # A function that logs out the current user
    logout_user()
    return redirect(url_for("main.index"))


@main.route("/end_game")
def end_game_page(): # A function responsible for calculating final block percentages for the game 
    blocks = Blocks.query.all()
    top_row, side_col = get_daily_puzzle()
    global_stats = Game_Stats.query.first()

    # Check if any blocks have been played today
    raw_total = db.session.query(func.sum(Block_Stats.times_chosen)).scalar() or 0
    no_blocks_placed = (raw_total == 0)

    # Get all block stats 
    all_stats = db.session.query(
        Block_Stats.square_id, 
        Block_Stats.block_id, 
        func.sum(Block_Stats.times_chosen).label("total")
        ).group_by(Block_Stats.square_id, Block_Stats.block_id).all()


    square_totals = {}
    block_counts = {}

    # Pre-calculate totals per square and counts for each block 
    for stat in all_stats:
        square_totals[stat.square_id] = square_totals.get(stat.square_id, 0) + stat.total
        block_counts[(stat.square_id, stat.block_id)] = stat.total

    results = {}

    # loop through each square and each block in valid options to find percentages of the blocks
    for i in range(3):
        for j in range(3):
            square_id = (i * 3) + j + 1

            current_top_con = top_row[j].condition_id
            current_side_con = side_col[i].condition_id

            square_total = square_totals.get(square_id, 0)

            if square_total == 0:
                results[str(square_id)] = {
                    "least": "assets/blank.png", "least_name": "", "least_percent": 0,
                    "most": 'assets/blank.png', "most_name": "", "most_percent": 0,
                }
                continue
            
            square_results = []

            valid_options = [
                b for b in blocks if
                str(current_top_con) in b.condition_compatibility.split(",") and
                str(current_side_con) in b.condition_compatibility.split(",")
            ]

            num_options = len(valid_options)

            # for each block find its count, then use that to calculate the percentage of that block in that current square
            for block in valid_options:
                count = block_counts.get((square_id, block.block_id), 0)

                if count > 0:
                    block_percent = (((count) / (square_total)) * 100)
                    square_results.append({
                        "texture": block.face_texture_path,
                        "name": block.block_name,
                        "percent": round(block_percent, 1)
                    })
        
            if square_results:
                square_results.sort(key=lambda x: x["percent"])

                results[str(square_id)] = {
                    "least": square_results[0]["texture"], 
                    "least_name": square_results[0]["name"], 
                    "least_percent": square_results[0]["percent"],

                    "most": square_results[-1]["texture"], 
                    "most_name": square_results[-1]["name"], 
                    "most_percent": square_results[-1]["percent"],   
                }
            else:
                results[str(square_id)] = {
                    "least": "assets/blank.png", "least_name": "", "least_percent": 0,
                    "most": 'assets/blank.png', "most_name": "", "most_percent": 0,
                }

    square_percentages = {}
    return render_template("end_game.html", results=results, no_blocks_placed=no_blocks_placed, top_row=top_row, side_col=side_col, global_stats=global_stats, max_durability=9, US=900, square_percentages=square_percentages)

@main.route("/api/finish_game", methods=["POST"])
def finish_game(): # A function that is responible for committing all necessary data to their respective places
    data = request.get_json()    
    final_us = data.get("us_score", 900)
    blocks_placed = data.get("chosen_blocks", [])
    today_seed = datetime.datetime.now().strftime("%Y-%m-%d")

    # Update the global stats
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

    # Update the personal stats
    if current_user.is_authenticated:
        p_stats = Personal_Stats.query.filter_by(user_id=current_user.user_id).first()
        if not p_stats:
            p_stats = Personal_Stats(user_id=current_user.user_id, total_games_played=0, total_games_won=0, lowest_uniqueness=0, average_uniqueness=0)
            db.session.add(p_stats)
        
        p_stats.total_games_played += 1
        p_stats.daily_uniqueness = final_us

        if len(blocks_placed) == 9:
            p_stats.total_games_won += 1

        if p_stats.lowest_uniqueness == 0 or final_us < p_stats.lowest_uniqueness:
            p_stats.lowest_uniqueness = final_us

        if p_stats.average_uniqueness:
            p_stats.average_uniqueness = round(((p_stats.average_uniqueness + final_us) / 2), 0)
        else:
            p_stats.average_uniqueness = final_us

    # Update block stats and inventory
    for pair in blocks_placed:
        b_id = pair.get("block_id")
        s_id = pair.get("cell_id")

        b_stat = Block_Stats.query.filter_by(block_id=b_id, square_id=s_id).first()
        if b_stat:
            b_stat.times_chosen += 1
        else:
            db.session.add(Block_Stats(block_id=b_id, square_id=s_id, times_chosen=1))

        if current_user.is_authenticated:
            inv_exists = Inventory.query.filter_by(user_id=current_user.user_id, block_id=b_id).first()
            if not inv_exists:
                db.session.add(Inventory(user_id=current_user.user_id, block_id=b_id))
            
    db.session.commit()
    return jsonify({"success": True})