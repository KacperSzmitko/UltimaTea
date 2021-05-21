var username = document.getElementById("id_username")

username.oninput = username_check;

function username_check(){

    if (username.value.length > 0)
    {
        if (!isASCII(username.value))
        {
            username.setCustomValidity("Nazwa użytkownika nie może zawierać niedozwolonych znaków");
            username.reportValidity();
        }
        else
        {
            username.setCustomValidity("");
        }
    }
    else
    {
        username.setCustomValidity("");
    }
}

function isASCII(str) {
    return /^[\x21-\x7D]*$/.test(str);
}