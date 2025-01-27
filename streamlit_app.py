import streamlit as st
import pandas as pd

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Detalles de cursos - CLIE - EIEM - TEC',
)


'''
# Detalles de cursos
#### Comisión para la creación de la Licenciatura en Ingeniería Electromecánica
Escuela de Ingeniería Electromecánica - Tecnológico de Costa Rica
'''

areas = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/areas.csv")
cursosraw = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/cursos/cursos_malla.csv")
rasgos = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/rasgos.csv")
saberes = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/saberes.csv")
cursos_rasgos = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/cursos/cursos_rasgos.csv")

nomArea = st.selectbox(
    'Area',
    areas[areas["nombre"] != "Total"]["nombre"])

codArea = areas[areas["nombre"]==nomArea]["codArea"].item()
cursos = cursosraw[(cursosraw["area"]==codArea)\
                   & (cursosraw["semestre"]<=10)\
                   & (cursosraw["nombre"]!="Electiva I")\
                   & (cursosraw["nombre"]!="Electiva II") ]
saberes = saberes[saberes["codArea"]==codArea].copy()

nomCurso = st.selectbox(
    "Curso",
    cursos[cursos["area"]==codArea]["nombre"])

st.markdown("### Detalles:")

codCurso = cursos[cursos["nombre"]==nomCurso]["codigo"].item()

idCurso = cursos[cursos["nombre"]==nomCurso]["id"].item()

semes = cursos[cursos["nombre"]==nomCurso]["semestre"].item()

cred = cursos[cursos["nombre"]==nomCurso]["creditos"].item()

hteor = cursos[cursos["nombre"]==nomCurso]["horasTeoria"].item()

hprac = cursos[cursos["nombre"]==nomCurso]["horasPractica"].item()

st.markdown(
f'''
* ID: {idCurso}
* Código: {codCurso}
* Semestre: {semes}
* Creditos: {cred}
* Horas: {hteor + hprac}
* Horas teoría: {hteor}
* Horas práctica: {hprac}
* Horas extraclase: {(cred * 3)-(hteor + hprac)}
''')

st.markdown("*Requisitos:*")

req = cursos[cursos["nombre"]==nomCurso]["requisitos"].str.split(';', expand=False).item()
if str(req) != "nan":
    for index in range(len(req)):
        curReq = cursosraw[cursosraw["id"]==req[index]]["nombre"].item()
        st.markdown(f"* {curReq}") 
else:
    st.markdown("* No")

st.markdown("*Correquisitos:*")

cor = cursos[cursos["nombre"]==nomCurso]["correquisitos"].str.split(';', expand=False).item()
if str(cor) != "nan":
    for index in range(len(cor)):
        curCor = cursosraw[cursosraw["id"]==cor[index]]["nombre"].item()
        st.markdown(f"* {curCor}") 
else:
    st.markdown("* No")

codSaber = cursos_rasgos[cursos_rasgos["id"]==idCurso]["codSaber"].str.split(';', expand=False).item()

rasgos["codSaber"] = rasgos["codSaber"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila

rasgos = rasgos.explode("codSaber") #expadir la lista

codRasgos = rasgos[rasgos["codSaber"].isin(codSaber)]["rasgo"].unique()

st.markdown("### Saberes:")

for index in range(len(codSaber)):
    saber = saberes[saberes["codSaber"]==codSaber[index]]["nombre"].item()
    st.markdown(f"* {saber}")

st.markdown("### Rasgos:")

for index in range(len(codRasgos)):
    rasgo = codRasgos[index]
    st.markdown(f"* {rasgo}")