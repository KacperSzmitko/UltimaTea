var recipesContainer = document.getElementById("recipesDisplay");


function loadRecipes(request_id, fetch_nexts) {
    var requestData = new XMLHttpRequest();
    requestData.responseType = "text";
    requestData.addEventListener("load", function () {
        if (requestData.status == 200) {
            console.log(requestData.response)
            recipesContainer.innerHTML = requestData.responseText
        }
        else {
            console.log('klops request response')
        }
    }, {once : true});
    requestData.open("get", window.location.href+'recipesList');
    requestData.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    requestData.send(JSON.stringify({ "starting_point": request_id, "range":fetch_nexts}));
}