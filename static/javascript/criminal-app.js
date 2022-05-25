console.log("update criminal record");

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

var socket = io.connect("http://127.0.0.1:5000");

socket.on("connect", function () {
  socket.emit("my event", { data: "I'm connected!" });
});

const turnCameraOn = async () => {
  if ("mediaDevices" in navigator && navigator.mediaDevices.getUserMedia) {
    await start(constraints);
    console.log("turning on camera");
    box.style.visibility = "visible";
  }
};
const start = async (constraints) => {
  const stream = await navigator.mediaDevices.getUserMedia(constraints);
  video.srcObject = stream;
  localStream = stream;
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

const begin = async () => {
  console.log("begin executed");

  if (StreamStarted) {
    await turnCameraOn();
  } 
  else {
    console.log("Stream not started yet");
  }
};

but.addEventListener("click", async () => {
   console.log("button click")
   if(gender_female.checked)
   {
    gender="female";
   }
   else{
     gender="male";
   }
   console.log({
     name:names.value,
     age:age.value,
     place:place.value,
     gender:gender,
     case_info:case_info.value
   })
  StreamStarted = true;
  await begin();
  console.log("taking snaps");

  const resetid=setInterval(()=>{
   
      let url=doScreenshot();
      console.log(url)
      socket.emit("detect face",url)
      if(photo)
      {

      box.style.display="none";
      pimg.style.display="none";
      clearInterval(resetid);
      alert("Criminal Record Saved Successfully")
     
      
      if (localStream!= null) {

        localStream.getTracks().map(function (val) {
        val.stop();
       
       });
       }

       
      }
       },1000/FPS) 
  console.log("Set Interval finished")
});

socket.on("response_back", function (url) {
  //console.log(image);
  box.style.visibility="visible";
  pimg.setAttribute("src", url);
  let name1=names.value
  console.log(url,name1);
  socket.emit('update criminal record',{
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

