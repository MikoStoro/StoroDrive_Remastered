// dragover and dragenter events need to have 'preventDefault' called
// in order for the 'drop' event to register. 
// See: https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Drag_operations#droptargets

dropContainer.addEventListener('dragover', (event) =>{
    event.preventDefault()
})
dropContainer.addEventListener('dragenter', (event) =>{
  event.preventDefault()
})
  
dropContainer.ondrop = function(evt) {
    // pretty simple -- but not for IE :(
    evt.preventDefault()
    fileInput.files = evt.dataTransfer.files;
  
    // If you want to use some of the dropped files
    const dT = new DataTransfer();
    var filenames = "";
    for(var i = 0; i < evt.dataTransfer.files.length; i++){
      dT.items.add(evt.dataTransfer.files[i])
      filenames += "<p>" + evt.dataTransfer.files[i].name  + "</p>";
    }

    document.getElementById("files_list").innerHTML = filenames;
    fileInput.files = dT.files;
  };

//requires panels.js
function resetFilesUpload(){
    document.getElementById("fileInput").value = null;

}

function closeUploadPanel(){
    hidePanel("uploadPanel");
    resetFilesUpload()
}

