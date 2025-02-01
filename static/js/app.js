// static/js/app.js
async function sendMessage() {
    const questionInput = document.getElementById("question");
    const question = questionInput.value.trim();
    if (!question) return;
    
    appendMessage("user", question);
    questionInput.value = "";
  
    try {
      const response = await fetch("/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
      });
      const data = await response.json();
      appendMessage("lola", data.answer);
    } catch (error) {
      appendMessage("lola", "Error: Could not retrieve an answer.");
      console.error(error);
    }
  }
  
  async function sendVoiceMessage() {
    const questionInput = document.getElementById("question");
    const question = questionInput.value.trim();
    if (!question) return;
    
    appendMessage("user", question);
    questionInput.value = "";
  
    try {
      const response = await fetch("/ask_voice", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
      });
      // Expecting audio/wav response
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
      // Optionally, also display the text answer by calling /ask
      const textResponse = await fetch("/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
      });
      const textData = await textResponse.json();
      appendMessage("lola", textData.answer);
    } catch (error) {
      appendMessage("lola", "Error: Could not retrieve a voice answer.");
      console.error(error);
    }
  }
  
  function appendMessage(sender, text) {
    const chatDiv = document.getElementById("chat");
    const messageDiv = document.createElement("div");
    messageDiv.className = "message " + sender;
    messageDiv.innerText = sender === "user" ? "You: " + text : "Lola: " + text;
    chatDiv.appendChild(messageDiv);
    chatDiv.scrollTop = chatDiv.scrollHeight;
  }
  