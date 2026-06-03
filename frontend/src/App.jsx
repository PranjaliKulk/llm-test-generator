import { useState } from "react";
import "./App.css";

const DEFAULT_SPEC_PATH = "../data/sample_api_spec.json";

export default function App() {
  const [specPath, setSpecPath] = useState(DEFAULT_SPEC_PATH);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  async function handleGenerate() {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const res = await fetch("http://3.21.168.210:8001/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ spec_path: specPath }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || `HTTP ${res.status}`);
      }

      const data = await res.json();
      setResults(data.endpoints);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>LLM Test Generator</h1>
        <p className="subtitle">Generate test cases from an API spec</p>
      </header>

      <main className="app-main">
        <div className="input-row">
          <input
            className="spec-input"
            type="text"
            value={specPath}
            onChange={(e) => setSpecPath(e.target.value)}
            placeholder="Path to API spec file"
          />
          <button
            className="generate-btn"
            onClick={handleGenerate}
            disabled={loading || !specPath.trim()}
          >
            {loading ? "Generating…" : "Generate Tests"}
          </button>
        </div>

        {loading && (
          <div className="status-message loading">
            <span className="spinner" />
            Generating test cases…
          </div>
        )}

        {error && (
          <div className="status-message error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {results && results.length === 0 && (
          <div className="status-message">No endpoints found in spec.</div>
        )}

        {results && results.length > 0 && (
          <div className="results">
            {results.map((endpoint, i) => (
              <section key={i} className="endpoint-section">
                <div className="endpoint-header">
                  <span className="endpoint-path">{endpoint.endpoint}</span>
                </div>

                {endpoint.test_cases && endpoint.test_cases.length > 0 ? (
                  <ul className="test-list">
                    {endpoint.test_cases.map((tc, j) => (
                      <li key={j} className="test-case">
                        <div className="test-name">{tc.name}</div>
                        {tc.description && (
                          <div className="test-description">{tc.description}</div>
                        )}
                        <div className="test-meta">
                          {tc.expected_status !== undefined && (
                            <span className="badge status-badge">
                              Status: {tc.expected_status}
                            </span>
                          )}
                          {tc.expected_behavior && (
                            <span className="badge behavior-badge">
                              {tc.expected_behavior}
                            </span>
                          )}
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="no-tests">No test cases generated.</p>
                )}
              </section>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
