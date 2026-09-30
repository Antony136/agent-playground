import { useState } from "react";
import "./App.css";

function App() {
  const [request, setRequest] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function runAgent() {
    if (!request.trim()) {
      return;
    }

    setLoading(true);
    setAnswer("");
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/agent", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          request: request,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to communicate with the agent.");
      }

      const data = await response.json();

      setAnswer(data.answer);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1>AI Developer Agent</h1>

        <p className="subtitle">
          Ask the agent to perform a task using its available tools.
        </p>

        <textarea
          value={request}
          onChange={(event) => setRequest(event.target.value)}
          placeholder="Example: Calculate 125 multiplied by 48, then add 250."
          rows={5}
        />

        <button
          onClick={runAgent}
          disabled={loading || !request.trim()}
        >
          {loading ? "Running Agent..." : "Run Agent"}
        </button>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {answer && (
          <div className="response">
            <h2>Agent Response</h2>
            <p>{answer}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;