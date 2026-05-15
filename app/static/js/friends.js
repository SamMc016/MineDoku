const searchInput = document.getElementById("friend-search");
const resultsBox = document.getElementById("search-results");
const addButton = document.getElementById("add-friend-btn");
const errorMsg = document.getElementById("friend-error");
let selectedFriend = "";

const appendFriendToList = (username) => {
    const container = document.getElementById("friends-list-container");
    
    const emptyMessage = container.querySelector(".no-friends");
    if (emptyMessage) {
        emptyMessage.remove();
    }

    const div = document.createElement("div");
    div.classList.add("friend");
    div.textContent = username;
    container.appendChild(div);
};

searchInput.addEventListener("input", async () => {
    const query = searchInput.value;
    if (query.length < 2) {
        resultsBox.innerHTML = "";
        return;
    }

    const response =
        await fetch(`/api/search_friends?q=${query}`);
    const matches = await response.json();
    resultsBox.innerHTML = "";

    matches.forEach(user => {
        const div = document.createElement("div");
        div.classList.add("search-result");
        div.textContent = user;

        div.addEventListener("click", () => {
            searchInput.value = user;
            selectedFriend = user;

            resultsBox.innerHTML = "";
        });
        resultsBox.appendChild(div);
    });
});

addButton.addEventListener("click", async () => {
    if (!selectedFriend) {
        return;
    }
    errorMsg.textContent = "";
    const response = await fetch("/api/add_friend", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({friend_name: selectedFriend})
    });

    const status = await response.json();
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
});
