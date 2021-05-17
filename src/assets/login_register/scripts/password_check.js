var password_input = document.getElementsByClassName("register-password").item(0);
var password_error = document.getElementById("e_pass");

var re_password_input = document.getElementById("id_re_password");
var re_password_error = document.getElementById("e_repass");

var special = document.getElementById("special-char");
var len = document.getElementById("len");
var big_letter = document.getElementById("big-letter");
var digit = document.getElementById("digit");

var contrants_num = 4;
re_password_input.oninput = check_re_passwd;
password_input.oninput = check_passwd;
password_input.onfocus = display_passoword_requriments;
password_input.onblur = hide_password_requriments;

function display_passoword_requriments(){
    password_error.style.display = "block";
}

function hide_password_requriments(){
    if (password_input.value.length == 0)
    password_error.style.display = "none";
}

function check_passwd() {
    var count = 0;
    if (password_input.value.length!= 0)
    {       
        if (re_password_input.value.length != 0)
        {
            if (re_password_input.value == password_input.value)
            { 
                re_password_input.classList.replace("invalid", "valid");
                re_password_error.style.display = "none";
            }
            else
            { 
                re_password_input.classList.replace( "valid","invalid");
                re_password_error.style.display = "block";
            }
        }
        
        password_error.style.display = "block";
        if (password_input.value.match("(?=.*[?!.!\"#%&'()*+,\-\./:<>=?@\\[\\]\^_{}|~$])") != null)
        {
            special.classList.replace("invalid-text","valid-text");
            count++;
        }
        else
        {
            special.classList.replace("valid-text","invalid-text");
        }

        if (password_input.value.match("(?=.*[A-Z])"))
        {
            big_letter.classList.replace("invalid-text","valid-text");
            count++;
        }
        else
        {
            big_letter.classList.replace("valid-text","invalid-text");
        }

        if(password_input.value.length >= 8)
        {
            len.classList.replace("invalid-text","valid-text");
            count++;
        }                
        else
        {
            len.classList.replace("valid-text","invalid-text");
        }
               
        if(password_input.value.match("(?=.*[0-9])"))
        {
            digit.classList.replace("invalid-text","valid-text");
            count++;
        }
        else
        {
            digit.classList.replace("valid-text","invalid-text");
        }
    }
    else
    {
        if (password_input.classList.contains("invalid"))
            password_input.classList.replace("invalid","log-in");
        return;
    }
    
    if (count==contrants_num)
    {
        password_input.classList.replace("invalid","valid")
        password_error.style.display = "none";
    }
    else
    {
        if (password_input.classList.contains("valid")) password_input.classList.replace("valid", "invalid")
        else password_input.classList.replace("log-in","invalid");
    }
    
}

function check_re_passwd(){
    if (re_password_input.value.length != 0 && re_password_input.value != password_input.value) {
        if (re_password_input.classList.contains("valid")) re_password_input.classList.replace("valid", "invalid");
        re_password_input.classList.replace("log-in", "invalid");
        re_password_error.style.display = "block";
    }
    else if (re_password_input.value.length == 0) {
        if (re_password_input.classList.contains("invalid"))
            re_password_input.classList.replace("invalid", "log-in");
            re_password_input.classList.replace("valid", "log-in");
            re_password_error.style.display = "none";
    }
    else {
        if (!re_password_input.classList.replace("invalid", "valid")) re_password_input.classList.add("valid");
        re_password_input.classList.replace("log-in", "invalid");
        re_password_error.style.display = "none";
    }

}