/* Friends Page Logic */

/* Search input field */
const searchInput =
    document.getElementById("friend-search");

/* Container for live search results */
const resultsBox =
    document.getElementById("search-results");

/* Add friend button */
const addButton =
    document.getElementById("add-friend-btn");

/* Error message container */
const errorMsg =
    document.getElementById("friend-error");


/* Global variables */

/* Stores the selected username */
let selectedFriend = "";


/* Friend is added to friends list */

const appendFriendToList = (username) => {

    const container =
        document.getElementById("friends-list-container");

    /* Remove empty placeholder message */
    const emptyMessage =
        container.querySelector(".no-friends");

    if (emptyMessage) {
        emptyMessage.remove();
    }

    /* Create new friend element */
    const friendDiv =
        document.createElement("div");

    friendDiv.classList.add("friend");
    friendDiv.textContent = username;
    container.appendChild(friendDiv);
};


/* Live Friend Search */

searchInput.addEventListener("input", async () => {

    /* Current search text */
    const query = searchInput.value.trim();

    /* Clear results if query too short */
    if (query.length < 2) {

        resultsBox.innerHTML = "";

        return;
    }

    try {

        /* Search matching usernames */
        const response =
            await fetch(`/api/search_friends?q=${query}`);

        const matches =
            await response.json();
        resultsBox.innerHTML = "";

        /* Display matching usernames */
        matches.forEach(user => {

            const resultDiv =
                document.createElement("div");
            
            resultDiv.classList.add("search-result");
            resultDiv.textContent = user;
            resultDiv.addEventListener("click", () => {

                searchInput.value = user;

                selectedFriend = user;

                resultsBox.innerHTML = "";
            });

            resultsBox.appendChild(resultDiv);
        });

    } catch (error) {

        console.error("Search error:", error);
    }
});


/* Add Friend Button */

addButton.addEventListener("click", async () => {

    /* Stop if no friend selected */
    if (!selectedFriend) return;

    /* Clear previous errors */
    errorMsg.textContent = "";

    try {

        /* Send add friend request */
        const response = await fetch("/api/add_friend", {

            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                friend_name: selectedFriend
            })
        });

        const status = await response.json();

        /* Friend successfully added */
        if (response.ok && status.success) {

            appendFriendToList(selectedFriend);
            searchInput.value = "";
            selectedFriend = "";
            resultsBox.innerHTML = "";

        } else {
            if (status.error) {

                errorMsg.textContent = status.error;
            }
        }

    } catch (error) {

        console.error("Add friend error:", error);
    }
});
