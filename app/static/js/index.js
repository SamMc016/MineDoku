/* 
finds viable boards 
sets conditions randomly given they work with the board
gets viable blocks 
*/ 

const gameCells = document.querySelectorAll(".gameboard-cell");
const inventoryCells = document.querySelectorAll(".inventory-cell");
const overlay = document.getElementById("inventory-overlay");
const backButton = document.getElementById("backFromInventory");

/* Opens inventory when a main grid cell is clicked */
gameCells.forEach(cell => {
    cell.addEventListener("click", () => {
        window.currentSquare = cell.id;
        overlay.classList.remove("hidden");
    });
});

/* Closes inventory when back button is clicked */
backButton.addEventListener("click", () => {
    overlay.classList.add("hidden");
});

/* Places selected inventory block into selected main grid cell */
inventoryCells.forEach(cell => {
    cell.addEventListener("click", () => {
        const blockName = cell.dataset.block;
        const selectedGameCell = document.getElementById(window.currentSquare);

        selectedGameCell.dataset.block = blockName;

        renderBoard(window.currentSquare);
        overlay.classList.add("hidden");
    });
});

function renderBoard(newlyPlacedId = null) {
    const board = document.querySelector(".table table");
    const boardRect = board.getBoundingClientRect();

    const vanishingPoint = {
        x: boardRect.left + boardRect.width / 2,
        y: boardRect.top + boardRect.height / 2
    };

    const depthAmount = 0.22;

    gameCells.forEach(cell => {
        const blockName = cell.dataset.block;

        if (!blockName) {
            return;
        }

        const id = Number(cell.id);
        const row = Math.floor((id - 1) / 3);
        const col = (id - 1) % 3;

        const isTopRow = row === 0;
        const isBottomRow = row === 2;

        const isLeftColumn = col === 0;
        const isRightColumn = col === 2;

        const hasRight = col < 2 && document.getElementById(String(id + 1)).dataset.block;
        const hasLeft = col > 0 && document.getElementById(String(id - 1)).dataset.block;
        const hasBelow = row < 2 && document.getElementById(String(id + 3)).dataset.block;
        const hasAbove = row > 0 && document.getElementById(String(id - 3)).dataset.block;

        const texturePath = `/static/assets/game_textures/${blockName}.png`;
        const animationClass = String(id) === String(newlyPlacedId) ? "newly-placed" : "";

        let blockHTML = `
            <div class="block-3d ${animationClass}">
                <div class="block-face block-front" style="background-image: url('${texturePath}')"></div>
        `;

        if (isLeftColumn && !hasRight) {
            blockHTML += createPerspectiveFace(cell, "right", texturePath, vanishingPoint, depthAmount);
        }

        if (isRightColumn && !hasLeft) {
            blockHTML += createPerspectiveFace(cell, "left", texturePath, vanishingPoint, depthAmount);
        }

        if (isTopRow && !hasBelow) {
            blockHTML += createPerspectiveFace(cell, "bottom", texturePath, vanishingPoint, depthAmount);
        }

        if (isBottomRow && !hasAbove) {
            blockHTML += createPerspectiveFace(cell, "top", texturePath, vanishingPoint, depthAmount);
        }

        blockHTML += `</div>`;

        cell.innerHTML = blockHTML;
    });
}

function createPerspectiveFace(cell, side, texturePath, vanishingPoint, depthAmount) {
    const rect = cell.getBoundingClientRect();

    const corners = {
        topLeft: { x: rect.left, y: rect.top },
        topRight: { x: rect.right, y: rect.top },
        bottomRight: { x: rect.right, y: rect.bottom },
        bottomLeft: { x: rect.left, y: rect.bottom }
    };

    let edgeStart;
    let edgeEnd;
    let className;

    if (side === "right") {
        edgeStart = corners.topRight;
        edgeEnd = corners.bottomRight;
        className = "block-side";
    }

    if (side === "left") {
        edgeStart = corners.bottomLeft;
        edgeEnd = corners.topLeft;
        className = "block-side";
    }

    if (side === "top") {
        edgeStart = corners.topLeft;
        edgeEnd = corners.topRight;
        className = "block-top";
    }

    if (side === "bottom") {
        edgeStart = corners.bottomRight;
        edgeEnd = corners.bottomLeft;
        className = "block-bottom";
    }

    const projectedStart = projectTowardPoint(edgeStart, vanishingPoint, depthAmount);
    const projectedEnd = projectTowardPoint(edgeEnd, vanishingPoint, depthAmount);

    const points = [
        edgeStart,
        edgeEnd,
        projectedEnd,
        projectedStart
    ];

    const localPoints = points.map(point => ({
        x: point.x - rect.left,
        y: point.y - rect.top
    }));

    const minX = Math.min(...localPoints.map(p => p.x));
    const minY = Math.min(...localPoints.map(p => p.y));
    const maxX = Math.max(...localPoints.map(p => p.x));
    const maxY = Math.max(...localPoints.map(p => p.y));

    const width = maxX - minX;
    const height = maxY - minY;

    const polygon = localPoints.map(p => {
        const xPercent = ((p.x - minX) / width) * 100;
        const yPercent = ((p.y - minY) / height) * 100;
        return `${xPercent}% ${yPercent}%`;
    }).join(", ");

    return `
        <div 
            class="block-face ${className}"
            style="
                left: ${minX}px;
                top: ${minY}px;
                width: ${width}px;
                height: ${height}px;
                clip-path: polygon(${polygon});
                background-image: url('${texturePath}');
            ">
        </div>
    `;
}

function projectTowardPoint(point, target, amount) {
    return {
        x: point.x + (target.x - point.x) * amount,
        y: point.y + (target.y - point.y) * amount
    };
}

/* need a function that picks random conditions and checks that they work with each other (holy time complexity..) */

/* (maybe inside the one above) need a function that returns a list of acceptable block ids for each square */

/* need a function that actually checks if the block clicked is acceptable (if yes its placed, if no the square goes red and shakes) */

/* need a function that adds to block stats */

/* need a function that calculates US and drops durability by 1 per guess */

/* need functions that provide navigation to other parts of the website */