var register_form = document.forms[1];
register_form.onsubmit = validate_form;
function validate_form()
{
    if (register_form["password"].classList.contains("invalid"))
    {
        reset_animation(register_form["password"]);
        register_form["password"].style.animation = "highlight 1.5s";
        return false;
    }
    else if (register_form["re_password"].classList.contains("invalid"))
    {
        reset_animation(register_form["re_password"]);
        register_form["re_password"].style.animation = "highlight 1.5s";
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