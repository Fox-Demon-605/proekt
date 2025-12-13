
const ws = new WebSocket("ws://localhost:8000/ws/chat?token=TEST&session_id=1");
const box = document.getElementById("messages");
const typing = document.getElementById("typing");
const input = document.getElementById("input");

ws.onmessage = e => {
  typing.style.display="none";
  const d = JSON.parse(e.data);
  box.innerHTML += `<div>${d.text}</div>`;
};

document.getElementById("send").onclick = send;
input.onkeydown = e => e.key==="Enter" && send();

function send(){
  if(!input.value) return;
  box.innerHTML += `<div><b>Вы:</b> ${input.value}</div>`;
  ws.send(JSON.stringify({message:input.value}));
  input.value="";
  typing.style.display="block";
}

document.getElementById("clear").onclick = ()=> box.innerHTML="";
