from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Cargar datos en dataframes
df_games = pd.read_csv("D:\\Curso Henry\\DasetAPI\\df_reviews_user.csv", encoding='utf-8')

class GenreRequest(BaseModel):
    genero: str

class GenreResponse(BaseModel):
    año: int

# Cambiando a un endpoint de tipo POST
@app.post("/PlayTimeGenre")
def playtime_genre(request: GenreRequest):
    genero = request.genero
    print(f"Llamada a /PlayTimeGenre con género {genero}")

    # Filtrar el dataframe para el género especificado
    df_genre = df_games[df_games['genres'] == genero]

    if df_genre.empty:
        raise HTTPException(status_code=404, detail=f"No hay datos para el género {genero}")

    # Encontrar el año con más horas jugadas
    idxmax_playtime = df_genre['playtime_forever'].idxmax()
    año_max = df_genre.loc[idxmax_playtime, 'release_year']

    return GenreResponse(año=año_max)




# Función para obtener el usuario con más horas jugadas y la acumulación de horas por año para un género dado
@app.get("/user_for_genre/{genero}")
def user_for_genre(genero: str):
    print(f"Llamada a /user_for_genre/{genero}")
    acumulacion_horas = []
    usuarios_por_año = {}
    
    for registro in datos_ejemplo["reviews"]:
        if registro["genero"] == genero:
            usuario = registro["usuario"]
            horas = registro["horas_jugadas"]
            año = registro["año"]
            
            if usuario not in usuarios_por_año:
                usuarios_por_año[usuario] = {}
                
            if año not in usuarios_por_año[usuario]:
                usuarios_por_año[usuario][año] = 0
                
            usuarios_por_año[usuario][año] += horas
    
    usuario_max = max(usuarios_por_año, key=lambda x: sum(usuarios_por_año[x].values()))
    
    for año, horas in usuarios_por_año[usuario_max].items():
        acumulacion_horas.append({"Año": año, "Horas": horas})
    
    return {"Usuario con más horas jugadas para Género X": usuario_max, "Horas jugadas": acumulacion_horas}

# Función para obtener el top 3 de juegos más recomendados por usuarios para un año dado
@app.get("/users_recommend/{año}")
def users_recommend(año: int):
    print(f"Llamada a /users_recommend/{año}")
    juegos_recomendados = [registro for registro in datos_ejemplo["reviews"] if registro["año"] == año and registro["recommend"] and registro["sentimiento"] in ["Positive", "Neutral"]]
    top_juegos = sorted(juegos_recomendados, key=lambda x: x["sentimiento"], reverse=True)[:3]
    
    return [{"Puesto {}".format(i+1): juego} for i, juego in enumerate(top_juegos)]

# Función para obtener el top 3 de desarrolladoras con juegos menos recomendados por usuarios para un año dado
@app.get("/users_worst_developer/{año}")
def users_worst_developer(año: int):
    print(f"Llamada a /users_worst_developer/{año}")
    juegos_no_recomendados = [registro for registro in datos_ejemplo["reviews"] if registro["año"] == año and not registro["recommend"] and registro["sentimiento"] == "Negative"]
    top_desarrolladoras = sorted(set(juego["genero"] for juego in juegos_no_recomendados), key=lambda x: sum(1 for juego in juegos_no_recomendados if juego.get("genero") == x), reverse=True)[:3]
    
    return [{"Puesto {}".format(i+1): desarrolladora} for i, desarrolladora in enumerate(top_desarrolladoras)]

# Función para realizar un análisis de sentimiento según el género del juego
@app.get("/sentiment_analysis/{genero}")
def sentiment_analysis(genero: str):
    print(f"Llamada a /sentiment_analysis/{genero}")
    categorias_sentimiento = {"Negative": 0, "Neutral": 0, "Positive": 0}
    
    for registro in datos_ejemplo["reviews"]:
        if "genero" in registro and registro.get("genero") == genero:
            categorias_sentimiento[registro["sentimiento"]] += 1
    
    return {genero: categorias_sentimiento}
