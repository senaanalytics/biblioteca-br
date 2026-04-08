# bacen.py
# Módulo de acesso aos dados do Banco Central do Brasil
# Autor: Isaque Sena

import logging
import requests
import pandas as pd
from typing import Optional, List, Dict, Any

# Configuração básica de logging
logger = logging.getLogger(__name__)

# Mapeamento de moedas para códigos SGS
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
    Busca uma série temporal do SGS (Sistema Gerenciador de Séries Temporais) do Banco Central.
    
    Esta função interna faz a comunicação direta com a API do BACEN e retorna
    os dados tratados em um DataFrame pandas.
    
    Args:
        codigo: Código numérico da série no sistema SGS
        inicio: Data inicial no formato "dd/mm/aaaa" (padrão: 01/01/2020)
        fim: Data final no mesmo formato (opcional - se omitido, traz até a data mais recente)
    
    Returns:
        DataFrame com colunas 'data' (datetime) e 'valor' (float)
    
    Raises:
        RequestException: Erros de conexão ou HTTP
        ValueError: Dados vazios ou formato inesperado
    """
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
    params = {
        "formato": "json",
        "dataInicial": inicio,
    }
    if fim:
        params["dataFinal"] = fim

    try:
        logger.info(f"Consultando série {codigo}...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        dados = response.json()
        if not dados:
            raise ValueError(f"Nenhum dado encontrado para a série {codigo}.")

        df = pd.DataFrame(dados)
        df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        df = df.dropna(subset=["valor"]).reset_index(drop=True)

        logger.info(f"Série {codigo} carregada: {len(df)} registros.")
        return df

    except requests.exceptions.Timeout:
        logger.error(f"Tempo esgotado ao consultar série {codigo}.")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Falha na requisição da série {codigo}: {e}")
        raise
    except ValueError as e:
        logger.error(f"Erro ao processar série {codigo}: {e}")
        raise
    except Exception as e:
        logger.exception(f"Erro inesperado na série {codigo}: {e}")
        raise

# ----------------------------------------------------------------------
# Funções públicas para os indicadores mais comuns
# ----------------------------------------------------------------------

def selic(inicio: str = "01/01/2020", fim: Optional[str] = None) -> pd.DataFrame:
    """Retorna a taxa Selic (meta) diária. Código SGS: 11."""
    return _fetch_sgs_series(11, inicio, fim)

def ipca(inicio: str = "01/01/2020", fim: Optional[str] = None) -> pd.DataFrame:
    """Retorna o IPCA (Índice Nacional de Preços ao Consumidor Amplo). Código SGS: 433."""
    return _fetch_sgs_series(433, inicio, fim)

def igpm(inicio: str = "01/01/2020", fim: Optional[str] = None) -> pd.DataFrame:
    """Retorna o IGP-M (Índice Geral de Preços do Mercado). Código SGS: 189."""
    return _fetch_sgs_series(189, inicio, fim)

def cambio(moeda: str = "USD", inicio: str = "01/01/2020", fim: Optional[str] = None) -> pd.DataFrame:
    """
    Retorna a cotação de moeda estrangeira (comercial).
    
    Moedas disponíveis: USD (dólar), EUR (euro), GBP (libra).
    """
    if moeda not in MOEDAS:
        raise ValueError(f"Moeda '{moeda}' não suportada. Use: {list(MOEDAS.keys())}")
    codigo = MOEDAS[moeda]
    return _fetch_sgs_series(codigo, inicio, fim)

def expectativas(indicador: str = "IPCA", top: int = 100) -> pd.DataFrame:
    """
    Busca as expectativas de mercado do Boletim Focus (API Olinda).
    
    Args:
        indicador: Nome do indicador (IPCA, IGP-M, Selic, etc.)
        top: Quantidade máxima de registros (padrão: 100)
    
    Returns:
        DataFrame com as expectativas mensais
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
        logger.info(f"Expectativas carregadas: {len(df)} registros.")
        return df
    except Exception as e:
        logger.exception(f"Erro ao buscar expectativas para {indicador}: {e}")
        raise

def juros_bancos(top: int = 1000) -> pd.DataFrame:
    """
    Retorna taxas de juros por banco e modalidade (dados mensais).
    
    Args:
        top: Quantidade máxima de registros (padrão: 1000)
    
    Returns:
        DataFrame com taxas de juros bancários
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
        if "Data" in df.columns:
            df["Data"] = pd.to_datetime(df["Data"])
        logger.info(f"Taxas de juros carregadas: {len(df)} registros.")
        return df
    except Exception as e:
        logger.exception(f"Erro ao buscar taxas de juros: {e}")
        raise


def calendario(meses: int = 3) -> pd.DataFrame:
    """
    Gera uma estimativa do calendário econômico com as próximas divulgações.
    
    Como o BACEN não disponibiliza uma API específica de calendário, esta função
    cria uma projeção baseada nas datas típicas de divulgação dos indicadores.
    
    Args:
        meses: Quantos meses à frente considerar (padrão: 3)
    
    Returns:
        DataFrame com colunas 'data', 'indicador' e 'descricao'
    """
    try:
        logger.info(f"Gerando calendário econômico para os próximos {meses} meses...")
        
        hoje = pd.Timestamp.now()
        limite = hoje + pd.DateOffset(months=meses)
        
        eventos = []
        
        # IPCA - geralmente na segunda semana do mês
        for mes in range(1, meses + 1):
            data_ref = hoje + pd.DateOffset(months=mes)
            data_ipca = pd.Timestamp(year=data_ref.year, month=data_ref.month, day=10)
            eventos.append({
                'data': data_ipca,
                'indicador': 'IPCA',
                'descricao': f'Divulgação do IPCA de {data_ref.strftime("%m/%Y")}'
            })
            
            # Selic - reunião do COPOM (aproximadamente a cada 45 dias)
            data_copom = hoje + pd.Timedelta(days=mes * 45)
            if data_copom <= limite:
                eventos.append({
                    'data': data_copom,
                    'indicador': 'Selic',
                    'descricao': f'Reunião do COPOM ({data_copom.strftime("%d/%m/%Y")})'
                })
            
            # PIB - trimestral (final de cada trimestre)
            if mes % 3 == 0:
                data_pib = pd.Timestamp(year=data_ref.year, month=data_ref.month, day=28)
                eventos.append({
                    'data': data_pib,
                    'indicador': 'PIB',
                    'descricao': f'Divulgação do PIB do trimestre encerrado em {data_ref.strftime("%m/%Y")}'
                })
        
        df = pd.DataFrame(eventos)
        
        if len(df) == 0:
            return pd.DataFrame(columns=['data', 'indicador', 'descricao'])
        
        df = df.sort_values('data').reset_index(drop=True)
        
        logger.info(f"Calendário gerado: {len(df)} eventos.")
        return df
        
    except Exception as e:
        logger.exception(f"Erro ao gerar calendário: {e}")
        raise