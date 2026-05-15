window.addEventListener("load", () => {
    const tableDiv = document.querySelector(".table");

    if (!tableDiv) return;
    if (typeof renderBoard === "function") {
        setTimeout(() => updateEndGame("least"), 100);
    }
});

function updateEndGame(type) {    
    const resultCells = document.querySelectorAll(".gameboard-cell");

    resultCells.forEach(cell => {
        let name, texture, percent;

        if (type === "least") {
            name = cell.getAttribute("data-least-name");
            texture = cell.getAttribute("data-least");
            percent = cell.getAttribute("data-least-percent");
        } else {
            name = cell.getAttribute("data-most-name");
            texture = cell.getAttribute("data-most");
            percent = cell.getAttribute("data-most-percent");
        }

        if (name && name !== "") {
            cell.setAttribute("data-block", name);
            cell.setAttribute("data-texture", texture);
            cell.setAttribute("data-percentage", percent + "%");
        } else {
            cell.setAttribute("data-block", "");
            cell.setAttribute("data-texture", "");
            cell.setAttribute("data-percentage", "");
        }
    });
    
    if (typeof renderBoard === "function") {
        renderBoard();
    }
}

document.getElementById("leastBtn").addEventListener("click", () => {
    showLeast();
});
document.getElementById("mostBtn").addEventListener("click", () => {
    showMost();
});

function showLeast() {
    console.log("swapping to least");
    updateEndGame('least');}

function showMost() {
    console.log("swapping to most");
    updateEndGame('most');}
