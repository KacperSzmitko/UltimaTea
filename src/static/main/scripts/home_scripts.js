var recipesContainer = document.getElementById("recipesDisplay");
var machinInfoContainer = document.getElementById("infoBar");


function loadRecipes(request_id, fetch_nexts, csrf_token) {
    var requestData = new XMLHttpRequest();
    requestData.responseType = "text";
    requestData.addEventListener("load", function () {
        if (requestData.status == 200) {
            recipesContainer.innerHTML = requestData.responseText
        }
        else {
            console.log('Request error')
        }
    }, {once : true});
    requestData.open("post", window.location.href+'recipesList');
    requestData.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    requestData.setRequestHeader("X-CSRFToken", csrf_token);
    requestData.send(JSON.stringify({ "from": request_id, "range":fetch_nexts}));

}


function loadMachineInfo(csrf_token) {
    var requestData = new XMLHttpRequest();
    requestData.responseType = "text";
    requestData.addEventListener("load", function () {
        if (requestData.status == 200) {
            machinInfoContainer.innerHTML = requestData.responseText
        }
        else {
            console.log('Request error')
        }
    }, {once : true});
    requestData.open("post", window.location.href+'machineList');
    requestData.setRequestHeader("X-CSRFToken", csrf_token);
    requestData.send();

}




var toggled = undefined

function displayTotalTime(){

}


function toggle_select(name) {
    var envRow = document.getElementById(name);
    
    if(envRow.classList.contains("selected")) {
        envRow.classList.remove("selected");
        toggled = undefined
    }
    else{
        envRow.classList.add("selected");
        if(toggled != undefined){
            toggle_select(toggled)
        }
        toggled = name

    }
}