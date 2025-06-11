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

function showDisplayPanel(filename, catalogue, relative_path = null){
    showPanel('displayPanel');
    let displayPanel = document.getElementById('displayPanel');
    if (document.getElementById('display_content') !== null)
        document.getElementById("display_content").remove();
    img = document.createElement('img');
    img.classList.add('image_view');
    img.id = 'display_content'
    if (relative_path !== null)
        img.src = `download?catalogue=${catalogue}&relative_path=${relative_path}&filename=${filename}`;
    else
        img.src = `download?catalogue=${catalogue}&filename=${filename}`;
    displayPanel.prepend(img)
}

function showDeletePanel(filename, href){
    showPanel('deletePanel');
    document.getElementById('sureToDeleteName').textContent=filename;
    document.getElementById('yes_delete_btn').href = href;
}



