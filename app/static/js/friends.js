const searchInput = document.getElementById("friend-search");
const resultsBox = document.getElementById("search-results");
const addButton = document.getElementById("add-friend-btn");

let selectedFriend = "";

searchInput.addEventListener("input", async () => {
    const query = searchInput.value;
    if (query.length < 2) {
        resultsBox.innerHTML = "";
        return;
    }

    const response =
        await fetch(`/search_friends?q=${query}`);
    const matches = await response.json();
    resultsBox.innerHTML = "";

    matches.forEach(user => {
        const div = document.createElement("div");
        div.classList.add("search-result");
        div.textContent = user;

        div.addEventListener("click", () => {
            searchInput.value = user;
            selectedFriend = user;
        });
        resultsBox.appendChild(div);
    });
});

addButton.addEventListener("click", async () => {
    if (!selectedFriend) {
        return;
    }

    await fetch("/add_friend", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({friend_name: selectedFriend})
    });
    location.reload();
});