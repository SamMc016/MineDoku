/* End Game Logic */

window.addEventListener("load", () => {

    /* Get all result cells from the gameboard */
    const resultCells =
        document.querySelectorAll(".gameboard-cell");

    /* Main table container */
    const tableDiv =
        document.querySelector(".table");

    /* Stop if board does not exist */
    if (!tableDiv || resultCells.length === 0) return;


    /* Prepare Least Common Data */

    resultCells.forEach(cell => {

        /* Image inside each board cell */
        const img = cell.querySelector("img");

        /* Default display = least common */
        cell.dataset.block =
            cell.dataset.leastName;

        cell.dataset.texture =
            cell.dataset.least;

        /* Format percentage to 1 decimal place */
        const percentage =
            parseFloat(cell.dataset.leastPercent) || 0;

        cell.dataset.percentage =
            `${percentage.toFixed(1)}%`;

        /* Hide raw image because renderBoard()
           rebuilds the visual board */
        img.style.visibility = "hidden";
    });


    /* Render Board */

    if (typeof renderBoard === "function") {

        /* Small delay ensures board is fully loaded */
        setTimeout(() => {

            renderBoard();

        }, 100);
    }
});


/* Display Least Common Blocks */

function showLeast() {

    document.querySelectorAll(".result-cell")
        .forEach(cell => {

        /* Update block name */
        cell.dataset.block =
            cell.dataset.leastName;

        /* Update block texture */
        cell.dataset.texture =
            cell.dataset.least;

        /* Update percentage */
        const percentage =
            parseFloat(cell.dataset.leastPercent) || 0;

        cell.dataset.percentage =
            `${percentage.toFixed(1)}%`;
    });

    /* Re-render updated board */
    renderBoard();
}


/* Display Most Common Blocks */

function showMost() {

    document.querySelectorAll(".result-cell")
        .forEach(cell => {

        /* Update block name */
        cell.dataset.block =
            cell.dataset.mostName;

        /* Update block texture */
        cell.dataset.texture =
            cell.dataset.most;

        /* Update percentage */
        const percentage =
            parseFloat(cell.dataset.mostPercent) || 0;

        cell.dataset.percentage =
            `${percentage.toFixed(1)}%`;
    });

    /* Re-render updated board */
    renderBoard();
}