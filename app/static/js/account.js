/* Logout button logic */

/* Handles logout button */
$(document).ready(() => {
    $("#logout-btn").on("click", function(e) {
        e.preventDefault();
        /* Remove saved live game session */
        sessionStorage.removeItem(
            "minedoku_live_session"
        );
        console.log(
            "Local puzzle session cache removed."
        );
        /* Redirect user to logout route */
        window.location.href = "/logout";
    });
});