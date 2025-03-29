function sendMessage() {
    const inputField = document.getElementById("input-message");
    const chatBox = document.getElementById("chat-box");
    const responseType = document.getElementById("response-type").value; // Lấy giá trị loại phản hồi

    const inputMessage = inputField.value.trim();
    if (inputMessage === "") return;

    addMessage(inputMessage, chatBox, "user");

    const apiUrl = responseType === "predict" ? "/predict" : "/generate_answer";
    const requestBody = responseType === "predict"
        ? { input_text: inputMessage }
        : { question: inputMessage };

    // Thêm tin nhắn "AI đang suy nghĩ..."
    const loadingMessage = addMessage("AI đang suy nghĩ...", chatBox, "bot");

    fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
    })
        .then(response => response.json())
        .then(data => {
            let responseText = data.output_text || data.answer || "Không có phản hồi.";
            loadingMessage.remove(); // Xóa tin nhắn "AI đang suy nghĩ..."
            addMessage(responseText, chatBox, "bot", true);
        })
        .catch(error => {
            console.error("🔥 Fetch Error:", error);
            loadingMessage.remove();
            addMessage("🚨 Lỗi hệ thống. Vui lòng thử lại.", chatBox, "bot");
        });

    inputField.value = "";
}

function addMessage(text, chatBox, sender, isHtml = false) {

    const messageWrapper = document.createElement("div");
    messageWrapper.classList.add("message-wrapper", sender);

    const avatar = document.createElement("img");
    avatar.src = sender === "user" ? "static/images/user.png" : "static/images/logo.png";
    avatar.alt = sender === "user" ? "User" : "Bot";
    avatar.classList.add("avatar");

    const message = document.createElement("div");
    message.classList.add("message", sender);
    if (isHtml) {
        message.innerHTML = text;
    } else {
        message.textContent = text;
    }

    if (sender === "user") {
        messageWrapper.appendChild(message);
        messageWrapper.appendChild(avatar);
    } else {
        messageWrapper.appendChild(avatar);
        messageWrapper.appendChild(message);
    }

    chatBox.appendChild(messageWrapper);
    scrollToBottom();

    return messageWrapper;
}

function scrollToBottom() {
    let chatBox = document.querySelector(".chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById("clear-chat").addEventListener("click", function () {
    if (confirm("Bạn có chắc muốn xóa lịch sử trò chuyện?")) {
        document.getElementById("chat-box").innerHTML = ""; // Xóa tất cả tin nhắn
    }
});
document.getElementById("input-message").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Ngăn form bị submit mặc định (nếu có)
        sendMessage(); // Gọi hàm gửi tin nhắn
    }
});