//navigate to candidate applications with their seat no

const seatno=document.getElementById("seat-no")
const href=document.querySelector(".details-link")
const verify=document.getElementById("verify")


verify.addEventListener("click",()=>{
   let value=seatno.value
   console.log(value)
   href.setAttribute('href',`/details/${value}`)
})