window.onload=()=>{
    document.getElementById("password").onkeyup=validar
    document.getElementById("repassword").onkeyup=validar
}

function validar(id){
    let repassword=document.getElementById("repassword").value;
        let password=document.getElementById("password").value;
        if(password==repassword){
            document.getElementById("btnEnviar").disabled=false;
        }else{
            document.getElementById("btnEnviar").disabled=true;
        }
}