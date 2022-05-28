//update criminal record

const video = document.querySelector("video");
const canvas = document.querySelector("canvas");
const pimg = document.querySelector(".face-detect-video");
const but = document.getElementById("update-criminal-record");
const names = document.getElementById("name");
const box=document.getElementById("camera-box");
const age=document.getElementById("age");
const place=document.getElementById("place");
const gender_male=document.getElementById("male");
const gender_female=document.getElementById("female");
const case_info=document.getElementById("case-info");


let gender;
let count = 0;
let StreamStarted = false;
let localStream = null;
let photo=false;

//set video dimensions
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

const FPS = 1;

//connect to server socketio
var socket = io.connect("http://127.0.0.1:5000");

//connect event
socket.on("connect", function () {
  socket.emit("my event", { data: "I'm connected!" });
});

//Permission to turn camera on
const turnCameraOn = async () => {
  if ("mediaDevices" in navigator && navigator.mediaDevices.getUserMedia) {
    await start(constraints);
    console.log("turning on camera");
    box.style.visibility = "visible";
  }
};

//start video stream
const start = async (constraints) => {
  const stream = await navigator.mediaDevices.getUserMedia(constraints);
  video.srcObject = stream;
  localStream = stream;
};

//take screenshots 
const doScreenshot = () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  
  //take screenshot and get url of frame
  canvas.getContext("2d").drawImage(video, 0, 0);
  let data = canvas.toDataURL("image/jpeg");

  //clear the canvas after getting url of frame
  canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
  return data;
};


//start camera only when streamstarted is set true
const begin = async () => {
  console.log("begin executed");

  if (StreamStarted) {
    await turnCameraOn();
  } 
  else {
    console.log("Stream not started yet");
  }
};


//update criminal record
but.addEventListener("click", async () => {
   console.log("button click")

   //get gender field
   if(gender_female.checked)
   {
    gender="female";
   }
   else{
     gender="male";
   }

  //turn on camera
  StreamStarted = true;
  await begin();
 
 //take continuous snaps
  const resetid=setInterval(()=>{
   
      let url=doScreenshot();
      console.log(url)

      //emit detect face event
      socket.emit("detect face",url)

      //clear interval when photo is set false
      if(photo)
      {

      box.style.display="none";
      pimg.style.display="none";
      clearInterval(resetid);
      alert("Photos clicked successfully")
     
      //turn camera off
      if (localStream!= null) {

        localStream.getTracks().map(function (val) {
        val.stop();
       
       });
       }

      }
       },1000/FPS) 
});

//response back event 
socket.on("response_back", function (url) {

  box.style.visibility="visible";
  pimg.setAttribute("src", url);
  
  //emit add criminal record event
  socket.emit('add criminal record',{
     name:names.value,
     age:age.value,
     place:place.value,
     gender:gender,
     case_info:case_info.value,
     image_url:url,
     count:count
  })
  count++;
  console.log(count)
  if(count==15)
  {
    photo=true;
    
  }
  });

count=0;

