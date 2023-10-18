const USER = true;
const ASSISTANT = false;

document.addEventListener("DOMContentLoaded", function () {
    const inputField = document.getElementById("chat-input");
    const button = document.getElementById("chat-button");

    // Add an event listener to the input field
    // FIXME: Works but throws an error on a get request, but not really a problem
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
        // disabled the chatbox and the button while waiting for the response
        document.getElementById("chat-input").disabled = true;
        document.getElementById("chat-button").disabled = true;
    });
});

function addNewChatbox(text, player) {
    let chatbox = document.createElement("div");
    // add the correct classnames
    chatbox.className = "chatbox" + (player ? " user" : " assistant");
    // add the text
    chatbox.innerHTML = text;
    // add the chatbox to the chat-content
    document.getElementById('chat-content').appendChild(chatbox);
    // scroll to the bottom of the chatbox to get the form into view
    document.getElementById('chat-form').scrollIntoView();

}

function getChat() {
    let message = document.getElementById("chat-input").value;
    document.getElementById("chat-input").value = "";
    addNewChatbox(message, USER)

    // send the message to the server
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
        }).finally(() => {
        // enable the chatbox and the button again and focus on the chatbox
        document.getElementById("chat-input").disabled = false;
        document.getElementById("chat-button").disabled = false;
        document.getElementById("chat-input").focus();
    });

}
