$(document).ready(() => {
    $("#logout-btn").on("click", function(e) {
        e.preventDefault();
        sessionStorage.removeItem("minedoku_live_session");
        console.log("Local puzzle session cache removed.")
        window.location.href = "/logout";
    } )
});