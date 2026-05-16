
/* End Game Logic */

window.addEventListener("load", () => {
    const resultCells = document.querySelectorAll(".gameboard-cell");
    const tableDiv = document.querySelector(".table");

    if (!tableDiv || resultCells.length === 0) return;

    resultCells.forEach(cell => {
        const img = cell.querySelector("img");
        cell.dataset.block = cell.dataset.leastName;
        cell.dataset.texture = img.src;
        let pct = parseFloat(cell.dataset.leastPercent) || 0;
        cell.dataset.percentage = pct.toFixed(1) + "%";
        img.style.visibility = "hidden";
    });
    if (typeof renderBoard === "function") {
        setTimeout(() => {
            renderBoard();
        }, 100);
    }
});

function showLeast() {
    document.querySelectorAll(".result-cell").forEach(cell => {
        cell.dataset.block = cell.dataset.leastName;
        cell.dataset.texture = cell.dataset.least;
        let pct = parseFloat(cell.dataset.leastPercent) || 0;
        cell.dataset.percentage = pct.toFixed(1) + "%";
    });
    renderBoard();
}    

function showMost() {
    document.querySelectorAll(".result-cell").forEach(cell => {
        cell.dataset.block = cell.dataset.mostName;
        cell.dataset.texture = cell.dataset.most;
        let pct = parseFloat(cell.dataset.mostPercent) || 0;
        cell.dataset.percentage = pct.toFixed(1) + "%";
    });
    renderBoard();
}    
