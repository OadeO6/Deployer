const projectName = document.getElementById('projectName')
// const project2 = document.getElementById('project2');
// const errorIcon = document.getElementById('errorIcon');
// const successIcon = document.getElementById('successIcon');
const project3 = document.getElementById('project3');
const projectType = document.getElementById('projectType');
const projectUrl = document.getElementById('projectUrl');
const formSubmit = document.getElementById('formSubmit');
const toDeploy = document.getElementById('toDeploy');
const notDeploy = document.getElementById('notDeploy');
const production = document.getElementById('production');
const development = document.getElementById('development');
const section1 = document.getElementById('section1');
const apiUrl = document.getElementById('apiurlnew');
const more = document.getElementById('more');
console.log(more, "sssss")
const env_vars = document.getElementById('env-vars');

let projectUrlValue = projectUrl.value;
let projectNameValue = projectName.value;
let projectTypeValue = projectType.value;

// let projectNameAvailable = false
let projectUrlAvailable = false

async function verifyName(name){
  try {
    const response = await fetch(`${apiUrl.value}/${name}/api4`);
    if (response.status === 200) {
      let data = await response.json()
      data = data.data;
      if (data) return true;
      else return false;
    } else return false;
  } catch (error) {
    console.error(error)
    return false
  }
}

async function verifyUrl(repoUrl){
  try {
    let repo = encodeURIComponent(repoUrl)
    const response = await fetch(`${apiUrl.value}/api5/api5`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ repo_url: repo })
    });
    if (response.status === 200) {
      let data = await response.json()
      data = data.data;
      console.log(data)
      if (data) return true;
      else return false;
    } else return false;
  } catch (error) {
    console.error(error)
    return false
  }
}

// async function verifyUrl(repo){
//   const apiUrl = `https://api.github.com/repos/${repo}`;
//
//   try {
//     const response = await fetch(apiUrl, {
//       method: 'GET',
//       headers: {
//         'Accept': 'application/vnd.github.v3+json'
//       }
//     });
//     if (response.status === 200) {
//       return true;
//     } else {
//       return false;
//     }
//   } catch (error) {
//     console.error('TheError: ', error)
//     return false;
//   }
// }


async function getRemainingForm(type){
  let data = null;
  try {
    const res = await fetch(`${apiUrl.value}/${type}/api3`);
    if (res.status === 200) {
      data = await  res.json();
      console.log(data, "data")
      data = data.data
      return data;
    } else {
      return data;
    }
  } catch (error) {
    console.error(error);
    return data
  }
}

async function OldUpdateForm(timeOut){
  setTimeout(() => {
    if (projectUrlAvailable) {
      project3.hidden = false;
    } else {
      project3.hidden = true;
    }

    projectTypeValue = projectType.value;
    console.log(projectType.value)
    if (projectTypeValue) {
      htmlData = getRemainingForm(projectTypeValue);
      htmlData.then((data) => {
        console.log(data, 9)
        if (data) project3.innerHTML = data;
        else project3.innerHTML = "";
      });
    } else {
      project3.innerHTML = "";
    }
  }, timeOut);
}

async function projectNameEventHandler(event){
  const value = event.target.value;
  const errorIcon = projectName.parentElement.getElementsByClassName("errorIcon")[0];
  const successIcon = projectName.parentElement.getElementsByClassName("successIcon")[0];
  console.log(1111)
  let available = value ? await verifyName(value) : false ;
  if (available) {
    errorIcon.classList.add('hidden');
    successIcon.classList.remove('hidden');
  } else {
    errorIcon.classList.remove('hidden');
    successIcon.classList.add('hidden');
  }
}

// projectName.addEventListener('change', async (event) => {
projectName.addEventListener('change', projectNameEventHandler);
projectName.addEventListener('input', projectNameEventHandler);

toDeploy.addEventListener('click', async () => {
  section1.classList.remove("hidden");
  formSubmit.children[0].value = "Deploy Project";
})

notDeploy.addEventListener('click', async () => {
  section1.classList.add("hidden");
  formSubmit.children[0].value = "Create Project";
})

production.addEventListener('click', async () => {
  document.querySelectorAll('.production').forEach((el)=>{
    el.classList.remove('hidden')
  })
})

development.addEventListener('click', async () => {
  document.querySelectorAll('.production').forEach((el)=>{
    el.classList.add('hidden')
  })
})

async function projectUrlEventHandler(event){
  const value = event.target.value;
  const available = await verifyUrl(value);
  const errorIcon = projectUrl.parentElement.getElementsByClassName("errorIcon")[0];
  const successIcon = projectUrl.parentElement.getElementsByClassName("successIcon")[0];
  let timeOut = 0;

  if (available) {
    // implement project type checking later
    projectUrlAvailable = true; // to be removed
    timeOut = 20;
    errorIcon.classList.add('hidden');
    successIcon.classList.remove('hidden');
  } else {
    projectUrlAvailable = false;
    timeOut = 10;
    errorIcon.classList.remove('hidden');
    successIcon.classList.add('hidden');
  }
  updateForm(timeOut);
}

// projectUrl.addEventListener('load', projectUrlEventHandler);
projectUrl.addEventListener('change', projectUrlEventHandler);


	const installCommand = document.getElementById('installCommand');
async function updateForm(){
	const buildCommandContainer = document.getElementById("buildCommandContainer");
	const server = document.getElementById("webServerContainer");
	const buildCommand = document.getElementById('buildCommand');
	const deployCommand = document.getElementById('deployCommand');
	const installCommand = document.getElementById('installCommand');
    projectTypeValue = projectType.value;
    console.log(projectType.value)
	let needBuild = ["Next", "Node", "React", "Javascript"]
	if (needBuild.includes(projectTypeValue)){
		// add build form
    buildCommandContainer.classList.remove('hidden');
    server.classList.add('hidden');
			deployCommand.placeholder = "npm run dev"
			deployCommand.parentElement.querySelector('.info').innerText = "npm run dev"
			installCommand.placeholder = "npm install"
			installCommand.parentElement.querySelector('.info').innerText = "npm install"
			buildCommand.placeholder = "npm run build"
			buildCommand.parentElement.querySelector('.info').innerText = "npm run build"
	} else {
		// add server form
    server.classList.remove('hidden');
   buildCommandContainer.classList.add('hidden');
			installCommand.placeholder = "pip install requirements.txt"
			installCommand.parentElement.querySelector('.info').innerText = "pip install requirements.txt"

	}
	switch (projectTypeValue) {
		case "Flask":

			deployCommand.placeholder = "python -m flask run"
			deployCommand.parentElement.querySelector('.info').innerText = "python -m flask run"
			break;
		case "Python":
			deployCommand.placeholder = "python -m flask run"
			deployCommand.parentElement.querySelector('.info').innerText = "python -m flask run"


			break;
		case "Django":
			deployCommand.placeholder = "python manage.py runserver"

			deployCommand.parentElement.querySelector('.info').innerText = "python manage.py runserver"


			break;
	}

}

projectType.addEventListener('change', () => {
  updateForm();
});


let envCount = 1
const items = document.getElementById("items");
const items0 = document.getElementById("items-0").parentElement;
const envKey = document.getElementById("envKey");
const envValue = document.getElementById("envValue");
const envTemplate = items0.outerHTML;
more.addEventListener('click', () => {

	if (envKey.value && envValue.value) {
		let bb = envTemplate.replaceAll('items-0', `items-${++envCount}`)
		bb = bb.replace(' hidden ', '')
		items.insertAdjacentHTML('beforeend', bb)
		let temp = document.getElementById(`items-${envCount}`)
		let temp2 = document.getElementById(`items-${envCount}-label`)
		temp.value = envKey.value + '=' + envValue.value
		temp2.innerHTML = `<b>${envKey.value}=${envValue.value}</b>`
		envKey.value = ''
		envValue.value = ''
	}
//	console.log(11111111);
//  const keyF = document.createElement('input');
//  keyF.type = 'text';
//  keyF.name = 'key';
//  keyF.placeholder = 'key';
//
//  const valueF = document.createElement('input');
//  valueF.type = 'text';
//  valueF.name = 'value';
//  valueF.placeholder = 'value';
//
//  env_vars.appendChild(keyF);
//  env_vars.appendChild(valueF);
})

