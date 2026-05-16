/* End game page logic */


/* Initialise end game board */
window.addEventListener("load", () => {

    /* Main board container */
    const tableDiv =
        document.querySelector(".table");

    /* Stop if board does not exist */
    if (!tableDiv) return;


    /* Render least common blocks by default */
    if (typeof renderBoard === "function") {

        setTimeout(() => {

            updateEndGame("least");

        }, 100);
    }
});


/* Update end game display */

function updateEndGame(type) {

    const resultCells =
        document.querySelectorAll(".gameboard-cell");


    resultCells.forEach(cell => {

        let blockName;
        let blockTexture;
        let blockPercent;


        /* Least common mode */

        if (type === "least") {

            blockName =
                cell.getAttribute("data-least-name");

            blockTexture =
                cell.getAttribute("data-least");

            blockPercent =
                cell.getAttribute("data-least-percent");


        /* Most common mode */

        } else {

            blockName =
                cell.getAttribute("data-most-name");

            blockTexture =
                cell.getAttribute("data-most");

            blockPercent =
                cell.getAttribute("data-most-percent");
        }


        /* Update cell data */

        if (blockName && blockName !== "") {

            cell.setAttribute(
                "data-block",
                blockName
            );

            cell.setAttribute(
                "data-texture",
                blockTexture
            );

            cell.setAttribute(
                "data-percentage",
                `${blockPercent}%`
            );

        } else {

            
            cell.setAttribute("data-block", "");

            cell.setAttribute("data-texture", "");

            cell.setAttribute("data-percentage", "");
        }
    });


    /* Re-render board */

    if (typeof renderBoard === "function") {

        renderBoard();
    }
}

/* Show least common blocks */
document.getElementById("leastBtn")
    .addEventListener("click", () => {

    showLeast();
});


/* Show most common blocks */
document.getElementById("mostBtn")
    .addEventListener("click", () => {

    showMost();
});


/* Show the least common results */

function showLeast() {

    console.log("Swapping to least common");

    updateEndGame("least");
}


/* Show the most common results */

function showMost() {

    console.log("Swapping to most common");

    updateEndGame("most");
}