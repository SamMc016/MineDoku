let durability = window.maxDurability;
let placedBlocks = [];
let currentUS = window.initialUS;

let gameCells, inventoryCells, overlay, backButton, giveUpButton, tableContainer;

document.addEventListener("DOMContentLoaded", () => {
    gameCells = document.querySelectorAll(".gameboard-cell");
    inventoryCells = document.querySelectorAll(".inventory-cell");
    overlay = document.getElementById("inventory-overlay");
    backButton = document.getElementById("backFromInventory");
    giveUpButton = document.getElementById("give-up");
    tableContainer = document.querySelector(".table");

    /* Opens inventory when a main grid cell is clicked */
    gameCells.forEach(cell => {
        cell.addEventListener("click", () => {
            if (cell.dataset.block) {
                return;
            }
            window.currentSquare = cell.id;
            overlay.classList.remove("hidden");
        });
    });
  
  /* Closes inventory when back button is clicked */
  backButton.addEventListener("click", () => {
      overlay.classList.add("hidden");
  });

  /* Clicking it or anywhere outside of the inventory drops the screen */
  overlay.addEventListener("click", (event) => {
      if (event.target === overlay) {
          overlay.classList.add("hidden");
      }
  });

  /* Goes to end game page when give up button is clicked */
  giveUpButton = document.getElementById("give-up");
  giveUpButton.addEventListener("click", () => {
      if (giveUpButton.innerText === "View Results?") {
          window.location.href = "/end_game";
      }
      else {
          endGame();
      }
  });

      /* Places selected inventory block into selected main grid cell */
      inventoryCells.forEach(cell => {
          cell.addEventListener("click", () => {
              const blockName = cell.dataset.block;
              const texturePath = cell.dataset.texture;
              const conditionCompatibility = cell.dataset.compatibility.split(",");

              const selectedGameCell = document.getElementById(window.currentSquare);

              durability--;
              updateDurability();

              const reqTop = selectedGameCell.getAttribute("data-top");
              const reqSide = selectedGameCell.getAttribute("data-side");
              const isCorrect = conditionCompatibility.includes(reqTop) && conditionCompatibility.includes(reqSide);

              if (isCorrect) {
                  const percentage = parseFloat(cell.dataset.blockPercentage) || 0;
                  currentUS = (currentUS - 100) + percentage;

                  const usDisplay = document.getElementById("us-score");
                  if (usDisplay) {
                      usDisplay.innerText = Math.round(currentUS);
                  }

                  selectedGameCell.dataset.percentage = percentage.toFixed(1) + "%";

                  selectedGameCell.dataset.block = blockName;
                  selectedGameCell.dataset.texture = texturePath;
                  selectedGameCell.innerHTML = "";

                  placedBlocks.push({
                      block_id: cell.dataset.blockId,
                      cell_id: window.currentSquare
                  })

                  renderBoard(window.currentSquare);
                  overlay.classList.add("hidden");
              } else {
                  const errorClasses = [
                      "is-error",
                      "!animate-[redFlash_1.5s_ease-in-out,shake_0.5s_ease-in-out_infinite]",
                      "!outline-red-500",
                      "!outline-4",
                      "!outline-offset-[-4px]",
                      "!border-transparent"
                  ];

                  overlay.classList.add("hidden");

                  selectedGameCell.classList.add(...errorClasses);
                  setTimeout(() => {
                      selectedGameCell.classList.remove(...errorClasses);
                  }, 1500);
              }

              if (durability <= 0) {
                  endGame();
                  return;
              }
          });
      });
});

function updateDurability() {
    const durabilityElement =
        document.getElementById("durability-score");

    if (durabilityElement) {
        durabilityElement.innerText =
            durability + "/9";
    }
}

function endGame() {
        durability = 0;
        updateDurability();

    tableContainer.classList.add("game-over-freeze");
    gameCells.forEach(cell => {
        cell.classList.add("greyed-out");
    });
    
    fetch("/finish_game", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ us_score: currentUS, chosen_blocks: placedBlocks})
    })

    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const finishButton = document.getElementById("give-up");

            finishButton.style.setProperty("background-color", "#3BB143", "important");
            finishButton.style.setProperty("border-color", "#3BB143", "important");
            finishButton.innerText = "View Results?";

            finishButton.onclick = () => {window.location.href = "/end_game"};
        }
    }) 

    .catch(error => {console.error("Error ending game:",error);
    });
}

/* UI FUNCTIONS */

function renderBoard(newlyPlacedId = null) {
    window.newlyPlacedId = newlyPlacedId;

    let sideFaceLayer = document.getElementById("side-face-layer");
    let frontFaceLayer = document.getElementById("front-face-layer");

    if (!sideFaceLayer) {
        sideFaceLayer = document.createElement("div");
        sideFaceLayer.id = "side-face-layer";
        tableContainer.appendChild(sideFaceLayer);
    }

    if (!frontFaceLayer) {
        frontFaceLayer = document.createElement("div");
        frontFaceLayer.id = "front-face-layer";
        tableContainer.appendChild(frontFaceLayer);
    }

    sideFaceLayer.innerHTML = "";
    frontFaceLayer.innerHTML = "";

    const board = document.querySelector(".table table");
    const boardRect = board.getBoundingClientRect();
    const containerRect = tableContainer.getBoundingClientRect();

    const vanishingPoint = {
        x: boardRect.left + boardRect.width / 2,
        y: boardRect.top + boardRect.height / 2
    };

    const depthAmount = 0.22;

    gameCells.forEach(cell => {
        const blockName = cell.dataset.block;
        const texturePath = cell.dataset.texture;
        const bottomTexturePath = cell.dataset.bottomTexture || texturePath;

        if (!blockName || !texturePath) {
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

        if (isLeftColumn && !hasRight) {
            sideFaceLayer.insertAdjacentHTML(
                "beforeend",
                createPerspectiveFace(cell, "right", texturePath, vanishingPoint, depthAmount, containerRect)
            );
        }

        if (isRightColumn && !hasLeft) {
            sideFaceLayer.insertAdjacentHTML(
                "beforeend",
                createPerspectiveFace(cell, "left", texturePath, vanishingPoint, depthAmount, containerRect)
            );
        }

        if (isTopRow && !hasBelow) {
            sideFaceLayer.insertAdjacentHTML(
                "beforeend",
                createPerspectiveFace(cell, "bottom", bottomTexturePath, vanishingPoint, depthAmount, containerRect)
            );
        }

        if (isBottomRow && !hasAbove) {
            sideFaceLayer.insertAdjacentHTML(
                "beforeend",
                createPerspectiveFace(cell, "top", texturePath, vanishingPoint, depthAmount, containerRect)
            );
        }

        frontFaceLayer.insertAdjacentHTML(
            "beforeend",
            createFrontFace(cell, texturePath, containerRect, cell.dataset.percentage)
        );
    });
}

function createFrontFace(cell, texturePath, containerRect, percentage) {
    const rect = cell.getBoundingClientRect();
    const left = rect.left - containerRect.left;
    const top = rect.top - containerRect.top;

    const boxHtml = percentage ?
        `<span class="percentage-box"> ${percentage}</span>`
        : '';

    return `
        <div
            class="block-face block-front rendered-block-face ${String(cell.id) === String(window.newlyPlacedId) ? 'newly-placed' : ''}"
            data-square-id="${cell.id}"
            data-block="${cell.dataset.block}"
            style="
                left: ${left}px;
                top: ${top}px;
                background-image: url('${texturePath}');

                display: flex;
                align-items: flex-end;
                justify-content: flex-end;
                padding: 8px;
                box-sizing: border-box;
            ">
            ${boxHtml}
        </div>
    `;
}

function createPerspectiveFace(cell, side, texturePath, vanishingPoint, depthAmount, containerRect) {
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
        x: point.x - containerRect.left,
        y: point.y - containerRect.top
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
            class="block-face ${className} rendered-block-face ${String(cell.id) === String(window.newlyPlacedId) ? 'newly-placed' : ''}"
            data-square-id="${cell.id}"
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
