# src/biblioteca_br/b3.py

import logging
import yfinance as yf
import pandas as pd
from typing import Optional, List, Union

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Função para o Ibovespa
# ----------------------------------------------------------------------
def ibovespa(inicio: Optional[str] = None, fim: Optional[str] = None) -> pd.DataFrame:
    """
    Retorna o histórico do índice Ibovespa (^BVSP).
    
    Args:
        : Data de início no formato 'YYYY-MM-DD'.
        fim (str, opcional): Data de fim no formato 'YYYY-MM-DD'.
    
    Returns:
        DataFrame: DataFrame com as colunas padrão do yfinance (Open, High, Low, Close, Volume).
    """
    ticker = "^BVSP"
    logger.info(f"Buscando dados do Ibovespa ({ticker})...")
    try:
        df = yf.download(ticker, start=inicio, end=fim, progress=False)
        if df.empty:
            raise ValueError("Nenhum dado retornado para o Ibovespa.")
        logger.info(f"Dados obtidos: {len(df)} registros.")
        return df
    except Exception as e:
        logger.exception(f"Erro ao obter dados do Ibovespa: {e}")
        raise

# ----------------------------------------------------------------------
# Função para uma ação
# ----------------------------------------------------------------------
def acao(ticker: str, inicio: Optional[str] = None, fim: Optional[str] = None) -> pd.DataFrame:
    """
    Retorna o histórico de uma ação da B3.
    
    Args:
        : Código da ação (ex: 'PETR4', 'VALE3'). 
                      O código deve ser informado sem o '.SA', a função adiciona automaticamente.
        inicio (str, opcional): Data de início.
        fim (str, opcional): Data de fim.
    
    Returns:
        DataFrame: DataFrame com histórico de preços.
    """
    # Garante que o ticker tenha o sufixo .SA (B3)
    if not ticker.endswith('.SA'):
        ticker_b3 = f"{ticker}.SA"
    else:
        ticker_b3 = ticker
    
    logger.info(f"Buscando dados da ação {ticker_b3}...")
    try:
        df = yf.download(ticker_b3, start=inicio, end=fim, progress=False)
        if df.empty:
            raise ValueError(f"Nenhum dado retornado para {ticker_b3}.")
        logger.info(f"Dados obtidos para {ticker_b3}: {len(df)} registros.")
        return df
    except Exception as e:
        logger.exception(f"Erro ao obter dados da ação {ticker_b3}: {e}")
        raise

# ----------------------------------------------------------------------
# Função para múltiplas ações
# ----------------------------------------------------------------------
def acoes(tickers: List[str], inicio: Optional[str] = None, fim: Optional[str] = None) -> pd.DataFrame:
    """
    Retorna o histórico de múltiplas ações da B3 em um único DataFrame.
    
    Args:
        : Lista de códgos de ações (ex: ['PETR4', 'VALE3']).
        inicio (str, opcional): Data de início.
        fim (str, opcional): Data de fim.
    
    Returns:
        DataFrame: DataFrame com MultiIndex (ticker, coluna) ou com tickers como colunas.
    """
    tickers_b3 = [t if t.endswith('.SA') else f"{t}.SA" for t in tickers]
    logger.info(f"Buscando dados para múltiplas ações: {tickers_b3}")
    try:
        df = yf.download(tickers_b3, start=inicio, end=fim, progress=False)
        if df.empty:
            raise ValueError("Nenhum dado retornado para as ações.")
        logger.info(f"Dados obtidos para {len(tickers_b3)} ações.")
        return df
    except Exception as e:
        logger.exception(f"Erro ao obter dados das ações: {e}")
        raise