document.addEventListener("DOMContentLoaded", function () {
    const fileSelector = document.getElementById("file-selector");

    // Add an event listener to the file selector
    fileSelector.addEventListener("change", function (event) {
        payButton = document.getElementById("payButton");
        // TODO: receive filename, get file size in bytes from database, estimate price and update price label
        payButton.textContent = "Pay $99999"
    });
});