var containerId = "recipesDisplay";
var num_of_recipes_to_fetch = 5;
var fetched_recipes = 0;
var filters = {
        "recipe_name_filter" : "",
        "ingredient1_filter" : "",
        "ingredient2_filter" : "",
        "ingredient3_filter" : "",
        "brewing_temperatue_filter" : "",
        "brewing_time_filter" :"",
        "mixing_time_filter" :"",
}

function fetch_next(){
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var data = JSON.stringify({ 
        "fetched_recipes": fetched_recipes, 
        "num_of_recipes_to_fetch":num_of_recipes_to_fetch,
        "filters": filters,
    })

    var requestData = new XMLHttpRequest();
    requestData.responseType = "text";
    requestData.addEventListener("load", function () {
        if (requestData.status == 200) {
            document.getElementById(containerId).innerHTML = requestData.responseText;
        }
        else {
            console.log('Request error')
        }
    }, {once : true});
    requestData.open("post", 'fetchRecipesWithFilters');
    requestData.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    requestData.setRequestHeader("X-CSRFToken", csrf_token);
    requestData.send(data);

    return false;
}

function fetch_previous(){
    JSON.stringify({ "fetched_recipes": fetched_recipes, "num_of_recipes_to_fetch":5})
    return false;
}


function apply_filters(){
    if (document.getElementById("id_ing_1").value != "")
        filters["ingredient1_filter"] = document.getElementById("id_ing_1").options[document.getElementById("id_ing_1").value].text;
    if (document.getElementById("id_ing_2").value != "")
        filters["ingredient2_filter"] = document.getElementById("id_ing_1").options[document.getElementById("id_ing_2").value].text;
    if (document.getElementById("id_ing_3").value != "")
        filters["ingredient3_filter"] = document.getElementById("id_ing_1").options[document.getElementById("id_ing_3").value].text;

    filters["recipe_name_filter"] = document.getElementById("recipe_name_filter").value;
    filters["brewing_temperatue_filter"] = document.getElementById("id_brewing_temperatue_filter").value;
    filters["brewing_time_filter"] = document.getElementById("id_brewing_time_filter").value;
    filters["mixing_time_filter"] = document.getElementById("id_mixing_time_filter").value;
}

