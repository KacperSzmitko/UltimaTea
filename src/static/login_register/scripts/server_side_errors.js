

function server_error(error,id)
{
    var element = document.getElementById(id);
    element.classList.add("invalid");
    element.setCustomValidity(error);
    // Username already in use
    if (id == "id_username")
    {
        
        document.getElementById("register_form").reportValidity();
    }
    // Email already in use
    else if (id == "id_email")
    {
        document.getElementById("register_form").reportValidity();
    }
    // Wrong email or username or password
    else if (id == "id_email_or_username" || id == "log_id_password")
    {
        document.getElementById("login_form").reportValidity();
    }

    element.onclick = function() {element.classList.remove("invalid");};
    element.oninput = function() {element.classList.remove("invalid");};
  
    setTimeout( function() {element.setCustomValidity("");},3000);

}

function on_click_reset(id)
{
    var element = document.getElementById(id);
}

