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

