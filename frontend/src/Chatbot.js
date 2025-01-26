import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Chatbot() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const navigate = useNavigate();

  // Handle logout and redirect to login
  const handleLogout = () => {
    localStorage.removeItem("token"); // Clear token from localStorage
    navigate("/login"); // Redirect to login page
  };

  // Helper function to check if a value is an object
  const isObject = (value) => {
    return value && typeof value === "object" && !Array.isArray(value);
  };

  // Helper component to render tables from arrays of objects
  const DataTable = ({ data }) => {
    if (!Array.isArray(data) || data.length === 0) return null;

    // Extract table headers from keys of the first object
    const headers = Object.keys(data[0]);

    return (
      <table className="min-w-full bg-white border rounded-lg overflow-hidden">
        <thead>
          <tr>
            {headers.map((header, idx) => (
              <th
                key={idx}
                className="py-2 px-4 border-b bg-blue-200 text-left text-sm font-semibold text-gray-800"
              >
                {header.charAt(0).toUpperCase() + header.slice(1)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item, rowIdx) => (
            <tr key={rowIdx} className="hover:bg-blue-50">
              {headers.map((header, colIdx) => (
                <td
                  key={colIdx}
                  className="py-2 px-4 border-b text-sm text-gray-700"
                >
                  {item[header]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  // Helper component to render comparison objects
  const ComparisonTable = ({ data }) => {
    if (!isObject(data)) return null;

    const keys = Object.keys(data);
    if (keys.length !== 2) return null; // Assuming comparison between two items

    const itemA = data[keys[0]];
    const itemB = data[keys[1]];

    const allKeys = Array.from(
      new Set([...Object.keys(itemA), ...Object.keys(itemB)])
    );

    return (
      <table className="min-w-full bg-white border rounded-lg overflow-hidden">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b bg-blue-200 text-left text-sm font-semibold text-gray-800">
              Feature
            </th>
            <th className="py-2 px-4 border-b bg-blue-200 text-left text-sm font-semibold text-gray-800">
              {keys[0]}
            </th>
            <th className="py-2 px-4 border-b bg-blue-200 text-left text-sm font-semibold text-gray-800">
              {keys[1]}
            </th>
          </tr>
        </thead>
        <tbody>
          {allKeys.map((key, idx) => (
            <tr key={idx} className="hover:bg-blue-50">
              <td className="py-2 px-4 border-b text-sm text-gray-700">
                {key.charAt(0).toUpperCase() + key.slice(1)}
              </td>
              <td className="py-2 px-4 border-b text-sm text-gray-700">
                {itemA[key] || "N/A"}
              </td>
              <td className="py-2 px-4 border-b text-sm text-gray-700">
                {itemB[key] || "N/A"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  // Helper function to render bot messages
  const renderBotMessage = (message) => {
    const { text } = message;

    if (typeof text === "object") {
      if (Array.isArray(text)) {
        if (text.length > 0 && "price" in text[0]) {
          return <DataTable data={text} />;
        } else if (text.length > 0 && "contact_info" in text[0]) {
          return <DataTable data={text} />;
        } else {
          return <DataTable data={text} />;
        }
      } else {
        return <ComparisonTable data={text} />;
      }
    } else {
      return <span>{text}</span>;
    }
  };

  // Handle message sending
  const handleSend = async () => {
    if (!query.trim()) return;

    const userMessage = { sender: "user", text: query };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const token = localStorage.getItem("token"); // Get the token from localStorage
      const response = await axios.post(
        "http://127.0.0.1:8000/api/chat",
        null,
        {
          params: { query },
          headers: { Authorization: `Bearer ${token}` }, // Include the token in headers
        }
      );

      const botMessage = { sender: "bot", text: response.data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error: Unable to fetch a response." },
      ]);
    } finally {
      setQuery("");
    }
  };

  return (
    <div
      className="min-h-screen flex flex-col items-center py-6"
      style={{
        background: "linear-gradient(to bottom right, #3B1E54, #2575fc)",
      }}
    >
      <header className="bg-[#9B7EBD] w-full max-w-4xl p-4 rounded-lg flex justify-between items-center shadow-lg">
        <h1 className="text-xl font-bold text-black">AI Powered ChatBot</h1>
        <button
          onClick={handleLogout}
          className="text-black font-bold hover:underline"
        >
          Logout
        </button>
      </header>
      <main className="bg-white w-full max-w-4xl mt-6 rounded-lg shadow-lg p-6">
        <div className="text-center mb-4">
          <h2 className="text-2xl font-semibold text-gray-800">
            Start chatting
          </h2>
          <p className="text-sm text-gray-600">
            This chatbot is configured to answer your about Products & Suppliers
          </p>
        </div>
        <div className="h-72 overflow-y-auto mb-6 border rounded-lg bg-gray-50 p-4 shadow-inner">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`mb-4 ${
                msg.sender === "user"
                  ? "text-right text-blue-600"
                  : "text-left text-green-600"
              }`}
            >
              <strong>{msg.sender.toUpperCase()}:</strong>
              {msg.sender === "bot" ? (
                <div className="mt-1">{renderBotMessage(msg)}</div>
              ) : (
                <span className="ml-2">{msg.text}</span>
              )}
            </div>
          ))}
        </div>
        <div className="flex items-center">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-grow border rounded-l px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type a new question..."
          />
          <button
            onClick={handleSend}
            className="bg-blue-500 text-white px-6 py-2 rounded-r hover:bg-blue-600 focus:outline-none"
            style={{ marginLeft: "12px" }} // Add space between input and button
          >
            Send
          </button>
        </div>
      </main>
    </div>
  );
}

export default Chatbot;
