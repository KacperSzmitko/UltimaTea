var recipesContainer = document.getElementById("recipesDisplay");


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function loadRecipes(request_id, fetch_nexts, tocken) {
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
    requestData.setRequestHeader("X-CSRFToken", csrftoken);
    requestData.send(JSON.stringify({ "starting_point": "request_id", "range":"fetch_nexts"}));

    // requestData.send(JSON.stringify({ "starting_point": request_id, "range":fetch_nexts}));
}