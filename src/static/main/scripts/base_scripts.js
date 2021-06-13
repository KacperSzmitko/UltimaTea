var machinInfoContainer = document.getElementById("infoBar");


async function loadMachineInfo(csrf_token) {
    console.log('asd')
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