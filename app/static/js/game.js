let selectedBlock = null;

let durability = 9;

let currentUS = 900;

let placedBlocks = [];

/* =========================
   INVENTORY SELECTION
========================= */

const inventoryItems =
document.querySelectorAll(".inventory-cell");

inventoryItems.forEach(item => {

    item.addEventListener("click", () => {

        selectedBlock = {

            id: item.dataset.blockId,

            name: item.dataset.blockName,

            conditions:
                item.dataset.blockConditions
                    .toLowerCase()
                    .split(","),

            image:
                item.dataset.blockImage
        };

        console.log(selectedBlock);

        inventoryItems.forEach(i =>
            i.classList.remove("selected-inventory")
        );

        item.classList.add("selected-inventory");
    });
});

/* =========================
   BOARD CELLS
========================= */

const boardCells =
document.querySelectorAll(".gameboard-cell");

boardCells.forEach(cell => {

    cell.addEventListener("click", () => {

        if (!selectedBlock) {

            alert("Select a block first.");

            return;
        }

        handleGuess(cell);
    });
});

/* =========================
   GET CONDITIONS
========================= */

function getCellConditions(cellId) {

    const topConditions = [

        document.getElementById("TLCon")
            .innerText.toLowerCase(),

        document.getElementById("TMCon")
            .innerText.toLowerCase(),

        document.getElementById("TRCon")
            .innerText.toLowerCase()
    ];

    const leftConditions = [

        document.getElementById("LTCon")
            .innerText.toLowerCase(),

        document.getElementById("LMCon")
            .innerText.toLowerCase(),

        document.getElementById("LBCon")
            .innerText.toLowerCase()
    ];

    const index = Number(cellId) - 1;

    const row = Math.floor(index / 3);

    const col = index % 3;

    return {

        topCondition: topConditions[col],

        leftCondition: leftConditions[row]
    };
}

/* =========================
   CHECK CONDITIONS
========================= */

function blockFitsConditions(
    block,
    topCondition,
    leftCondition
) {

    return (

        block.conditions.includes(topCondition)

        &&

        block.conditions.includes(leftCondition)
    );
}

/* =========================
   HANDLE GUESS
========================= */

function handleGuess(cell) {

    if (cell.classList.contains("filled-cell")) {
        return;
    }

    const cellConditions =
        getCellConditions(cell.id);

    const isCorrect =
        blockFitsConditions(

            selectedBlock,

            cellConditions.topCondition,

            cellConditions.leftCondition
        );

    durability--;

    updateDurability();

    if (isCorrect) {

        placeBlock(cell);

    } else {

        showWrong(cell);
    }

    if (durability <= 0) {

        endGame();
    }
}

/* =========================
   PLACE BLOCK
========================= */

function placeBlock(cell) {

    cell.innerHTML = "";

    const img = document.createElement("img");

    img.src = selectedBlock.image;

    img.alt = selectedBlock.name;

    cell.appendChild(img);

    placedBlocks.push({

        block_id: selectedBlock.id,

        cell_id: cell.id
    });

    cell.classList.add("filled-cell");

    inventoryItems.forEach(i =>
        i.classList.remove("selected-inventory")
    );

    selectedBlock = null;
}

/* =========================
   WRONG ANSWER
========================= */

function showWrong(cell) {

    cell.classList.add("wrong");

    setTimeout(() => {

        cell.classList.remove("wrong");

    }, 500);
}

/* =========================
   UPDATE DURABILITY
========================= */

function updateDurability() {

    const durabilityElement =
        document.getElementById("durability-score");

    if (durabilityElement) {

        durabilityElement.innerText =
            durability + "/9";
    }
}

/* =========================
   END GAME
========================= */

function endGame() {

    fetch("/finish_game", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            us_score: currentUS,

            chosen_blocks: placedBlocks
        })

    })

    .then(response => response.json())

    .then(data => {

        if (data.success) {

            window.location.href = "/end_game";
        }
    })

    .catch(error => {

        console.error(
            "Error ending game:",
            error
        );
    });
}