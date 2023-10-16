function addNewChatbox(text) {
    let chatbox = document.createElement("div");
    chatbox.className = "chatbox";
    chatbox.innerHTML = text;
    document.body.appendChild(chatbox);
}

function getChat() {
    let message = document.getElementById("chat-input").value;

    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({user_prompt: message})
    })
        .then(response => response.json())
        .then(data => {
            addNewChatbox(data.response);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
