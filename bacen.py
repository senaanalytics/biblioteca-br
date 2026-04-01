import requests
import pandas as pd

def serie(codigo, inicio="01/01/2020", fim=None):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
    parametros = {
        "formato": "json",
        "dataInicial": inicio,
    }
    if fim is not None:
        parametros["dataFinal"] = fim

    resposta = requests.get(url, params=parametros)
    dados = resposta.json()
    df = pd.DataFrame(dados)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = df["valor"].astype(float)
    return df

def selic(inicio="01/01/2020", fim=None):
    return serie(11, inicio, fim)

def ipca(inicio="01/01/2020", fim=None):
    return serie(433, inicio, fim)
    
