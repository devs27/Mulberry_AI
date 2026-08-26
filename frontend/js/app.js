const API_BASE_URL = "http://localhost:8000";

async function checkHealth() {
  const statusEl = document.getElementById("status");
  try {
    const res = await fetch(`${API_BASE_URL}/api/health`);
    const data = await res.json();
    statusEl.textContent = `✅ Connected (${data.status})`;
    statusEl.className = "ok";
  } catch (err) {
    statusEl.textContent = "❌ Backend not reachable. Is it running on :8000?";
    statusEl.className = "error";
  }
}

checkHealth();
