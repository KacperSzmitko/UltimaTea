var containerId = "recipesDisplay";
var fetched_recipes = 0;
var last_fetch = 0;
var filters = {
        "recipe_name_filter" : "",
        "ingredient1_filter" : "",
        "ingredient2_filter" : "",
        "ingredient3_filter" : "",
        "brewing_temperatue_down_filter" : "",
        "brewing_time_down_filter" :"",
        "mixing_time_down_filter" :"",
        "brewing_temperatue_up_filter":"",
        "brewing_time_up_filter":"",
        "mixing_time_up_filter":"",
        "tea_type_filter": "",
}
var csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

function fetch_next(num_of_recipes_to_fetch,id_to_remove){
    var remove = false;
    if (id_to_remove > 0){
        remove = true;
    }
    var data = JSON.stringify({ 
        "fetched_recipes": fetched_recipes, 
        "num_of_recipes_to_fetch":num_of_recipes_to_fetch,
        "filters": filters,
        "last_fetch": last_fetch,
        "remove":remove,
        "id_to_remove":id_to_remove
    })

    var requestData = new XMLHttpRequest();
    requestData.responseType = "text";
    requestData.addEventListener("load", function () {
        if (requestData.status == 200) {
            document.getElementById(containerId).innerHTML = requestData.responseText;
            last_fetch = parseInt(requestData.getResponseHeader("last_fetch"));
            fetched_recipes = parseInt(requestData.getResponseHeader("fetched"));
            console.log(fetched_recipes);
            console.log(last_fetch);
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


function apply_filters(){
    if (document.getElementById("id_ing_1").value != "")
        filters["ingredient1_filter"] = document.getElementById("id_ing_1").options[document.getElementById("id_ing_1").value].text;
    else filters["ingredient1_filter"] = "";

    if (document.getElementById("id_ing_2").value != "")
        filters["ingredient2_filter"] = document.getElementById("id_ing_1").options[document.getElementById("id_ing_2").value].text;
    else filters["ingredient2_filter"] = "";

    if (document.getElementById("id_ing_3").value != "")
        filters["ingredient3_filter"] = document.getElementById("id_ing_1").options[document.getElementById("id_ing_3").value].text;
    else filters["ingredient3_filter"] = "";

    filters["recipe_name_filter"] = document.getElementById("recipe_name_filter").value;

    filters["brewing_temperatue_down_filter"] = document.getElementById("id_brewing_temperatue_down_filter").value;
    filters["brewing_time_down_filter"] = document.getElementById("id_brewing_time_down_filter").value;
    filters["mixing_time_down_filter"] = document.getElementById("id_mixing_time_down_filter").value;

    filters["brewing_temperatue_up_filter"] = document.getElementById("id_brewing_temperatue_up_filter").value;
    filters["brewing_time_up_filter"] = document.getElementById("id_brewing_time_up_filter").value;
    filters["mixing_time_up_filter"] = document.getElementById("id_mixing_time_up_filter").value;
    fetched_recipes = 0;
}

async function icons_fetches(url,recipe_id){
    return await fetch(url,{
        method:"POST",
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        },
        body:JSON.stringify({"recipe_id" : recipe_id}),
    });
}

async function add_to_favourites(element){
    let value = element.getAttribute('value');
    document.getElementById("full_hearth_ico_" + value).style.zIndex = "1";
    document.getElementById("empty_hearth_ico_" + value).style.zIndex = "0";
    const response = await icons_fetches("addToFavourites",value);
    if (!response.ok){
        console.log("favourites add error");
    }
}

async function delete_from_favourites(element){
    let value = element.getAttribute('value');
    document.getElementById("empty_hearth_ico_" + value).style.zIndex = "1";
    document.getElementById("full_hearth_ico_" + value).style.zIndex = "0";
    const response = await icons_fetches("deleteFromFavourites",value);
    if (!response.ok){
        console.log("favourites delete error");
    }
}


async function delete_recipe(element){
    let value = element.getAttribute('value');
    fetched_recipes -= last_fetch
    fetch_next(5,value);
}

function edit_recipe(element){

}

function create_recipe(){
    document.getElementById("content_to_blur").classList.add("to_blur");
    document.getElementById("content_to_blur").style.zIndex = 0;
    document.getElementById("addRecipePage").style.zIndex = 2;
    document.getElementById("addRecipePage").style.display = "flex";
}

function close_create_recipe(){
    document.getElementById("addRecipePage").zIndex = 0;
    document.getElementById("addRecipePage").style.display = "none";
    document.getElementById("content_to_blur").classList.remove("to_blur");
    document.getElementById("content_to_blur").style.zIndex = 1;
}

function submit_recipe(){
    var fields = {
        "recipe_name" : "",
        "water" : "",
        "ingredient1" : "",
        "ingredient2" : "",
        "ingredient3" : "",
        "brewing_temperatue" : "",
        "brewing_time" :"",
        "mixing_time" :"",
        "tea_type": "",
    }
    if (document.getElementById("recipe_name_create").value != "")
        fields["recipe_name"] =  document.getElementById("recipe_name_create").value
    if (document.getElementById("id_water").value != "")
        fields["water"] =  document.getElementById("id_water").value
    if (document.getElementById("id_ing_1_create").value != "")
        fields["ingredient1"] =  document.getElementById("id_ing_1_create").options[document.getElementById("id_ing_1_create").value].text;
    if (document.getElementById("id_ing_2_create").value != "")
        fields["ingredient2"] =  document.getElementById("id_ing_2_create").options[document.getElementById("id_ing_2_create").value].text;
    if (document.getElementById("id_ing_3_create").value != "")
        fields["ingredient3"] =  document.getElementById("id_ing_3_create").options[document.getElementById("id_ing_3_create").value].text;
    if (document.getElementById("tea_name_create").value != "")
        fields["tea_type"] =  document.getElementById("tea_name_create").options[document.getElementById("tea_name_create").value].text;

}