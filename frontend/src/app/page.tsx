'use client';

import { useEffect, useState } from 'react';

export default function Home() {
  const [apiMessage, setApiMessage] = useState('');
  const [wsMessage, setWsMessage] = useState('');
  const [username, setUsername] = useState('demo');

  const apiUrl = process.env.NEXT_PUBLIC_FASTAPI_URL;
  const wsUrl = process.env.NEXT_PUBLIC_FASTAPI_WS;

  useEffect(() => {
    console.log(apiUrl);
    fetch(`${apiUrl}/api/helloworld`)
      .then((res) => res.json())
      .then((data) => setApiMessage(data.message));
  }, []);

  const connectWebSocket = () => {
    console.log(wsUrl);
    const ws = new WebSocket(`${wsUrl}/ws/${username}`);
    ws.onopen = () => ws.send("Hello from frontend");
    ws.onmessage = (event) => setWsMessage(event.data);
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6 bg-gray-100 text-center">
      <h1 className="text-3xl font-bold mb-4">AIcebreaker</h1>
      <p className="mb-2">API Response: <strong>{apiMessage}</strong></p>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="p-2 border rounded mb-4"
        placeholder="username"
      />
      <button
        onClick={connectWebSocket}
        className="px-4 py-2 bg-blue-600 text-white rounded"
      >
        Connect to the WebSocket
      </button>
      <p className="mt-4 text-lg">{wsMessage}</p>
    </main>
  );
}
