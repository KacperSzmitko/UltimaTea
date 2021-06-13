

function send_ingredients(token){
    ingredientsContainers = document.getElementsByClassName("choose");
    var ingredients = [];
    for (var i = 0; i < ingredientsContainers.length; i++){
        console.log(ingredientsContainers[i].options[ingredientsContainers[i].selectedIndex].text)
        
        ingredients.push(ingredientsContainers[i].options[ingredientsContainers[i].selectedIndex].text)
    }
    console.log(ingredients)

    var requestData = new XMLHttpRequest();
    requestData.responseType = "text";
    requestData.addEventListener("load", function () {
        if (requestData.status == 200) {
            console.log('OK')
        }
        else {
            console.log('Request error')
        }
    }, {once : true});
    requestData.open("post", window.location.href);
    requestData.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    requestData.setRequestHeader("X-CSRFToken", token);
    requestData.send(JSON.stringify(ingredients));
}


