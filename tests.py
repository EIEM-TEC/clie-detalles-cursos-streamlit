import pandas as pd

areas = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/areas.csv").fillna("")
cursosraw = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/cursos/cursos_malla.csv").fillna("")
rasgos = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/rasgos.csv").fillna("")
saberes = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/saberes.csv").fillna("")
cursos_rasgos = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/cursos/cursos_rasgos.csv").fillna("")


# nomArea = areas[areas["nombre"] != "Total"]["nombre"].head(1).item()
nomArea = "Instalaciones electromecánicas"

codArea = areas[areas["nombre"]==nomArea]["codArea"].item()
saberes = saberes[saberes["codArea"]==codArea]

cursos = cursosraw[(cursosraw["area"]==codArea)\
                   & (cursosraw["semestre"]<=10)\
                   & (cursosraw["nombre"]!="Electiva I")\
                   & (cursosraw["nombre"]!="Electiva II") ].copy()

#"Codigo de area:", codArea

# nomCurso = cursos[cursos["area"]==codArea]["nombre"].head(1).item()
nomCurso = "Gestión de la energía"

codCurso = cursos[cursos["nombre"]==nomCurso]["codigo"].item()
idCurso = cursos[cursos["nombre"]==nomCurso]["id"].item()

cursos_rasgos["codSaber"] = cursos_rasgos["codSaber"].str.split(';', expand=False)

codSaber = cursos_rasgos[cursos_rasgos["id"]==idCurso]["codSaber"].item()

rasgos["codSaber"] = rasgos["codSaber"].str.split(';', expand=False)

rasgos = rasgos.explode("codSaber")

codRasgos = rasgos[rasgos["codSaber"].isin(codSaber)]["rasgo"].unique()

print("Requisitos:\n")

cursos["requisitos"] = cursos["requisitos"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila

req = cursos[cursos["nombre"]==nomCurso]["requisitos"].item()

if req != [""]:
    for reqi in req:
        codReq = cursosraw[cursosraw["id"]==reqi]["codigo"].item()
        curReq = cursosraw[cursosraw["id"]==reqi]["nombre"].item()
        print(f"* {codReq} - {curReq}") 
else:
    print("* No")

print("Ruta de requisitos:\n")

cursosraw["requisitos"] = cursosraw["requisitos"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila

rutaReq = set()

def recurReq(req):
    if req != [""]:
        for reqi in req:
            seme = cursosraw[cursosraw["id"]==reqi]["semestre"].item()
            fila = cursosraw[cursosraw["id"]==reqi]["fila"].item()
            codReq = cursosraw[cursosraw["id"]==reqi]["codigo"].item()
            curReq = cursosraw[cursosraw["id"]==reqi]["nombre"].item()
            order = int(str(seme) + str(fila))
            rutaReq.add((order, codReq, curReq))
            print(f"* {codReq} - {curReq}")
            reqreq = cursosraw[cursosraw["id"]==reqi]["requisitos"].item()
            recurReq(reqreq)

recurReq(req)

# Convert the set to a list and sort it by "nombre"
rutaReq = sorted(list(rutaReq), key=lambda x: x[0])

for req in rutaReq:
    print(req[2])