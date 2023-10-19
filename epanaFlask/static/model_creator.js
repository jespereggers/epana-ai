document.addEventListener("DOMContentLoaded", function () {
    const fileSelector = document.getElementById("file-selector");

    // Add an event listener to the file selector
    fileSelector.addEventListener("change", function (event) {
        payButton = document.getElementById("payButton");
        // TODO: receive filename, get file size in bytes from database, estimate price and update price label
        let price = 10;
        updateButton(`Pay $${price}`);
    });
});

function updateButton(text) {
    let payButton = document.getElementById("payButton");
    payButton.textContent = text;
}