const BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function getTodaySessions() {
  const res = await fetch(`${BASE_URL}/sessions/today`);
  if (!res.ok) throw new Error("Failed to fetch sessions");
  return res.json();
}

export async function createSession(data: any) {
  const res = await fetch(`${BASE_URL}/sessions/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error("Failed to create session");
  return res.json();
}