from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def pagina_horarios():
    return render_template('pagina horarios.html')

@app.route('/inicio_sesion/')
def inicio_sesion():
    return render_template('pagina inicio sesion.html')

@app.route('/pagina_docentes/')
def pagina_docente():
    return render_template('pagina docentes.html')


if __name__ == "__main__":
        app.run(debug=True)