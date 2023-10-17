const USER = true;
const ASSISTANT = false;

document.addEventListener("DOMContentLoaded", function () {
    const inputField = document.getElementById("chat-input");
    const button = document.getElementById("chat-button");

    // Add an event listener to the input field
    inputField.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            // Prevent the form from submitting (if inside a form)
            event.preventDefault();

            // Trigger the button's click event
            button.click();
        }
    });

    // Handle button click
    button.addEventListener("click", function () {
        getChat(); // Call the getChat() function when the button is clicked
    });
});

function addNewChatbox(text, player) {
    let chatbox = document.createElement("div");
    chatbox.className = "chatbox";
    if (player) {
        chatbox.className += " user";
    } else {
        chatbox.className += " assistant";
    }
    chatbox.innerHTML = text;
    document.getElementById('chat-content').appendChild(chatbox);

}

function getChat() {
    let message = document.getElementById("chat-input").value;
    document.getElementById("chat-input").value = "";
    document.getElementById("chat-input").focus();
    addNewChatbox(message, USER)


    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({user_prompt: message})
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data.response);
            addNewChatbox(data.response, ASSISTANT);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
