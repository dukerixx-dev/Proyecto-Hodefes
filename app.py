from flask import Flask, render_template, request, redirect, url_for, flash
import json

app=Flask(__name__)
app.secret_key = "clave"

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
            nombre_usuario= i["usuario"]
            carrera=i["carrera"]
            #subcadena desde el final del correo hasta el arroba
            if i["correo"][-17:]=="alumnos.ulagos.cl":
                return redirect(f"/pagina_horarios/{carrera}/{nombre_usuario}")
            else:   
                return redirect(f"pagina_docentes/{carrera}/{nombre_usuario}")
    return render_template("pagina inicio sesion.html ")


#Pagina de horarios
@app.route('/pagina_horarios/<carrera>/<usuario>')
def pagina_horarios(carrera,usuario):
    with open("profes.json","r") as archivo:
        profes=json.load(archivo)
    with open("tickets.json","r") as archivo:
        Tickets=json.load(archivo)

    return render_template('pagina horarios.html',profes=profes,usuario=usuario,carrera=carrera, Tickets=Tickets)

@app.route('/enviar_ticket/<carrera>/<usuario>/<docente>', methods=["POST"])
def enviar_ticket(carrera,usuario,docente):
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
        "carrera":carrera,
        "tipo": tipo_ticket,
        "contenido":contenido_ticket,
        "respuesta":"",
        "estado": "pendiente"
    }
    Tickets.append(nuevo_ticket)
    print(nuevo_ticket["id"], " ", nuevo_ticket["estudiante"], " ", nuevo_ticket["tipo"], " ", nuevo_ticket["docente"], " ",nuevo_ticket["contenido"]  )
    with open("tickets.json","w") as archivo:
        json.dump(Tickets,archivo,indent=4)

    flash("La solicitud ha sido enviada!")
    return redirect(f'/pagina_horarios/{carrera}/{usuario}')

@app.route("/pagina_horarios/invitado")    
def invitado():
    with open("profes.json","r") as archivo:
        profes=json.load(archivo)
    return render_template('pagina de horarios invitados.html',datos=profes)


#Pagina de docentes
@app.route('/pagina_docentes/<carrera>/<usuario>')
def pagina_docentes(carrera,usuario):
    with open("tickets.json","r") as archivo:
        Tickets=json.load(archivo)
    return render_template('pagina docentes.html', Tickets=Tickets, carrera=carrera, usuario=usuario)

@app.route('/responder_ticket/<carrera>/<usuario>/<int:ticket_id>', methods=["POST"])
def responder_ticket(carrera,usuario,ticket_id):
    respuesta=request.form["respuesta"]
    for x in request.form:
        ticket_tipo_respuesta=x
    with open("tickets.json","r") as archivo:
        Tickets=json.load(archivo)
    for i in Tickets:
        if i["id"]==ticket_id:
            i["respuesta"]=respuesta
            if ticket_tipo_respuesta == "coordinar_reunion" or ticket_tipo_respuesta == "enviar_resuelto":
                i["estado"]="respondido"
    with open("tickets.json","w") as archivo2:
        json.dump(Tickets,archivo2,indent=4)

    flash("Su respuesta ha sido enviada!")    
    return redirect(f'/pagina_docentes/{carrera}/{usuario}')


def pagina_no_encontrada(error):
    return redirect(url_for("inicio_de_sesion"))


if __name__ == "__main__":
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()