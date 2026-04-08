import requests
import pandas as pd

MOEDAS = {

    "USD": 1,
    "EUR": 21619,
    "GBP": 21623,

}

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

def igpm(inicio="01/01/2020", fim=None):
    return serie(189, inicio, fim)

def cambio(moeda="USD", inicio="01/01/2020", fim=None):
    if moeda not in MOEDAS:
        raise ValueError(f"Moeda '{moeda}' não suportada. Use: {list(MOEDAS.keys())}")
    
    codigo = MOEDAS[moeda]
    return serie(codigo, inicio, fim)


def expectativas(indicador="IPCA"):
    url = (
        "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/"
        f"ExpectativaMercadoMensais?$filter=Indicador%20eq%20%27{indicador}%27"
        "&$format=json&$orderby=Data%20desc&$top=100"
    )
    
    resposta = requests.get(url)
    print(resposta.status_code)
    dados = resposta.json()
    df = pd.DataFrame(dados["value"])
    df["Data"] = pd.to_datetime(df["Data"])
    return df

    
