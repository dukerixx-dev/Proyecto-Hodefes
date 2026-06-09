from flask import Flask, render_template
import json

app=Flask(__name__)

@app.route('/')
def inicio_sesion():
        
    return render_template('pagina inicio sesion.html')


#def contenido_horarios():


@app.route('/pagina_horarios/')
def pagina_horarios():
    #el profe lucas sugiere hacer otra funcion que busque o filtre a un diccionario especifico que serian los profesores en el json para colocarlo en el html
    with open("profes.json","r") as archivo:
        profes=json.load(archivo)
    return render_template('pagina horarios.html',datos=profes)


@app.route('/pagina_docentes/')
def pagina_docente():

    return render_template('pagina docentes.html')


if __name__ == "__main__":
        app.run(debug=True)