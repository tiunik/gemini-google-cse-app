import { useState, useRef, useEffect } from "react";
import ReactDOM from "react-dom/client";
import "./index.css";

const App = () => {
  const [messages, setMessages] = useState<{ text: string; sender: string }[]>([]);
  const [input, setInput] = useState("");
  const chatBoxRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
      });

      const data = await res.json();
      const botReply =
        data?.candidates?.[0]?.content?.parts?.[0]?.text || "Помилка з'єднання";
      setMessages((prev) => [...prev, { text: botReply, sender: "bot" }]);
    } catch {
      setMessages((prev) => [...prev, { text: "Помилка з'єднання", sender: "bot" }]);
    }
  };

  return (
    <div className="chat-container">
      <h1>💬 Gemini Chat</h1>
      <div className="chat-box" ref={chatBoxRef}>
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.sender}`}>
            {m.text}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Напишіть повідомлення..."
        />
        <button onClick={sendMessage}>▶</button>
      </div>
    </div>
  );
};

ReactDOM.createRoot(document.getElementById("root")!).render(<App />);
