document.getElementById("userMenu").addEventListener("click", function() {
  this.parentElement.classList.toggle("mySmallMenu");
  this.classList.toggle("border-none");
  //document.getElementByClassName("myMenuHide").forEachclassList.toggle("hidden");
  document.querySelectorAll(".myMenuHide").forEach((element)=>{
    element.classList.toggle("hidden");
  });
  document.querySelectorAll(".myMenuHide2").forEach((element)=>{
    if (! element.classList.contains('hidden')) {
      element.classList.add('hidden');
    }
  });
  // const di = document.getElementById("dropdown-project");
  // di.classList.add("hidden")
});

function toggleHidden(Id) {
  const div = document.getElementById(Id);
  div.classList.toggle("hidden")
}
