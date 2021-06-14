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
var options = {};
var edit = false;
var edit_recipe_id = 0;

// id_to_remove = 0 means no delete
function fetch_next(num_of_recipes_to_fetch,id_to_remove,page){
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
    let url = ""
    if (page == "edit"){
        url = "fetchRecipesWithFilters";
    }
    else if(page =="browse"){
        url = "browseFetchRecipesWithFilters";
    }
    else{
        return false;
    }
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
    requestData.open("post", url);
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

    if (document.getElementById("tea_name_filter").value != "")
        filters["tea_type_filter"] = document.getElementById("tea_name_filter").options[document.getElementById("tea_name_filter").value].text;
    else filters["tea_type_filter"] = "";

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
    //fetched_recipes -= last_fetch
    fetch_next(5,value,'edit');
}

function load_options(){
    var options_list = document.getElementById("id_ing_1").options;
    for (let j=0;j<options_list.length;j++){
        options[options_list[j].textContent.trim()] = j;
    }
    var options_list = document.getElementById("tea_name_filter").options;
    for (let j=0;j<options_list.length;j++){
        options[options_list[j].textContent.trim()] = j;
    }
}


function edit_recipe(element){
    edit = true;
    var recipe_id = element.getAttribute('value');
    edit_recipe_id = recipe_id;
    var ig_names = document.getElementsByClassName("igName_" + recipe_id);
    var ig_values = document.getElementsByClassName("igQuan_" + recipe_id);
    document.getElementById("recipe_name_create").value = document.getElementById("teaName_" + recipe_id).textContent.trim();
    

    var tea_type = ig_names[0].textContent.trim();
    document.getElementById("tea_name_create").value = options[tea_type];
    document.getElementById("id_tea_quan").value = ig_values[0].getAttribute('value');

    var water = parseInt(ig_values[1].getAttribute('value'));
    document.getElementById("id_water").value = water;

    for(var i=2;i<ig_names.length;i++){
        if (i>=5){
            break;
        }
        var name = ig_names[i].textContent.trim();
        let k = i - 1;
        document.getElementById("id_ing_" + k + "_create").value = options[name];
        document.getElementById("id_ing" + k + "_ammount").value = ig_values[i].getAttribute('value');
    }

    var temp_ammounts = document.getElementsByClassName("tempAm_" + recipe_id);
    document.getElementById("id_brewing_temperature").value = temp_ammounts[0].getAttribute('value');

    var tim_ammounts = document.getElementsByClassName("timAm_" + recipe_id);
    var tim_names = document.getElementsByClassName("timName_" + recipe_id);

    for(let i=0;i<tim_ammounts.length;i++){
        let name = tim_names[i].innerHTML.trim();
        if(name == 'Parzenie'){
            document.getElementById("id_brewing_time").value = tim_ammounts[i].getAttribute('value');
        }
        else{
            document.getElementById("id_mixing_time").value = tim_ammounts[i].getAttribute('value');
        }
    }
    create_recipe();
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
    document.getElementById("create_recipe_id").reset();
    edit = false;
}

async function submit_recipe(form){
    const data = new FormData(form);
    var value = Object.fromEntries(data.entries());
    value['edit'] = edit;
    value['recipe_id'] = edit_recipe_id;
    const response = await fetch('createRecipe',{
        method:"POST",
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        },
        body:JSON.stringify(value),
    });
    if (response.ok){
        console.log("Utworzono przepis");
        fetched_recipes -= last_fetch;
        fetch_next(5,0,'edit');
    }
    else{
        console.log("Nie udało się utworyć przepisu");
    }
}

async function copy(element){
    let value = element.getAttribute('value');
    document.getElementById("empty_hearth_ico_" + value).style.zIndex = "0";
    document.getElementById("full_hearth_ico_" + value).style.zIndex = "1";
    const response = await icons_fetches("copyRecipe",value);
    if (!response.ok){
        console.log("favourites delete error");
    }
}

async function delete_copy(element){
    let value = element.getAttribute('value');
    document.getElementById("empty_hearth_ico_" + value).style.zIndex = "1";
    document.getElementById("full_hearth_ico_" + value).style.zIndex = "0";
    const response = await icons_fetches("deleteCopiedRecipe",value);
    if (!response.ok){
        console.log("favourites delete error");
    }
}