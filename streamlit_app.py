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

areas = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/areas.csv").fillna("")
cursosraw = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/cursos/cursos_malla.csv").fillna("")
rasgos = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/rasgos.csv").fillna("")
saberes = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/saberes.csv").fillna("")
cursos_rasgos = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/cursos/cursos_rasgos.csv").fillna("")

nomArea = st.selectbox(
    'Area',
    areas[areas["nombre"] != "Total"]["nombre"])

codArea = areas[areas["nombre"]==nomArea]["codArea"].item()
cursos = cursosraw[(cursosraw["area"]==codArea)\
                   & (cursosraw["semestre"]<=10)\
                   & (cursosraw["nombre"]!="Electiva I")\
                   & (cursosraw["nombre"]!="Electiva II") ].copy()
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
* Horas clase: {hteor + hprac}<br>
&nbsp;&nbsp;&nbsp;&nbsp; teoría: {hteor}<br>
&nbsp;&nbsp;&nbsp;&nbsp; práctica: {hprac}
* Horas extraclase: {(cred * 3)-(hteor + hprac)}
''', unsafe_allow_html=True)

st.markdown("*Requisitos:*")

cursos["requisitos"] = cursos["requisitos"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila

req = cursos[cursos["nombre"]==nomCurso]["requisitos"].item()

if req != [""]:
    for reqi in req:
        codReq = cursosraw[cursosraw["id"]==reqi]["codigo"].item()
        curReq = cursosraw[cursosraw["id"]==reqi]["nombre"].item()
        st.markdown(f"* {codReq} - {curReq}") 
else:
    st.markdown("* No")

st.markdown("*Correquisitos:*")

cursos["correquisitos"] = cursos["correquisitos"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila

cor = cursos[cursos["nombre"]==nomCurso]["correquisitos"].item()

if cor != [""]:
    for cori in cor:
        codCor = cursosraw[cursosraw["id"]==cori]["codigo"].item()
        curCor = cursosraw[cursosraw["id"]==cori]["nombre"].item()
        st.markdown(f"* {codCor} - {curCor}") 
else:
    st.markdown("* No")

st.markdown("*Es requisito:*")

cursos["esrequisito"] = cursos["esrequisito"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila

esreq = cursos[cursos["nombre"]==nomCurso]["esrequisito"].item()

if esreq != [""]:
    for esreqi in esreq:
        codesReq = cursosraw[cursosraw["id"]==esreqi]["codigo"].item()
        curesReq = cursosraw[cursosraw["id"]==esreqi]["nombre"].item()
        st.markdown(f"* {codesReq} - {curesReq}") 
else:
    st.markdown("* No")


cursos_rasgos["codSaber"] = cursos_rasgos["codSaber"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila

codSaber = cursos_rasgos[cursos_rasgos["id"]==idCurso]["codSaber"].item()

rasgos["codSaber"] = rasgos["codSaber"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila

rasgos = rasgos.explode("codSaber") #expadir la lista

codRasgos = rasgos[rasgos["codSaber"].isin(codSaber)]["rasgo"].unique()

cursos_rasgos = cursos_rasgos.explode("codSaber") #expadir la lista despues de tener codSaber

st.markdown("### Saberes:")

for codSaberi in codSaber:
    saber = saberes[saberes["codSaber"]==codSaberi]["nombre"].item()
    st.markdown(f"* **{saber}**")
    compar = cursos_rasgos[(cursos_rasgos["codSaber"]==codSaberi)\
                        & (cursos_rasgos["id"]!=idCurso)\
                        ]['id'].tolist()
    if compar != []:
            st.markdown("*Compartido con:*")
    for compari in compar:        
        if compari in cursos["id"].tolist():
            codCompar = cursos[cursos["id"]==compari]["codigo"].item()
            nomCompar = cursos[cursos["id"]==compari]["nombre"].item()
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{codCompar} - {nomCompar}")
    
st.markdown("### Rasgos:")

for rasgo in codRasgos:
    st.markdown(f"* {rasgo}")


st.markdown("### Ruta de requisitos:")

cursosraw["requisitos"] = cursosraw["requisitos"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila

def recurReq(req):
    if req != [""]:
        for reqi in req:
            codReq = cursosraw[cursosraw["id"]==reqi]["codigo"].item()
            curReq = cursosraw[cursosraw["id"]==reqi]["nombre"].item()
            st.markdown(f"* {codReq} - {curReq}")
            reqreq = cursosraw[cursosraw["id"]==reqi]["requisitos"].item()
            recurReq(reqreq)

recurReq(req)

st.markdown("### Ruta de cursos para los que es requisito:")

cursosraw["esrequisito"] = cursosraw["esrequisito"].str.split(';', expand=False) #convertir los valores separados por ; en una lista por fila

def recurEsReq(esreq):
    if esreq != [""]:
        for esreqi in esreq:
            codesReq = cursosraw[cursosraw["id"]==esreqi]["codigo"].item()
            curesReq = cursosraw[cursosraw["id"]==esreqi]["nombre"].item()
            st.markdown(f"* {codesReq} - {curesReq}")
            esreqesreq = cursosraw[cursosraw["id"]==esreqi]["esrequisito"].item()
            recurEsReq(esreqesreq)

recurEsReq(esreq)