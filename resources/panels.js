function showPanel(id){
    document.getElementById("smokescreen").style.display = "block";
    document.getElementById(id).style.display = "block";
}

function hidePanel(id){
    document.getElementById("smokescreen").style.display = "none";
    document.getElementById(id).style.display = "none";
}

function closeError(){
    document.getElementById('errorMessage').style.display="none";
}

let image_extensions = [ 'jpg', 'jpeg', 'gif', 'png' ]
function is_image_extension(ext){
    if(image_extensions.includes(ext.toLowerCase())){
        return true;
    }
    return false;
}

function is_pdf_extension(ext){
    if(ext.toLowerCase() == 'pdf'){
        return true;
    }
    return false;
}

let text_extensions = [ 'txt', 'json' ]
function is_text_extension(ext){
    if(text_extensions.includes(ext.toLowerCase())){
        return true;
    }
    return false;
}

function showDisplayPanel(extension, filename, location_path){
    showPanel('displayPanel');

    let displayPanel = document.getElementById('displayPanel');
    if (document.getElementById('display_content') !== null)
        document.getElementById("display_content").remove();
    let element = null;
    if(is_image_extension(extension)){
        element = document.createElement('img');
        element.classList.add('image_view');
        element.src = `download${location_path}&filename=${filename}`;
    }
    else if(is_pdf_extension(extension)){
        element = document.createElement('object');
        element.type = 'application/pdf'
        element.classList.add('pdf_view');
        element.data = `util_download${location_path}&filename=${filename}`;
    }else if(is_text_extension(extension)){
        element = document.createElement('object');
        element.classList.add('pdf_view');
        element.data = `util_download${location_path}&filename=${filename}`;
    }
    else {
        element = document.createElement('p');
        element.textContent = `Nieobsługiwany format pliku ${filename} (${extension})`
    }
    element.id = 'display_content'
    displayPanel.prepend(element);
}

function showDeletePanel(filename, href){
    showPanel('deletePanel');
    document.getElementById('sureToDeleteName').textContent=filename;
    document.getElementById('yes_delete_btn').href = href;
}



