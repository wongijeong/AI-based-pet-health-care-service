(function () {


  var socket = new WebSocket("ws://localhost:5000/echo");
  var form = document.getElementById("chat-form");
  var messageField = document.getElementById('chat-message');
  var diaogs = document.getElementById('chat-dialogs');
  
  let userMessages =[];  //user 메세지 저장
  let assistantMessages =[];     //chatbot 메세지 저장
  
  
  socket.onopen = function () {
    showMessage("안녕하세요! 저는 애완견 건강 상담을 담당하는 AI 상담사입니다. 무슨 도움을 드릴까요?", 'bot');
  };
  
  socket.onmessage = async function (event) { //봇 응답 출력(웹소켓으로 받았을 때)
    //백엔드 서버에 Json 보내기(파이썬의 AI한테 넘어갔다와)
    userMessages.push(event.data);//사용자 메시지 저장
    const response = await fetch("http://127.0.0.1:5000/aitell", { 
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: event.data, 
      userMessages:userMessages,
      assistantMessages:assistantMessages,        
    }),
  }); //AI 파이썬 처리 후 여기로 return, 여기를 웹소켓으로 하려면 파이썬 함수를 호출하면서 데이터 전송해야됨
  
  //응답오면 데이터 저장 후 
  const data = await response.json();
  assistantMessages.push(data); //봇 응답 저장
  text = JSON.stringify(data); //JSON -> 스트링으로
  text = text.replace(/\\n\\n/g, "");
  text = text.replace (/\"/g,'');
  text = text.replace (/\\/g,'');
  text = text.replace (/"/g,'');
  
  showMessage(text, 'bot');  //변환해서 메시지 화면에 출력
  };
  
  form.onsubmit = handleFormSubmit;
  messageField.onkeydown = handleTextareaKeyDown;
  
  
  function handleFormSubmit(event) { //사용자 메시지를 출력
    event.preventDefault();
    const message = messageField.value; //입력된 메시지 가져옴
    socket.send(message); //소켓으로 메시지 전송                            
    showMessage(message, 'user'); //유저 메시지 화면상에 출력
    messageField.value = ""; // 입력필드 크리닝
  }
  
  function handleTextareaKeyDown(event) { //키 눌림 시
    if (event.keyCode === 13 && !event.shiftKey) {
      event.preventDefault();
      handleFormSubmit(event); //챗폼 서밋처리
    }
  }
  
  function showMessage(message, speaker) {
    var label = (speaker == 'user') ? '나' : '봇';
    var dialog = document.createElement('p');
    dialog.classList.add(`chat-dialog-${speaker}`);
    dialog.classList.add('chat-dialog');
    dialog.innerHTML = `<span class="chat-speaker-${speaker} chat-speaker">${label}: </span>`;
    dialog.appendChild(document.createTextNode(message));
    diaogs.appendChild(dialog);
    window.scrollTo(0, document.body.scrollHeight);
  }
  
  
  })();
  