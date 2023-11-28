from fastapi import FastAPI, HTTPException
import pandas as pd
app = FastAPI()

# Cargar datos en dataframes
df_games = pd.read_csv("D:\\Curso Henry\\DasetAPI\\df_reviews_user.csv", encoding='utf-8')

# Cambiando a un endpoint de tipo POST
@app.post("/PlayTimeGenre")
def playtime_genre(genero: str):
    print(f"Llamada a /PlayTimeGenre con género {genero}")

    # Filtrar el dataframe para el género especificado
    df_genre = df_games[df_games['genres'] == genero]

    if df_genre.empty:
        raise HTTPException(status_code=404, detail=f"No hay datos para el género {genero}")

    # Encontrar el año con más horas jugadas
    idxmax_playtime = df_genre['playtime_forever'].idxmax()
    año_max = df_genre.loc[idxmax_playtime, 'release_year']

    return {"Año de lanzamiento con más horas jugadas para Género X": año_max}



