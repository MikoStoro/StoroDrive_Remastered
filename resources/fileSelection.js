all_files = {}
selected_files = {}

function select_all_files(){
    let state = document.getElementById("select_all_checkbox").checked;
    let inputs = document.getElementsByClassName("file_selection");
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].checked = state;
    };
    toggle_batch_panel(state);
}

function any_checkbox_checked(){
    let inputs = document.getElementsByClassName("file_selection");
    for (let i = 0; i < inputs.length; i++) {
        if(inputs[i].checked){
            return true;
        }
    };
    return false;
}

function toggle_batch_panel(value){
    if(value){
        document.getElementById("batch_panel").style.display = "block";
    }else{
        document.getElementById("batch_panel").style.display = "none";
    }
   
}

function auto_toggle_batch_panel(){
    let panel = document.getElementById("batch_panel");
    if (any_checkbox_checked()){
        panel.style.display = "block";
    }else{
        panel.style.display = "none";
    }
}

function get_row_filename(id){
    return id.substring(3);
}

function filter_files(name){
    let files = document.getElementsByClassName("file_tr");
    for (let i = 0; i < files.length; i++) {
        let filename = get_row_filename(files[i].id).toLowerCase();
        console.log(filename)
        console.log(name)
        if(filename.includes(name.toLowerCase()) || !name){ 
            files[i].style.display = "";
        }else{
            files[i].style.display = "none";
        }
    };
}