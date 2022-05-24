console.log("Candidate registration")


const defaultbtn=document.querySelector('#file')
const img=document.querySelector('.output-image')
const FileName=document.querySelector('.filename')
const url_img=document.querySelector('.url-img')

var socket = io.connect("http://127.0.0.1:5000");

defaultbtn.addEventListener("change",(event)=>{
   
    
    
        const reader=new FileReader();
        reader.addEventListener("load",()=>{
            const result=reader.result;
            console.log(result)
            img.src=result;
        })



        reader.readAsDataURL(event.target.files[0]);
    
    if(this.value)
    {
        let value=this.value;
        FileName.innerHTML=value
    }
})

