console.log("app.js executed, turning on camera ....");

const video = document.querySelector("video");
const canvas = document.querySelector("canvas");
const pimg = document.querySelector(".face-detect-video");
const rimg=document.querySelector(".face-recognise-image");
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
const FPS = 2;

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


const begin=async()=>{

if ("mediaDevices" in navigator && navigator.mediaDevices.getUserMedia) {
    await start(constraints);
  }

   setInterval(()=>{
  
      let url=doScreenshot();
      console.log(url);
      socket.emit('detect face',url);
    
    },1000/FPS)  
  
   setInterval(()=>{
    let url=doScreenshot();
    console.log(url);
    socket.emit('rec face',url);

   },5000)
 but.onclick=()=>{

  let url=doScreenshot();
  console.log(url);
  socket.emit('rec face',url); 

};
  

socket.on('response_back', function(image){
    //console.log(image);
    pimg.setAttribute('src', image );
   
  });

socket.on('rec_face',(image)=>{
    rimg.setAttribute('src',image);
})

}

begin();