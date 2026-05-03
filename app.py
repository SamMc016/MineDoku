from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/friends")
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

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/login")
def login():
    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True)

