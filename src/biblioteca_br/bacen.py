# bacen.py
import logging
import requests
import pandas as pd
from typing import Optional, List, Dict, Any

# Configuração básica de logging (pode ser ajustada depois)
logger = logging.getLogger(__name__)

# Dicionário de moedas com seus códigos SGS
MOEDAS: Dict[str, int] = {
    "USD": 1,      # Dólar comercial
    "EUR": 21619,  # Euro
    "GBP": 21623,  # Libra
}

# ----------------------------------------------------------------------
# Função interna para chamadas genéricas à API SGS
# ----------------------------------------------------------------------
def _fetch_sgs_series(codigo: int, inicio: str = "01/01/2020", fim: Optional[str] = None) -> pd.DataFrame:
    """
    Consulta uma série do SGS (Sistema Gerenciador de Séries Temporais) do Banco Central.
    
    Parâmetros:
        codigo (int): Código da série SGS.
        inicio (str): Data de início no formato "dd/mm/aaaa". Padrão: "01/01/2020".
        fim (str, opcional): Data de fim no mesmo formato. Se None, vai até a data mais recente.
    
    Retorna:
        pd.DataFrame: DataFrame com colunas 'data' (datetime) e 'valor' (float).
    
    Levanta:
        requests.exceptions.RequestException: se houver erro de rede ou HTTP.
        ValueError: se a resposta não for JSON válido ou dados não estiverem no formato esperado.
    """
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
    params = {
        "formato": "json",
        "dataInicial": inicio,
    }
    if fim:
        params["dataFinal"] = fim

    try:
        logger.info(f"Fazendo requisição para série {codigo}...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Levanta exceção para status HTTP 4xx/5xx

        dados = response.json()
        if not dados:
            raise ValueError(f"Série {codigo} retornou vazia.")

        df = pd.DataFrame(dados)
        df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        # Remove linhas onde valor é NaN (caso haja dados mal formatados)
        df = df.dropna(subset=["valor"]).reset_index(drop=True)

        logger.info(f"Série {codigo} obtida com sucesso: {len(df)} registros.")
        return df

    except requests.exceptions.Timeout:
        logger.error(f"Timeout ao acessar API para série {codigo}.")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição para série {codigo}: {e}")
        raise
    except ValueError as e:
        logger.error(f"Erro ao processar dados da série {codigo}: {e}")
        raise
    except Exception as e:
        logger.exception(f"Erro inesperado na série {codigo}: {e}")
        raise

# ----------------------------------------------------------------------
# Funções públicas para os indicadores mais comuns
# ----------------------------------------------------------------------

def selic(inicio: str = "01/01/2020", fim: Optional[str] = None) -> pd.DataFrame:
    """Taxa Selic (meta) diária - código SGS 11."""
    return _fetch_sgs_series(11, inicio, fim)

def ipca(inicio: str = "01/01/2020", fim: Optional[str] = None) -> pd.DataFrame:
    """Índice Nacional de Preços ao Consumidor Amplo (IPCA) - código SGS 433."""
    return _fetch_sgs_series(433, inicio, fim)

def igpm(inicio: str = "01/01/2020", fim: Optional[str] = None) -> pd.DataFrame:
    """Índice Geral de Preços do Mercado (IGP-M) - código SGS 189."""
    return _fetch_sgs_series(189, inicio, fim)

def cambio(moeda: str = "USD", inicio: str = "01/01/2020", fim: Optional[str] = None) -> pd.DataFrame:
    """
    Cotação de moeda estrangeira (comercial) - via SGS.
    
    Moedas suportadas: USD, EUR, GBP.
    """
    if moeda not in MOEDAS:
        raise ValueError(f"Moeda '{moeda}' não suportada. Use: {list(MOEDAS.keys())}")
    codigo = MOEDAS[moeda]
    return _fetch_sgs_series(codigo, inicio, fim)

def expectativas(indicador: str = "IPCA", top: int = 100) -> pd.DataFrame:
    """
    Expectativas de mercado do Boletim Focus (via API Olinda).
    
    Parâmetros:
        indicador (str): Nome do indicador (IPCA, IGP-M, Selic, etc.).
        top (int): Número máximo de registros.
    
    Retorna:
        pd.DataFrame: Dados de expectativas mensais.
    """
    url = (
        "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/"
        f"ExpectativaMercadoMensais?$filter=Indicador%20eq%20%27{indicador}%27"
        f"&$format=json&$orderby=Data%20desc&$top={top}"
    )
    try:
        logger.info(f"Buscando expectativas para {indicador}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        dados = response.json()
        if "value" not in dados:
            raise ValueError("Resposta da API não contém 'value'.")
        df = pd.DataFrame(dados["value"])
        df["Data"] = pd.to_datetime(df["Data"])
        logger.info(f"Expectativas obtidas: {len(df)} registros.")
        return df
    except Exception as e:
        logger.exception(f"Erro ao obter expectativas para {indicador}: {e}")
        raise

def juros_bancos(top: int = 1000) -> pd.DataFrame:
    """
    Taxas de juros por banco e modalidade (mensal).
    """
    url = (
        "https://olinda.bcb.gov.br/olinda/servico/taxaJuros/versao/v2/odata/"
        f"TaxasJurosMensalPorMes?$format=json&$top={top}"
    )
    try:
        logger.info("Buscando taxas de juros bancários...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        dados = response.json()
        if "value" not in dados:
            raise ValueError("Resposta da API não contém 'value'.")
        df = pd.DataFrame(dados["value"])
        # Converter colunas de data se existirem
        if "Data" in df.columns:
            df["Data"] = pd.to_datetime(df["Data"])
        logger.info(f"Taxas de juros obtidas: {len(df)} registros.")
        return df
    except Exception as e:
        logger.exception(f"Erro ao obter taxas de juros: {e}")
        raise