document.getElementById("userMenu").addEventListener("click", function() {
  this.parentElement.classList.toggle("mySmallMenu");
  this.classList.toggle("border-none");
  //document.getElementByClassName("myMenuHide").forEachclassList.toggle("hidden");
  document.querySelectorAll(".myMenuHide").forEach((element)=>{ element.classList.toggle("hidden");
  });
});
