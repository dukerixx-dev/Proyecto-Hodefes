from flask import Flask, render_template, request, redirect, url_for
import json

app=Flask(__name__)

"""
DEBE DE ESTAR DOCUMENTADO
"""

#Inicio sesión
@app.get('/')
def inicio_de_sesion():
    return render_template("pagina inicio sesion.html ")
@app.post("/login")
def verificar_inicio_de_sesion():
    correo=request.form.get("correo")
    contrasena=request.form.get("contraseña")
    with open("inicio_sesion.json","r") as archivo:
            inicio_sesion=json.load(archivo)

    for i in inicio_sesion:
        if correo == i["correo"] and contrasena == i["contrasena"]:
            #subcadena desde el final del correo hasta el arroba
            if i["correo"][-17:]=="alumnos.ulagos.cl":
                nombre_usuario= i["correo"][:-18]
                return redirect(f"/pagina_horarios/{nombre_usuario}")
            else:   
                nombre_usuario= i["correo"][:-10]
                return redirect(f"pagina_docentes/{nombre_usuario}")
    return render_template("pagina inicio sesion.html ")


#Pagina de horarios
@app.route('/pagina_horarios/<usuario>')
def pagina_horarios(usuario):
    with open("profes.json","r") as archivo:
        profes=json.load(archivo)
    return render_template('pagina horarios.html',datos=profes,usuario=usuario)

@app.route('/enviar_ticket/<usuario>/<docente>', methods=["POST"])
def enviar_ticket(usuario,docente):
    #conseguir el tipo de ticket
    for x in request.form:
        tipo_ticket=x
    contenido_ticket=request.form[tipo_ticket]
    with open("tickets.json","r") as archivo:
        Tickets=json.load(archivo)
    nuevo_ticket={
        "id":len(Tickets)+1,
        "estudiante":usuario,
        "docente":docente,
        "tipo": tipo_ticket,
        "contenido":contenido_ticket,
        "respuesta":"",
        "estado": "pendiente"
    }
    Tickets.append(nuevo_ticket)
    print(nuevo_ticket["id"], " ", nuevo_ticket["estudiante"], " ", nuevo_ticket["tipo"], " ", nuevo_ticket["docente"], " ",nuevo_ticket["contenido"]  )
    with open("tickets.json","w") as archivo:
        json.dump(Tickets,archivo,indent=4)
    return "hola"

@app.route("/pagina_horarios/invitado")    
def invitado():
    with open("profes.json","r") as archivo:
        profes=json.load(archivo)
    return render_template('pagina de horarios invitados.html',datos=profes)


#Pagina de docentes
@app.route('/pagina_docentes/<usuario>')
def pagina_docentes(usuario):
    return render_template('pagina docentes.html')


if __name__ == "__main__":
        app.run(debug=True)