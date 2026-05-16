/* Friends Page Logic */

/* Input field for searching users */
const searchInput = document.getElementById("friend-search");

/* Container that displays matching usernames */
const resultsBox = document.getElementById("search-results");

/* Add friend button */
const addButton = document.getElementById("add-friend-btn");


/* Live Search */

searchInput.addEventListener("input", async () => {

    const query = searchInput.value.trim();

    if (query.length < 2) {
        resultsBox.innerHTML = "";
        return;
    }

    try {

        const response =
            await fetch(`/search_friends?q=${query}`);

        const matches = await response.json();

        displayResults(matches);

    } catch (error) {

        console.error("Search error:", error);
    }
});


/* Display Results */

function displayResults(matches) {

    resultsBox.innerHTML = "";

    matches.forEach(username => {

        const result = document.createElement("div");

        result.className = "search-result";

        result.textContent = username;

        /* Clicking autofills search bar */
        result.addEventListener("click", () => {

            searchInput.value = username;

            resultsBox.innerHTML = "";
        });

        resultsBox.appendChild(result);
    });
}


/* Add Friend */

addButton.addEventListener("click", async () => {

    const friendName = searchInput.value.trim();

    if (!friendName) return;

    try {

        const response = await fetch("/add_friend", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                friend_name: friendName
            })
        });

        const result = await response.json();

        if (result.success) {

            location.reload();

        } else {

            alert(result.error || "Could not add friend");
        }

    } catch (error) {

        console.error("Add friend error:", error);
    }
});