import pandas as pd

# Cargar los datos desde un archivo CSV
cursos_df = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/cursos/cursos_malla.csv")

# Reemplazar valores NaN con cadenas vacías y crear una columna de requisitos como lista
cursos_df = cursos_df.fillna('')
cursos_df['requisitos'] = cursos_df['requisitos'].apply(lambda x: x.split(';') if x else [])
cursos_df['correquisitos'] = cursos_df['correquisitos'].apply(lambda x: x.split(';') if x else [])
cursos_df['esrequisito'] = cursos_df['esrequisito'].apply(lambda x: x.split(';') if x else [])

print(cursos_df)