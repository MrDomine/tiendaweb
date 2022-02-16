window.onload=()=>{

    for(let i=0; i<document.getElementsByClassName("iconoUsuario").length;i++){
        document.getElementsByClassName("iconoUsuario")[i].onmouseover=()=>{
            if(document.getElementById("datosUsuario").classList.contains("datosUsuario")){
                document.getElementById("datosUsuario").classList.remove("datosUsuario")
            } else {
                document.getElementById("datosUsuario").classList.add("datosUsuario")
            }
            
        }
    }
    /*document.getElementById("datosUsuario").onblur=()=>{
        document.getElementById("datosUsuario").classList.remove('datosUsuario');
    }*/

    let titulos=document.getElementsByClassName("tituloProducto")
    for (let i = 0; i < titulos.length; i++) {
        titulos[i].onmouseover=function(e){
            e.currentTarget.style.backgroundColor="red";
        }
    }
    for (let i = 0; i < titulos.length; i++) {
        titulos[i].onmouseleave=function(e){
            e.currentTarget.style.backgroundColor="white";
        }
    }
}