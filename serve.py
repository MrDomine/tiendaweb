# serve.py
from ast import For
from flask import Flask, make_response, redirect, url_for
from flask import render_template
from flask import request,session,jsonify

import hashlib
import json
import os
import pathlib

from jinja2 import Undefined

# creates a Flask application, named app
app = Flask(__name__, static_folder="templates/static")

def validar(us,pwd):
    tienda={}
    with open('datos_tienda.json', 'r+') as file:
        tienda=json.load(file)
        file.close()
    for item in tienda["usuarios"]:
        if (item["usuario"]==us)&(item["password"]==hashlib.sha224(bytes(pwd, encoding="utf-8")).hexdigest()):
            return True
    return False

def comprobarUsuario(usr):
    tienda={}
    with open('datos_tienda.json', 'r+') as file:
        tienda=json.load(file)
        file.close()
    for item in tienda["usuarios"]:
        if (item["usuario"]==usr):
            return True
    return False

def registrarUsuario(usr,pwd):
    tienda={}
    with open("datos_tienda.json", "r") as file:
        tienda=json.load(file)
        file.close()

    tienda["usuarios"].append({"usuario":usr,"password":hashlib.sha224(bytes(pwd,encoding="utf-8")).hexdigest()})

    with open("datos_tienda.json", "w") as file:
        json.dump(tienda,file,indent=2)
        file.close()

def nombreUnico(fichero,directorio):
    dir=pathlib.Path(directorio)
    encontrado=False
    for file in dir.iterdir():
        if(file.name==fichero):
            encontrado=True
            break
    if(not encontrado):
        return fichero
    contador=fichero.split(".")[0][len(fichero.split(".")[0])-1]
    cont=0
    if(contador.isnumeric()):
        cont=int(contador)+1
    fichero=fichero.split(".")[0]+str(cont)+"."+fichero.split(".")[1]
    return nombreUnico(fichero,directorio)

def guardarProducto(nombreProducto,descripcion,filename,precio,cantidad):
    tienda={}
    with open("datos_tienda.json","r") as file:
        tienda=json.load(file)
        file.close()
    contador=0
    if("contador" in tienda.keys()):
        tienda["contador"]+=1
    else:
        tienda["contador"]=0
    contador=tienda["contador"]
    tienda["productos"].append({
        'id':contador,
        'nombre': nombreProducto,
        'descripcion':descripcion,
        'img':filename,
        'precio':precio,
        'cantidad':cantidad
    })

    with open("datos_tienda.json", "w") as file:
        json.dump(tienda,file,indent=2)
        file.close()
    
    return tienda['productos']

def leerProductosFichero():
    tienda={}
    with open("datos_tienda.json","r") as file:
        tienda=json.load(file)
        file.close()
    return tienda['productos']

def eliminarProduct(id):
    tienda={}
    with open("datos_tienda.json","r") as file:
        tienda=json.load(file)
        file.close()

    productos=tienda["productos"]
    pEliminar=None
    for item in productos:
        if(item['id']==id):
            pEliminar=item
            break
    productos.remove(pEliminar)
    with open("datos_tienda.json", "w") as file:
        json.dump(tienda,file,indent=2)
        file.close()
    
    return productos

# a route where we will display a welcome message via an HTML template

@app.route("/getproducts",methods=['GET'])
def mostrarProductos():
    productos=leerProductosFichero()
    return jsonify(productos)

@app.route("/")
def hello():
    message = "Hello, World"
    return redirect(url_for('login'))

@app.route("/producto")
def index():
    #name = request.cookies.get('userID')
    nombreUsuario=session.get("userId")
    if(nombreUsuario==None):
        return redirect(url_for('login'))
    else:
        return render_template("index.html",nombre=nombreUsuario)

@app.route("/login",methods=['POST','GET'])
def login():
    if(request.method=='GET'):
        return render_template('login.html')
    elif(request.method=='POST'):
        user=request.form.get("usr")
        passw=request.form.get("passw")
        if(validar(user,passw)):
            resp = make_response(redirect(url_for('index')))
            #resp.set_cookie('userID',hashlib.sha224(bytes(user,encoding="utf-8")).hexdigest())
            session["userId"]=user
            return resp
            #return redirect(url_for("hello"))
        else:
            msg="Usuario o contraseña incorrecto."
            return render_template('login.html',mensaje=msg)

@app.route("/registro",methods=['GET'])
def registro():
    return render_template('registro.html')

@app.route("/crearUsuario", methods=['POST'])
def crearUsuario():
    usuario=request.form["usr"]
    pwd=request.form["passw"]
    if(comprobarUsuario(usuario)):
        msg="El usuario ya existe"
        return redirect(url_for("registro", mensaje=msg))
    registrarUsuario(usuario,pwd)
    return redirect(url_for("login", usuarioExiste=usuario))

@app.route("/cerrarSesion")
def cerrarsesion():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('userID')
    return response

@app.route("/crearProducto", methods=['GET','POST'])
def crearProducto():
    if(request.method=="GET"):
        return render_template("formularioProducto.html")
    else:
        idProducto=request.form["idProducto"]
        nombreProducto=request.form['nombre']
        descripcion=request.form['descripcion']
        f=request.files["imagen"]
        filename=f.filename
        filename=nombreUnico(filename,'./templates/static/img')
        precio=request.form['precio']
        cantidad=request.form['cantidad']
        f.save(os.path.join('./templates/static/img',filename))
        productos=guardarProducto(nombreProducto,descripcion,filename,precio,cantidad)
        
        return redirect(url_for('crearProducto'))

@app.route("/eliminarProducto",methods=["GET","POST"])
def eliminarProducto():
    idProducto=int(request.args["id"])
    result=eliminarProduct(idProducto)
    return jsonify(result)

# run the application
if __name__ == "__main__":
    app.secret_key="generador de claves de sesion"
    app.run(host="192.168.1.10",port=8080, debug=True)
