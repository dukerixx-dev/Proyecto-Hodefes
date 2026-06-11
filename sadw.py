import json
with open("inicio_sesion.json","r") as archivo:
        inicio_sesion=json.load(archivo)
        print (inicio_sesion)
correo="pepe.torres@alumnos.ulagos.cl"
contrasena="1234"
for i in inicio_sesion:
    if correo == i["correo"]:
        if contrasena == i["contrasena"]:
            print("funciono")
        else:
            print("nop")
    else:
        print("nop")