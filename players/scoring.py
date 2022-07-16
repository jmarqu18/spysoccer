# Archivo donde definiremos las funciones de
# cálculo de scoring, similitud y clustering
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import scipy.stats as ss
import pandas as pd


def filter_context_data(data, minutes):
    # Limpiamos duplicados (ordenamos por minutos jugados)
    data = data.sort_values(by=["minutes_played"], ascending=False).drop_duplicates(
        "player_id", keep="first"
    )
    # Nos quedamos con jugadores con este minimo de minutos jugados
    data = data.loc[data["minutes_played"] >= minutes]

    return data


neg_metrics = []


def set_scoring(data, metricas, pesos):
    # Filtramos el dataframe entrante con las columnas requeridas
    columnas = ["player_id"]
    for metrica in metricas:
        columnas.append(metrica)
    data = data[columnas].copy()
    # Invertimos las columnas de métricas negativas (p.ej Goles contra)
    for col in columnas:
        if col in neg_metrics:
            data[col] = data[col] * (-1)
    # Primero normalizamos el dataframe entrante
    scaler = MinMaxScaler()
    scaler = scaler.fit(data[metricas])
    data[metricas] = scaler.transform(data[metricas])

    # Transformamos cada variable: valor transformado * peso asociado
    for i, metrica in enumerate(metricas):
        data[metrica] = data[metrica].apply(lambda x: x * pesos[i])
    # Calculamos el scoring (Suma de cada registro completo)
    data["scoring"] = data[metricas].sum(axis=1)
    # Ajustamos a 10
    data["scoring"] = round(10 * data["scoring"], 3)
    data["rank"] = (len(data) + 1) - ss.rankdata(data["scoring"], method="min").astype(
        int
    )
    data["scoring"] = data["scoring"].apply(
        lambda x: round((99 - max(data["scoring"] * 10) + x * 10), 3)
    )
    # Ordenamos el df resultante por "scoring"
    data.sort_values(by=["scoring"], ascending=False, inplace=True)

    return data


def set_similarity(data, metricas):
    # Filtramos el dataframe entrante con las columnas requeridas
    columnas = ["player_id"]
    for metrica in metricas:
        columnas.append(metrica)
    data = data[columnas].copy()
    # Primero normalizamos el dataframe entrante
    scaler = MinMaxScaler()
    scaler = scaler.fit(data[metricas])
    data[metricas] = scaler.transform(data[metricas])
    # sacamos a los jugadores al índice del dataframe para los cáculos de similaridad
    data = data.set_index("player_id")
    # Usamos la función cosine_similarity de sklearn
    vector = cosine_similarity(data.values)
    # Creamos un dataframe resultado de enfrentar todos los jugadores y su similitud
    df = pd.DataFrame(vector, columns=data.index.values, index=data.index).reset_index()
    # Generamos un dataframe vacio sobre el que colocar los pares de jugador-similar
    df_base = pd.DataFrame(columns=["player_id", "similar_player_id", "similarity"])

    for player in list(df.columns[1:]):
        df_temp = df[["player_id", player]]
        df_temp.rename(
            columns={player: "similarity", "player_id": "similar_player_id"},
            inplace=True,
        )
        df_temp = df_temp.sort_values("similarity", ascending=False).head(6)
        df_temp = df_temp.loc[df_temp["similarity"] < 1]
        df_temp["player_id"] = player
        df_base = pd.concat(
            [df_base, df_temp[["player_id", "similar_player_id", "similarity"]]]
        )

    # Redondeamos la similitud
    df_base["similarity"] = round(df_base["similarity"] * 100, 3)

    return df_base
