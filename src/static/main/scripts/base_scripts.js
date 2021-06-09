var machinInfoContainer = document.getElementById("infoBar");


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
    requestData.open("post",'machineList');
    requestData.setRequestHeader("X-CSRFToken", csrf_token);
    requestData.send();

}