var recipesContainer = document.getElementById("recipesDisplay");


function loadRecipes(request_id, fetch_nexts, csrf_token) {
    var requestData = new XMLHttpRequest();
    requestData.responseType = "text";
    requestData.addEventListener("load", function () {
        if (requestData.status == 200) {
            recipesContainer.innerHTML = requestData.responseText
        }
        else {
            console.log('klops request response')
        }
    }, {once : true});
    requestData.open("post", window.location.href+'recipesList');
    requestData.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    requestData.setRequestHeader("X-CSRFToken", csrf_token);
    requestData.send(JSON.stringify({ "from": "request_id", "range":"fetch_nexts"}));

    // requestData.send(JSON.stringify({ "starting_point": request_id, "range":fetch_nexts}));
}