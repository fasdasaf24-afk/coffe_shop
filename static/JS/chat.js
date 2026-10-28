document.addEventListener('DOMContentLoaded', function() {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatForm = document.getElementById('chat-form');
    const chatBody = document.getElementById('chat-body');

    if (chatToggle && chatWindow) {
        chatToggle.addEventListener('click', function() {
            chatWindow.style.display = (chatWindow.style.display === 'flex') ? 'none' : 'flex';
        });
    }

    if (chatForm) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const msgInput = document.getElementById('chat-message');
            const msg = msgInput.value;
            if(!msg.trim()) return;

            fetch('/api/support/', {
                method: 'POST',
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value},
                body: new URLSearchParams({'name': document.getElementById('chat-name').value, 'message': msg})
            }).then(response => {
                if (response.ok) {
                    const div = document.createElement('div');
                    div.className = 'chat-msg user';
                    div.textContent = msg;
                    chatBody.appendChild(div);
                    msgInput.value = '';
                    chatBody.scrollTop = chatBody.scrollHeight;
                }
            });
        });
    }
});
