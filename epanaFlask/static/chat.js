const USER = true;
const ASSISTANT = false;

function addNewChatbox(text, player) {
    let chatbox = document.createElement("div");
    chatbox.className = "chatbox";
    if (player) {
        chatbox.className += " user";
    } else {
        chatbox.className += " assistant";
    }
    chatbox.innerHTML = text;
    document.getElementById('chat').appendChild(chatbox);
}

function getChat() {
    let message = document.getElementById("chat-input").value;
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
