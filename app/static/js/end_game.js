let durability = 9;

function makeGuess() {

    durability--;

    document.getElementById("durability-score").innerText =
        durability + "/9";

    if (durability <= 0) {
        endGame();
    }
}

function endGame() {
    alert("Game Over");
}