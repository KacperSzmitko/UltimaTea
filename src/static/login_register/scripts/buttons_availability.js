var register_form = document.getElementById("register_form")
register_form.onsubmit = validate_form;
function validate_form()
{
    if (register_form["password1"].classList.contains("invalid"))
    {
        reset_animation(register_form["password1"]);
        register_form["password1"].style.animation = "highlight 1.5s";
        return false;
    }
    else if (register_form["password2"].classList.contains("invalid"))
    {
        reset_animation(register_form["password2"]);
        register_form["password2"].style.animation = "highlight 1.5s";
        return false;
    }
    return true;
}

function reset_animation(element)
{
    element.style.animation = "none";
    element.offsetHeight;
    element.style.animation = null;
}