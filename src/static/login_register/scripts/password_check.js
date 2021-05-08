var password_input = document.getElementsByClassName("register-password").item(0);
var password_error = document.getElementById("e_pass")

var re_password_input = document.getElementById("id_re_password");
var re_password_error = document.getElementById("e_repass")

re_password_input.oninput = check_re_passwd;
password_input.oninput = check_passwd;

function check_passwd() {
    if (password_input.value.length!= 0 && password_input.value.match("(?=.*[?!.!\"#%&'()*+,\-\./:<>=?@\\[\\]\^_{}|~$])(?=.*[A-Z]).{8,255}") == null)
    {
        if (password_input.classList.contains("valid")) password_input.classList.replace("valid", "invalid")
        else password_input.classList.replace("log-in","invalid");
        password_error.innerHTML = "Hasło powinno składać się z min. 8 znaków,1 znaku specjalnego,1 liczby oraz 1 wielkiej lietry";
    }
    else if(password_input.value.length == 0)
    {
        if (password_input.classList.contains("invalid"))
            password_input.classList.replace("invalid","log-in");
        password_error.innerHTML = "";
    }
    else
    {
        password_input.classList.replace("invalid","valid")
        password_error.innerHTML = "";
    }
    
}

function check_re_passwd(){
    if (re_password_input.value.length != 0 && re_password_input.value != password_input.value) {
        if (re_password_input.classList.contains("valid")) re_password_input.classList.replace("valid", "invalid")
        else re_password_input.classList.replace("log-in", "invalid");
    re_password_error.innerHTML = "Hasła nie są takie same";
    }
    else if (re_password_input.value.length == 0) {
        if (re_password_input.classList.contains("invalid"))
            re_password_input.classList.replace("invalid", "log-in");
        re_password_error.innerHTML = "";
    }
    else {
        re_password_input.classList.replace("invalid", "valid")
        re_password_error.innerHTML = "";
    }

}