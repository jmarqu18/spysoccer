# Archivo donde definiremos las funciones de
# cálculo de scoring, similitud y clustering
from sklearn.preprocessing import MinMaxScaler
import scipy.stats as ss


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
