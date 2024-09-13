// const project2 = document.getElementById('project2');
// const errorIcon = document.getElementById('errorIcon');
// const successIcon = document.getElementById('successIcon');
const project3 = document.getElementById('project3');
const projectUrl = document.getElementById('projectUrl');
const global_scope = document.getElementById('global_scope');
const local_scope = document.getElementById('local_scope');
const rProjectName = document.getElementById('rProjectName');
const formSubmit = document.getElementById('formSubmit');
const toDeploy = document.getElementById('toDeploy');
const notDeploy = document.getElementById('notDeploy');


window.onload = ()=>{
document.getElementsByName('dataBaseScope')[0].checked = true;
}
local_scope.addEventListener('click', async () => {
  rProjectName.classList.remove("hidden");
})

global_scope.addEventListener('click', async () => {
  rProjectName.classList.add("hidden");
})
