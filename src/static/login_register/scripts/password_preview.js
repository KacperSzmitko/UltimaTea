
function show_password(){
    var x = document.getElementById("reg_id_password");
    if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}