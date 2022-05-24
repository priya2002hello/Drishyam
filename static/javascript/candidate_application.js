console.log("application")
const seatno=document.querySelector(".seat-no")
const href=document.querySelector(".details-link")
const verify=document.querySelector(".verify")


verify.addEventListener("click",()=>{
   let value=seatno.value
   console.log(value)
   href.setAttribute('href',`/details/${value}`)
})