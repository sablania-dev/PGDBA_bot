async function sendMessage(query) {
  let res = await fetch(`https://yourserver.com/chat?query=${encodeURIComponent(query)}`);
  let data = await res.json();
  document.getElementById("chat-output").innerText = data.answer;
}
