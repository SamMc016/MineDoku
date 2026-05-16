const todaysDate = new Date().toISOString().split("T")[0];
const square_percentages = $("#block-percentages").data("percentages");
const $game = $(".game");
const maxDurability = Number($game.data("maxDurability"));
const initialUS = Number($game.data("initialUs"));

let durability = maxDurability;
let placedBlocks = [];
let currentUS = initialUS;
let isGameOver;

let userIsLoggedIn, $gameCells, $inventoryCells, $overlay, $backButton, $giveUpButton, $tableContainer;

$(document).ready(() => {
    $tableContainer = $(".table");
    $gameCells = $(".gameboard-cell");

    if (window.location.pathname.includes("/end_game")) {
        console.log("on end game page. skipping index.js init.");
        return;
    }

    userIsLoggedIn = $("body").data("isLoggedIn") === true;
    $inventoryCells = $(".inventory-cell");
    $overlay = $("#inventory-overlay");
    $backButton = $("#backFromInventory");
    $giveUpButton = $("#give-up");

    loadPuzzleSession();

    if (durability <= 0 || isGameOver) {
        endGame();
        return;
    }

    /* Opens inventory when a main grid cell is clicked */
    $gameCells.on("click", function() {
        if (durability <= 0 || isGameOver) {
            endGame();
            return;
        }

        const $cell = $(this);
        if ($cell.data("block")) {
            return;
        }

        window.currentSquare = $cell.attr("id");
        const squareData = square_percentages[window.currentSquare] || square_percentages[Number(window.currentSquare)];

        $inventoryCells.each(function() {
            const $invCell = $(this);
            const blockId = Number($invCell.data("blockId"));
            let displayPercent = "0.0%";

            if (squareData) {
                const stat = squareData.find(s => Number(s.block_id) === blockId);
                if (stat) {
                    displayPercent = stat.percentage + "%";
                }
            }

            $invCell.find(".percentage-display").text(displayPercent);
        });

        $overlay.removeClass("hidden");
    });

    /* Closes inventory when back button is clicked */
    $backButton.on("click", () => {
        $overlay.addClass("hidden");
    });

    /* Clicking anywhere outside the inventory closes the inventory overlay */
    $overlay.on("click", (event) => {
        if ($(event.target).is($overlay)) {
            $overlay.addClass("hidden");
        }
    });

    /* Goes to end game page when give up button is clicked */
    $giveUpButton.on("click", function() {
        if ($giveUpButton.text() === "View Results?") {
            window.location.href = "/end_game";
        } else {
            endGame();
        }
    });

    /* Places selected inventory block into selected main grid cell */
    $inventoryCells.on("click", function() {
        const $invCell = $(this);
        const blockName = $invCell.data("block");
        const blockId = Number($invCell.data("blockId"));
        const texturePath = $invCell.data("texture");
        const bottomTexturePath = $invCell.data("bottomTexture") || texturePath;
        const conditionCompatibility = String($invCell.data("compatibility")).split(",");

        const $selectedGameCell = $(`#${window.currentSquare}`);

        const squareData = square_percentages[window.currentSquare] || square_percentages[Number(window.currentSquare)];
        let sPercent = 0;

        if (squareData) {
            const blockStat = squareData.find(item => Number(item.block_id) === blockId);
            sPercent = blockStat ? blockStat.percentage : 0;
        }

        durability--;
        updateDurability();

        const reqTop = $selectedGameCell.attr("data-top");
        const reqSide = $selectedGameCell.attr("data-side");
        const isCorrect = conditionCompatibility.includes(reqTop) && conditionCompatibility.includes(reqSide);

        if (isCorrect) {
            currentUS = Math.round((currentUS - 100) + sPercent);

            const $usDisplay = $("#us-score");
            if ($usDisplay.length) {
                $usDisplay.text(Math.round(currentUS));
            }

            $selectedGameCell.attr("data-percentage", sPercent.toFixed(1) + "%");
            $selectedGameCell.attr("data-block", blockName);
            $selectedGameCell.attr("data-texture", texturePath);
            $selectedGameCell.attr("data-bottom-texture", bottomTexturePath);
            $selectedGameCell.attr("data-block-id", blockId);
            $selectedGameCell.empty();

            placedBlocks.push({
                block_id: blockId,
                cell_id: window.currentSquare
            });

            handleBoardUpdate();

            renderBoard(window.currentSquare);
            $overlay.addClass("hidden");
        } else {
            const errorClasses = [
                "is-error",
                "!animate-[redFlash_1.5s_ease-in-out,shake_0.5s_ease-in-out_infinite]",
                "!outline-red-500",
                "!outline-4",
                "!outline-offset-[-4px]",
                "!border-transparent"
            ];

            $overlay.addClass("hidden");
            $selectedGameCell.addClass(errorClasses);

            setTimeout(() => {
                $selectedGameCell.removeClass(errorClasses);
            }, 1500);
        }

        if (durability <= 0 || isGameOver) {
            endGame();
            return;
        }
    });
});

function updateDurability() {
    const $durabilityElement = $("#durability-score");
    if ($durabilityElement.length) {
        $durabilityElement.text(`${durability}/9`);
    }
}

function endGame() {
    durability = 0;
    updateDurability();

    $tableContainer.addClass("game-over-freeze");
    $gameCells.addClass("greyed-out");

    $.ajax({
        url: "/api/finish_game",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ us_score: currentUS, chosen_blocks: placedBlocks }),
        success: (data) => {
            if (data.success) {
                handleBoardUpdate(true);

                $giveUpButton.attr(
                    "style",
                    "background-color: rgba(59, 177, 67, 1) !important; border-color: rgba(59, 177, 67, 1) !important;"
                );

                $giveUpButton.text("View Results?").off("click").on("click", () => {
                    window.location.href = "/end_game";
                });
            }
        },
        error: (xhr, status, error) => {
            console.error("Error ending game:", error);
        }
    });
}

function loadPuzzleSession() {
    const localSession = JSON.parse(sessionStorage.getItem("minedoku_live_session"));

    if (localSession && localSession.date === todaysDate) {
        console.log("restoring session data from local data");
        restoreBoardFromJSON(localSession.board_state);

        if (localSession.isGameOver) {
            $tableContainer.addClass("game-over-freeze");
            $gameCells.addClass("greyed-out");

            $giveUpButton.attr(
                "style",
                "background-color: rgba(59, 177, 67, 1) !important; border-color: rgba(59, 177, 67, 1) !important;"
            );

            $giveUpButton.text("View Results?").on("click", () => {
                window.location.href = "/end_game";
            });
        }

        return;
    }

    if (userIsLoggedIn) {
        $.getJSON("/api/get_game", (data) => {
            if (data.board_state && data.board_state !== "none") {
                const parsedState = JSON.parse(data.board_state);
                console.log("restoring session data from login");

                durability = Number(data.durability);
                currentUS = Number(data.us_score);

                updateDurability();

                const $usDisplay = $("#us-score");
                if ($usDisplay.length) {
                    $usDisplay.text(currentUS);
                }

                restoreBoardFromJSON(parsedState);

                if (durability <= 0 || isGameOver) {
                    endGame();
                    return;
                }

                sessionStorage.setItem("minedoku_live_session", JSON.stringify({
                    date: todaysDate,
                    board_state: parsedState,
                    isGameOver: durability <= 0
                }));
            }
        }).fail((err) => console.error("failed to get live game profile from login", err));
    }
}

function handleBoardUpdate(isGameOver = false) {
    const currentGridState = {};

    $gameCells.each(function() {
        const $cell = $(this);

        if ($cell.attr("data-block")) {
            currentGridState[$cell.attr("id")] = {
                block: $cell.attr("data-block"),
                texture: $cell.attr("data-texture"),
                bottomTexture: $cell.attr("data-bottom-texture"),
                percentage: $cell.attr("data-percentage"),
                blockId: $cell.attr("data-block-id")
            };
        }
    });

    const savePayload = {
        cells: currentGridState,
        durability: durability,
        currentUS: currentUS
    };

    const sessionPayload = {
        date: todaysDate,
        board_state: savePayload,
        isGameOver: isGameOver
    };

    sessionStorage.setItem("minedoku_live_session", JSON.stringify(sessionPayload));

    if (userIsLoggedIn) {
        $.ajax({
            url: "/api/save_game",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                board_state: JSON.stringify(currentGridState),
                durability: durability,
                us_score: currentUS
            })
        }).fail((err) => console.error("login session state save failed:", err));
    }
}

function restoreBoardFromJSON(savedData) {
    placedBlocks = [];

    if (!savedData) {
        return;
    }

    const boardState = savedData.cells ? savedData.cells : savedData;

    if (savedData.durability !== undefined) {
        durability = Number(savedData.durability);
        updateDurability();
    }

    if (savedData.currentUS !== undefined) {
        currentUS = Number(savedData.currentUS);

        const $usDisplay = $("#us-score");
        if ($usDisplay.length) {
            $usDisplay.text(Math.round(currentUS));
        }
    }

    Object.keys(boardState).forEach(cellId => {
        const cellData = boardState[cellId];
        const $cellElement = $(`#${cellId}`);

        if ($cellElement.length) {
            $cellElement.attr("data-block", cellData.block);
            $cellElement.attr("data-texture", cellData.texture);
            $cellElement.attr("data-bottom-texture", cellData.bottomTexture || cellData.texture);
            $cellElement.attr("data-percentage", cellData.percentage);
            $cellElement.attr("data-block-id", cellData.blockId);
            $cellElement.empty();

            placedBlocks.push({
                block_id: cellData.blockId,
                cell_id: cellId
            });
        }
    });

    renderBoard();
}

/* UI FUNCTIONS */

function renderBoard(newlyPlacedId = null) {
    window.newlyPlacedId = newlyPlacedId;

    $("#side-face-layer, #front-face-layer").remove();

    let $sideFaceLayer = $("#side-face-layer");
    let $frontFaceLayer = $("#front-face-layer");

    if (!$sideFaceLayer.length) {
        $sideFaceLayer = $("<div>", { id: "side-face-layer" });
        $tableContainer.append($sideFaceLayer);
    }

    if (!$frontFaceLayer.length) {
        $frontFaceLayer = $("<div>", { id: "front-face-layer" });
        $tableContainer.append($frontFaceLayer);
    }

    const $board = $(".table table");
    const $boardRect = $board[0].getBoundingClientRect();
    const containerRect = $tableContainer[0].getBoundingClientRect();
    const depthAmount = 0.22;

    const vanishingPoint = {
        x: $boardRect.left + $boardRect.width / 2,
        y: $boardRect.top + $boardRect.height / 2
    };

    $gameCells.each(function() {
        const $cell = $(this);
        const blockName = $cell.attr("data-block");
        const texturePath = $cell.attr("data-texture");
        const bottomTexturePath = $cell.attr("data-bottom-texture") || texturePath;

        if (!blockName || !texturePath) {
            return;
        }

        const id = Number($cell.attr("id"));
        const row = Math.floor((id - 1) / 3);
        const col = (id - 1) % 3;

        const isTopRow = row === 0;
        const isBottomRow = row === 2;

        const isLeftColumn = col === 0;
        const isRightColumn = col === 2;

        const hasRight = col < 2 && $(`#${id + 1}`).data("block");
        const hasLeft = col > 0 && $(`#${id - 1}`).data("block");
        const hasBelow = row < 2 && $(`#${id + 3}`).data("block");
        const hasAbove = row > 0 && $(`#${id - 3}`).data("block");

        if (isLeftColumn && !hasRight) {
            $sideFaceLayer.append(
                createPerspectiveFace($cell[0], "right", texturePath, vanishingPoint, depthAmount, containerRect)
            );
        }

        if (isRightColumn && !hasLeft) {
            $sideFaceLayer.append(
                createPerspectiveFace($cell[0], "left", texturePath, vanishingPoint, depthAmount, containerRect)
            );
        }

        if (isTopRow && !hasBelow) {
            $sideFaceLayer.append(
                createPerspectiveFace($cell[0], "bottom", bottomTexturePath, vanishingPoint, depthAmount, containerRect)
            );
        }

        if (isBottomRow && !hasAbove) {
            $sideFaceLayer.append(
                createPerspectiveFace($cell[0], "top", texturePath, vanishingPoint, depthAmount, containerRect)
            );
        }

        $frontFaceLayer.append(
            createFrontFace($cell[0], texturePath, containerRect, $cell.attr("data-percentage"))
        );
    });
}

function createFrontFace(cell, texturePath, containerRect, percentage) {
    const rect = cell.getBoundingClientRect();
    const left = rect.left - containerRect.left;
    const top = rect.top - containerRect.top;

    const $cell = $(cell);

    const boxHtml = percentage ? `<span class="percentage-box"> ${percentage}</span>` : "";

    return `
        <div
            class="block-face block-front rendered-block-face ${String($cell.attr("id")) === String(window.newlyPlacedId) ? "newly-placed" : ""}"
            data-square-id="${$cell.attr("id")}"
            data-block="${$cell.attr("data-block")}"
            style="
                left: ${left}px;
                top: ${top}px;
                background-image: url('${texturePath}');

                background-repeat: no-repeat;
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
    const $cell = $(cell);

    const corners = {
        topLeft: { x: rect.left, y: rect.top },
        topRight: { x: rect.right, y: rect.top },
        bottomRight: { x: rect.right, y: rect.bottom },
        bottomLeft: { x: rect.left, y: rect.bottom }
    };

    let edgeStart, edgeEnd, className;

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

    const points = [edgeStart, edgeEnd, projectedEnd, projectedStart];

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
            class="block-face ${className} rendered-block-face ${String($cell.attr("id")) === String(window.newlyPlacedId) ? "newly-placed" : ""}"
            data-square-id="${$cell.attr("id")}"
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

document.addEventListener("visibilitychange", function () {
    if (!document.hidden) {
        location.reload();
    }
});