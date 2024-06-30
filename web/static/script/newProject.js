const projectName = document.getElementById('projectName')
const project2 = document.getElementById('project2');
const project3 = document.getElementById('project3');
const projectType = document.getElementById('projectType');
const projectUrl = document.getElementById('projectUrl');
const formSubmit = document.getElementById('formSubmit');
const apiUrl = document.getElementById('apiurlnew').value;

let projectUrlValue = projectUrl.value;
let projectNameValue = projectName.value;
let projectTypeValue = projectType.value;

// let projectNameAvailable = false
let projectUrlAvailable = false

async function verifyName(name){
  try {
    const response = await fetch(`${apiUrl}/${name}/api4`);
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
    const response = await fetch(`${apiUrl}/api5/api5`, {
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
    const res = await fetch(`${apiUrl}/${type}/api3`);
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

async function updateForm(timeOut){
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
  let available = await verifyName(value);
  if (available) {
    project2.classList.remove('hidden');
  } else {
    project2.classList.add('hidden');
  }
}

// projectName.addEventListener('change', async (event) => {
projectName.addEventListener('change', projectNameEventHandler);
projectName.addEventListener('input', projectNameEventHandler);


async function projectUrlEventHandler(event){
  const value = event.target.value;
  const available = await verifyUrl(value);
  let timeOut = 0;

  if (available) {
    // implement project type checking later
    projectUrlAvailable = true;
    timeOut = 20;
  } else {
    projectUrlAvailable = false;
    timeOut = 10;
  }
  updateForm(timeOut);
}

// projectUrl.addEventListener('load', projectUrlEventHandler);
projectUrl.addEventListener('change', projectUrlEventHandler);

projectType.addEventListener('change', () => {
  updateForm(2000);
});
