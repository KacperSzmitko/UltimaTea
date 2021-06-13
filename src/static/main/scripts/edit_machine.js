

async function send_ingredients(token){
    return new Promise((a, b)=>{
        ingredientsContainers = document.getElementsByClassName("choose");
        var ingredients = [];
        for (var i = 0; i < ingredientsContainers.length; i++){
            
            ingredients.push(ingredientsContainers[i].options[ingredientsContainers[i].selectedIndex].text)
        }

        var requestDataI = new XMLHttpRequest();
        requestDataI.responseType = "text";
        requestDataI.addEventListener("load", function () {
            if (requestDataI.status == 200) {
                console.log('OK')
                a()
            }
            else {
                console.log('Request error')
                b()
            }
        }, {once : true});
        requestDataI.open("post", window.location.href);
        requestDataI.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        requestDataI.setRequestHeader("X-CSRFToken", token);
        requestDataI.send(JSON.stringify(ingredients));
    })

    
}


