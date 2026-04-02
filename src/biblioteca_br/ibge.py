import logging
import requests
import pandas as pd
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def _call_ibge_api(agregado: int, variavel: int, inicio: Optional[str] = None, fim: Optional[str] = None) -> pd.DataFrame:
    """Chama a API do IBGE com intervalo de datas obrigatório."""
    # Define período padrão se não informado
    if inicio is None:
        inicio = "201501"  # janeiro de 2015
    if fim is None:
        fim = "202503"     # março de 2025 (último disponível)
    
    periodo = f"{inicio}-{fim}"
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{agregado}/periodos/{periodo}/variaveis/{variavel}?localidades=N1[all]"
    
    try:
        logger.info(f"Chamando API IBGE: agregado={agregado}, periodo={periodo}")
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            raise ValueError("Resposta vazia da API do IBGE.")
        df = _parse_ibge_response(data)
        return df
    except Exception as e:
        logger.exception(f"Erro ao acessar API IBGE: {e}")
        raise

def _parse_ibge_response(data):
    rows = []
    for agregado in data:
        for resultado in agregado.get("resultados", []):
            for serie in resultado.get("series", []):
                local = serie.get("localidade", {}).get("nome", "")
                for periodo, valor in serie.get("serie", {}).items():
                    rows.append({
                        "periodo": periodo,
                        "valor": valor if valor != "..." else None,
                        "localidade": local
                    })
    df = pd.DataFrame(rows)
    if not df.empty:
        try:
            df["data"] = pd.to_datetime(df["periodo"], format="%Y%m", errors="coerce")
        except:
            df["data"] = pd.to_datetime(df["periodo"], format="%Y", errors="coerce")
        df = df.sort_values("data")
    return df

# Funções públicas agora aceitam inicio e fim opcionais
def pib(inicio: Optional[str] = None, fim: Optional[str] = None) -> pd.DataFrame:
    """PIB trimestral do Brasil (valores correntes)."""
    return _call_ibge_api(agregado=1846, variavel=37, inicio=inicio, fim=fim)

def desemprego(inicio: Optional[str] = None, fim: Optional[str] = None) -> pd.DataFrame:
    """Taxa de desemprego - PNAD Contínua."""
    return _call_ibge_api(agregado=4099, variavel=4099, inicio=inicio, fim=fim)

def populacao(ano: Optional[int] = None) -> pd.DataFrame:
    """População estimada por ano."""
    if ano:
        inicio = fim = str(ano)
    else:
        inicio = "2015"
        fim = "2024"
    return _call_ibge_api(agregado=4709, variavel=4709, inicio=inicio, fim=fim)

def ipca(inicio: Optional[str] = None, fim: Optional[str] = None) -> pd.DataFrame:
    """IPCA geral (IBGE) - índice mensal."""
    return _call_ibge_api(agregado=1737, variavel=1737, inicio=inicio, fim=fim)