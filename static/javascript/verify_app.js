console.log("app.js executed, turning on camera ....");
console.log(myVar1)
const video = document.querySelector("video");
const canvas = document.querySelector("canvas");
const pimg = document.querySelector(".face-detect-video");
const rimg = document.querySelector(".face-recognise-image");
const names = document.querySelector(".face-name");
const verify_btn = document.getElementById("verify-button");
const seatno = document.getElementById("candidate-seatno");
const candidate_status = document.querySelector(".candidate-status");
const form_alert=document.querySelector(".form-alert");
const box_face=document.getElementById("camera-box");
const box_rec_face=document.getElementById("face-rec-box");

let StreamStarted = false;
let localStream = null;
let photo =0;

let resetid;
const constraints = {
  video: {
    width: {
      min: 1280,
      ideal: 1920,
      max: 2560,
    },
    height: {
      min: 720,
      ideal: 1080,
      max: 1440,
    },
  },
};
const FPS = 2;

var socket = io.connect("http://127.0.0.1:5000");

socket.on("connect", function () {
  socket.emit("my event", { data: "I'm connected!" });
});

const turnCameraOn = async () => {
  if ("mediaDevices" in navigator && navigator.mediaDevices.getUserMedia) {
    await start(constraints);
    console.log("turning on camera");
    box_face.style.visibility="visible";
  }
};
const start = async (constraints) => {
  const stream = await navigator.mediaDevices.getUserMedia(constraints);
  video.srcObject = stream;
  localStream=stream
};

const doScreenshot = () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  let data = canvas.toDataURL("image/jpeg");

  //console.log(data)
  canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
  return data;
};

//begin => turn camera on 
const begin = async () => {
  console.log("begin executed");

  if (StreamStarted) {
    await turnCameraOn();
  } else {
    console.log("Stream not started yet");
  }
};

//stop
const stop=()=>{
      box_face.style.display = "none";      
      clearInterval(resetid);

      if (localStream != null) {
        localStream.getTracks().map(function (val) {
          val.stop();
        });
      }
}

//verify candidate
verify_btn.addEventListener("click", async() => {

  StreamStarted = true;
  await begin();
  console.log("taking snaps");
  
  //take screenshots and send to server
  resetid = setInterval(() => {
       let url = doScreenshot();
       socket.emit("detect face", url);
  }, 1000 / FPS);

});

//response back event - display face detected videos.
socket.on("response_back", function (url) {
  
  //console.log(image);
  pimg.style.visibility = "visible";
  pimg.setAttribute("src", url);

  let data_image = {
    frame: url,
    'seat_no':myVar1,
  };
  console.log(data_image)
  socket.emit("rec face", data_image);
});

//rec_face event => verify candidate and display details
socket.on("rec_face", async(data) => {

  if(data["status"]=="unavailable")
  {
    rimg.style.visibility="hidden";
    form_alert.innerHTML="Candidate unavailable ";
    
  }
  else if(data["status"]=="seatno not found" || data["status"]=="error")
  {
    rimg.style.visibility="hidden";
    form_alert.innerHTML="There was some issue ";
  }
  else
  {
    box_rec_face.style.visibility="visible"
    
    rimg.setAttribute("src", data["img_url"]);
    names.innerHTML = `Name : ${data["names"]}`;
    candidate_status.innerHTML = `Status : ${data["status"]}`;
    form_alert.innerHTML="Candidate Verification Complete"
    verify_btn.style.visibility="hidden";
    clearInterval(resetid);
    if (localStream != null) {
      await localStream.getTracks().map(function (val) {
        val.stop();
      });

    }
  }
  
});


