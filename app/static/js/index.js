/* 
finds viable boards 
sets conditions randomly given they work with the board
gets viable blocks 
*/ 

/* function that brings up the selection screen */
const gameCells = document.querySelectorAll(".gameboard-cell")

gameCells.forEach(cell => {
    cell.addEventListener("click", () => {
        const squareId = cell.id;
        cellClick(squareId);
    });
    });

function cellClick(id) {
    window.currentSquare = id;
    const overlay = document.getElementById("inventory-overlay");
    overlay.classList.remove("hidden");
}

/* need a function that picks random conditions and checks that they work with each other (holy time complexity..) */

/* (maybe inside the one above) need a function that returns a list of acceptable block ids for each square */

/* need a function that actually checks if the block clicked is acceptable (if yes its placed, if no the square goes red and shakes) */

/* need a function that adds to block stats */

/* need a function that calculates US and drops durability by 1 per guess */

/* need functions that provide navigation to other parts of the website */