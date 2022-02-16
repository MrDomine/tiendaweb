window.onload=()=>{
    
        ajax=new XMLHttpRequest();

        ajax.onreadystatechange=()=>{
            if(ajax.readyState==4){
                if(ajax.status==200){
                    let productos=JSON.parse(ajax.responseText);
                    mostrarProductos(productos);
                }
            }
        }
        ajax.open('GET','http://192.168.1.10:8080/getproducts',true);
        ajax.send(null);
    
}

function mostrarProductos(productos){
    let contenido="";
    for(let i=0;i<productos.length;i++){
        contenido +=`<div class="filaProducto">
                        <img src='static/img/${productos[i].img}'>
                        <div class="tituloProducto">
                            <h4>${productos[i].nombre}</h4>
                            <p>${productos[i].descripcion}</p>
                        </div>
                        <div>
                            <label>Precio</label><span>${productos[i].precio}</span><label>Cantidad:</label><span>${productos[0].cantidad}</span>
                        </div>
                        <div>
                            <img src="static/img/borrar.png" id="btn${productos[i].id}" class="btnBorrar">
                        </div>
                    </div>`;
        
    }
    

    document.getElementById("creados").innerHTML=contenido;

    asociarEventos();
}

function asociarEventos(){
    let papeleras=document.getElementsByClassName("btnBorrar");
    for(let i=0;i<papeleras.length;i++){
        const papelera=papeleras[i];
        papelera.onclick=(evt)=>{
            let idProducto=evt.currentTarget.id.substring(3);
            ajax=new XMLHttpRequest();
            ajax.onreadystatechange=()=>{
                if(ajax.readyState==4){
                    if(ajax.status==200){
                        let productos=JSON.parse(ajax.responseText);
                        mostrarProductos(productos);
                    }else if(ajax.status==500){
                        alert("Error en el servidor");
                    }
                }
            }
            let url=`http://192.168.1.10:8080/eliminarProducto?id=${idProducto}`
            ajax.open("GET",url,true);
            ajax.send(null);
        }
    }
}
