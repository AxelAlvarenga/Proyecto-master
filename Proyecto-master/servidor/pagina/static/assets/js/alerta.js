async function notify(type,message,event){
  (()=>{
    let n = document.createElement("div");
    let id = Math.random().toString(36).substr(2,10);
    n.setAttribute("id",id);
    n.classList.add("notification",type);
    n.innerText = message;
    document.getElementById("notification-area").appendChild(n);
    document.getElementById("notification-area").style = "display:initial"
    debugger
    setTimeout(()=>{
      var notifications = document.getElementById("notification-area").getElementsByClassName("notification");
      for(let i=0;i<notifications.length;i++){
        if(notifications[i].getAttribute("id") == id){
          notifications[i].remove();
          break;
        }
      }
      event.submit()
    },2000);
  })();
}

function notifySuccess(event){
  notify("success","Se guardo correctamente", event)
}
function notifyError(event){
  notify("error","This is demo error notification message", event);
}
function notifyInfo(event){
  notify("info","This is demo info notification message", event);
}