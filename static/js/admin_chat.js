document.addEventListener("DOMContentLoaded", function () {
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
    fetch(`/api/admin/messages/${ticketId}`)
      .then(response => response.json())
      .then(messages => {
        if (messages.length === 0) return;

        const latestMessage = messages[messages.length - 1];
        if (lastMessageId === latestMessage.id) {
          return;
        }

        // 💬 Log du nouveau message détecté (Admin)
        console.log("💬 Nouveau message détecté (Admin) :", {
          id: latestMessage.id,
          user: latestMessage.user,
          content: latestMessage.content,
          created_at: latestMessage.created_at,
          prediction: latestMessage.prediction,
          confidence: latestMessage.confidence,
          role: latestMessage.role
        });

        lastMessageId = latestMessage.id;
        chatBox.innerHTML = "";

        messages.forEach(msg => {
          const msgDiv = document.createElement("div");
          msgDiv.classList.add('chat-message');
          msgDiv.classList.add(msg.role); // 'sent' ou 'received'

          msgDiv.innerHTML = `
            <div class="chat-meta">
              <strong>${msg.user}</strong> • <span>${formatLocalDateTime(msg.created_at)}</span><br>
              <small>🤖 Sentiment : ${msg.prediction} (${msg.confidence || "?"}%)</small>
            </div>
            <div class="chat-text">${msg.content}</div>
          `;

          chatBox.appendChild(msgDiv);
        });

        chatBox.scrollTop = chatBox.scrollHeight;
      })
      .catch(error => console.error("Erreur chargement messages (admin) :", error));
  }

  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const content = messageInput.value.trim();
    if (!content) return;

    fetch(`/send_message_admin/${ticketId}`, {
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
    .catch(error => console.error("Erreur envoi message (admin) :", error));
  });

  loadMessages();
  setInterval(loadMessages, 3000);
});
