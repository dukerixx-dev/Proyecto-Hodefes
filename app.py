from flask import Flask, render_template, request, redirect, url_for
import json

app=Flask(__name__)


    
@app.post("/login")
def verificar_inicio_de_sesion():
    correo=request.form.get("correo")
    contrasena=request.form.get("contraseña")
    with open("inicio_sesion.json","r") as archivo:
            inicio_sesion=json.load(archivo)
    for i in inicio_sesion:
        if correo == i["correo"] and contrasena == i["contrasena"]:
            return redirect(url_for("pagina_horarios"))

    return render_template("pagina inicio sesion.html ")


@app.get('/')
def inicio_de_sesion():
    return render_template("pagina inicio sesion.html ")
    

@app.route('/pagina_horarios/')
def pagina_horarios():
    with open("profes.json","r") as archivo:
        profes=json.load(archivo)
    return render_template('pagina horarios.html',datos=profes)

#def filtro_y_busqueda():
    #investigar sobre post, ida y vuelta


@app.route('/pagina_docentes/')
def pagina_docente():

    return render_template('pagina docentes.html')


if __name__ == "__main__":
        app.run(debug=True)