console.log("hello world");

const video = document.querySelector("video");
const canvas = document.querySelector("canvas");
const pimg = document.querySelector("img");
const but=document.querySelector("button")


   video.style.display = "none";
const constraints =  {
  video: {
    width: {
      min: 1280,
      ideal: 1920,
      max: 2560,
    },
    height: {
      min: 720,
      ideal: 1080,
      max: 1440
    }
  }
} ;
const FPS = 4;

 var socket = io.connect("http://127.0.0.1:5000");

 socket.on("connect", function () {

   socket.emit("my event", { data: "I'm connected!" });

 });

const start = async (constraints) => {
  const stream = await navigator.mediaDevices.getUserMedia(constraints);
  video.srcObject = stream;
  
};

const doScreenshot = () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  let data= canvas.toDataURL('image/jpeg');
  
  //console.log(data)
  canvas.getContext("2d").clearRect(0, 0,canvas.width,canvas.height);
  return data
};

  
if ("mediaDevices" in navigator && navigator.mediaDevices.getUserMedia) {
    start(constraints);
  }

  setInterval(()=>{
  
      let url=doScreenshot();
      console.log(url);
      socket.emit('image',url);
    
    },1000/FPS) 
  
/* but.onclick=()=>{

  let url=doScreenshot();
  console.log(url);
  socket.emit('image',url);
  
};
 */

socket.on('response_back', function(image){
    //console.log(image);
    pimg.setAttribute('src', image );
  });