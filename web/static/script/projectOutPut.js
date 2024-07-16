const container = document.getElementById("projectOutPut");
let intervalID;
let content;
let count = 0;
let interval = 2000;
let mybrake = false;

//not working
const projectLink = document.getElementById("projectUrl");
const projectMsg = document.getElementById("projectMsg");
projectLink.addEventListener("click",(event) => {
  if (this.classList.contains("mydisable")){
    event.preventDefault();
alert("aaaaa")
    projectMsg.classList.remove("hidden");
    setTimeout(() => {
      projectMsg.classList.add("hidden")
    }, 2000)
  }
})

projectLink.classList.contains("mydisable")
async function sleep(time){
    await new Promise(resolve => setTimeout(
      resolve,
      time
    ));
}

async function updateData(){
  const url = window.location.href;
  const endpoint = url + "/api1";

  await new Promise((resolve, regect) => {
  fetch(`${endpoint}`)
    .then(res => res.json())
    .then(data => {
      if (data.output === content){
        count += 1;
      }else{
        count = 0;
      }
      if (count > 30){
        mybrake = true;
      }
      content = data.output;
      container.innerHTML = content;
      if (data.building == false){
        //clearInterval(intervalID);
        mybrake = true;
        document.getElementById("loading").classList.add("hidden");
        document.getElementById("links").classList.remove("hidden");
        //return
      }

      resolve()
    })
    .catch(err => {
      console.error("an error ocured:", err)
      mybrake = true;
      regect(err)
      //clearInterval(intervalID);
    });
  });


}
/*
intervalID = setInterval(() => {
  updateData()
}, interval);
*/
//let ll = 0;
(async ()=>{
  while (!mybrake) {
    /*
    setTimeout(
      updateData
      ,
      0
      //(count < 2) ? interval : (interval * (count / 2))
    );
    */
    await updateData();
    await sleep((count < 2) ? interval : (interval * count));
    console.log((count < 2) ? interval : (interval * count));

    if (mybrake){
      break
    }
    /*
    ll += 1;
    console.log("while", ll)
    if (ll > 20){
      break
    }
    */
  }
})();
