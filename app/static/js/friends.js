const searchInput = document.getElementById("friend-search");
const resultsBox = document.getElementById("search-results");
const addButton = document.getElementById("add-friend-btn");

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

            resultsBox.innerHTML = "";
        });
        resultsBox.appendChild(div);
    });
});

addButton.addEventListener("click", async () => {
    if (!selectedFriend) {
        return;
    }

    const response = await fetch("/add_friend", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({friend_name: selectedFriend})
    });
    if (response.ok) {
        appendFriendToList(selectedFriend);

        searchInput.value = "";
        selectedFriend = "";
        resultsBox.innerHTML = "";
    } else {
        console.error("server returned an error");
    }
});

/* 
{% for friend in friends_list %}
                <div class="friend">{{ friend.username }}</div>
            {% else %}
                <div class="friend no-friends">No Friends Added Yet!</div>
            {% endfor %}
        </div>
        */