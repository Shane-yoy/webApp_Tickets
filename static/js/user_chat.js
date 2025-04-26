document.addEventListener("DOMContentLoaded", function () {
  const myRole = "user"; // Rôle côté utilisateur
  const ticketId = document.getElementById("ticket-id").value;
  const chatBox = document.querySelector(".chat-box");
  const chatForm = document.getElementById("chat-form");
  const messageInput = document.getElementById("chat-input");

  let lastMessageId = null;

  function formatLocalDateTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString([], { hour: '2-digit', minute: '2-digit' });
  }

  function loadMessages() {
    fetch(`/api/messages/${ticketId}`)
      .then(response => response.json())
      .then(messages => {
        if (messages.length === 0) return;

        const latestMessage = messages[messages.length - 1];
        if (lastMessageId === latestMessage.id) {
          return;
        }

        console.log("💬 Nouveau message détecté :", {
          id: latestMessage.id,
          user: latestMessage.user,
          content: latestMessage.content,
          created_at: latestMessage.created_at,
          prediction: latestMessage.prediction,
          role: latestMessage.role
        });

        lastMessageId = latestMessage.id;
        chatBox.innerHTML = "";

        messages.forEach(msg => {
          const msgDiv = document.createElement("div");
          const isCurrentUserMessage = (msg.role === myRole);

          msgDiv.classList.add('chat-message');
          msgDiv.classList.add(isCurrentUserMessage ? 'sent' : 'received');

          msgDiv.innerHTML = `
            <div class="chat-meta">
              <strong>${msg.user}</strong> • <span>${formatLocalDateTime(msg.created_at)}</span>
            </div>
            <div class="chat-text">${msg.content}</div>
          `;

          chatBox.appendChild(msgDiv);
        });

        chatBox.scrollTop = chatBox.scrollHeight;
      })
      .catch(error => {
        console.error("Erreur chargement messages :", error);
      });
  }

  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const content = messageInput.value.trim();
    if (!content) return;

    fetch(`/send_message/${ticketId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Erreur lors de l\'envoi du message');
      }
      return response.json();
    })
    .then(data => {
      messageInput.value = "";
      loadMessages();
    })
    .catch(error => {
      console.error("Erreur envoi message :", error);
    });
  });

  loadMessages();
  setInterval(loadMessages, 3000);
});
