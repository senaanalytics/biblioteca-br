"""
Módulo de Análise - biblioteca-br

Ferramentas para análise estatística, comparação e detecção de tendências
em dados econômicos e financeiros brasileiros.

Autor: Isaque Sena
"""

import pandas as pd
import numpy as np
from typing import Union, Tuple, Optional
from . import bacen, b3


def resumo(df: pd.DataFrame, coluna_valor: str = 'valor') -> dict:
    """
    Gera um resumo estatístico completo dos dados.
    
    Args:
        df: DataFrame com os dados econômicos
        coluna_valor: Nome da coluna com os valores (padrão: 'valor')
    
    Returns:
        Dicionário com média, mínimo, máximo, variação percentual, 
        desvio padrão e quantidade de observações
    """
    if coluna_valor not in df.columns:
        raise ValueError(f"Coluna '{coluna_valor}' não encontrada no DataFrame.")
    
    valores = df[coluna_valor].dropna()
    
    if len(valores) == 0:
        return {
            'media': None,
            'minimo': None,
            'maximo': None,
            'variacao_percentual': None,
            'desvio_padrao': None,
            'observacoes': 0
        }
    
    media = valores.mean()
    minimo = valores.min()
    maximo = valores.max()
    desvio_padrao = valores.std()
    observacoes = len(valores)
    
    # Variação percentual total (do primeiro ao último valor)
    if len(valores) > 1:
        primeiro = valores.iloc[0]
        ultimo = valores.iloc[-1]
        variacao_percentual = ((ultimo - primeiro) / primeiro) * 100 if primeiro != 0 else None
    else:
        variacao_percentual = 0.0
    
    return {
        'media': round(media, 4),
        'minimo': round(minimo, 4),
        'maximo': round(maximo, 4),
        'variacao_percentual': round(variacao_percentual, 4) if variacao_percentual is not None else None,
        'desvio_padrao': round(desvio_padrao, 4),
        'observacoes': observacoes
    }


def comparar(df1: pd.DataFrame, df2: pd.DataFrame, 
             nome1: str = 'Indicador 1', nome2: str = 'Indicador 2',
             coluna_valor: str = 'valor') -> pd.DataFrame:
    """
    Compara dois indicadores alinhando-os por data.
    
    Args:
        df1: Primeiro DataFrame
        df2: Segundo DataFrame
        nome1: Rótulo para o primeiro indicador
        nome2: Rótulo para o segundo indicador
        coluna_valor: Nome da coluna com os valores
    
    Returns:
        DataFrame com ambos os indicadores lado a lado
    """
    # Identificar coluna de data
    col_data1 = 'data' if 'data' in df1.columns else df1.columns[0]
    col_data2 = 'data' if 'data' in df2.columns else df2.columns[0]
    
    # Renomear colunas de valor
    df1_copy = df1.copy()
    df2_copy = df2.copy()
    
    df1_copy = df1_copy.rename(columns={coluna_valor: nome1})
    df2_copy = df2_copy.rename(columns={coluna_valor: nome2})
    
    # Mesclar por data
    df_comparado = pd.merge(
        df1_copy[[col_data1, nome1]],
        df2_copy[[col_data2, nome2]],
        on=col_data1 if col_data1 == col_data2 else ('left_on', 'right_on'),
        left_on=col_data1 if col_data1 != col_data2 else None,
        right_on=col_data2 if col_data1 != col_data2 else None,
        how='inner'
    )
    
    # Se as colunas de data tinham nomes diferentes, remover a duplicada e renomear
    if col_data1 != col_data2:
        df_comparado = df_comparado.drop(columns=[col_data2])
        df_comparado = df_comparado.rename(columns={col_data1: 'data'})
    else:
        # Se já têm o mesmo nome, apenas garantir que se chama 'data'
        if col_data1 != 'data':
            df_comparado = df_comparado.rename(columns={col_data1: 'data'})
    
    # Ordenar por data
    df_comparado = df_comparado.sort_values(by='data').reset_index(drop=True)
    
    return df_comparado


def correlacao(df1: pd.DataFrame, df2: pd.DataFrame,
               coluna_valor: str = 'valor') -> dict:
    """
    Calcula a correlação entre dois indicadores.
    
    Args:
        df1: Primeiro DataFrame
        df2: Segundo DataFrame
        coluna_valor: Nome da coluna com os valores
    
    Returns:
        Dicionário com coeficiente de correlação de Pearson,
        número de observações e interpretação do resultado
    """
    # Identificar coluna de data
    col_data1 = 'data' if 'data' in df1.columns else df1.columns[0]
    col_data2 = 'data' if 'data' in df2.columns else df2.columns[0]
    
    # Mesclar por data
    df_merged = pd.merge(
        df1[[col_data1, coluna_valor]],
        df2[[col_data2, coluna_valor]],
        left_on=col_data1,
        right_on=col_data2,
        how='inner',
        suffixes=('_1', '_2')
    )
    
    if len(df_merged) < 2:
        return {
            'coeficiente_correlacao': None,
            'observacoes': len(df_merged),
            'interpretacao': 'Dados insuficientes para calcular correlação'
        }
    
    # Calcular correlação
    correlacao_pearson = df_merged[f'{coluna_valor}_1'].corr(df_merged[f'{coluna_valor}_2'])
    
    # Interpretar correlação
    if correlacao_pearson is None or np.isnan(correlacao_pearson):
        interpretacao = 'Não foi possível calcular correlação'
    elif abs(correlacao_pearson) >= 0.7:
        interpretacao = 'Correlação forte' + (' positiva' if correlacao_pearson > 0 else ' negativa')
    elif abs(correlacao_pearson) >= 0.4:
        interpretacao = 'Correlação moderada' + (' positiva' if correlacao_pearson > 0 else ' negativa')
    else:
        interpretacao = 'Correlação fraca' + (' positiva' if correlacao_pearson > 0 else ' negativa')
    
    return {
        'coeficiente_correlacao': round(correlacao_pearson, 4) if correlacao_pearson is not None else None,
        'observacoes': len(df_merged),
        'interpretacao': interpretacao
    }


def tendencia(df: pd.DataFrame, coluna_valor: str = 'valor',
              periodo_minimo: int = 5) -> dict:
    """
    Identifica se um indicador está em tendência de alta, baixa ou lateral.
    
    Args:
        df: DataFrame com os dados
        coluna_valor: Nome da coluna com os valores
        periodo_minimo: Mínimo de observações necessárias
    
    Returns:
        Dicionário com direção, força da tendência e estatísticas relacionadas
    """
    valores = df[coluna_valor].dropna()
    
    if len(valores) < periodo_minimo:
        return {
            'direcao': 'insuficiente_dados',
            'forca': None,
            'mensagem': f'Dados insuficientes (mínimo de {periodo_minimo} observações necessárias)'
        }
    
    # Calcular regressão linear simples
    x = np.arange(len(valores))
    y = valores.values
    
    # Evitar divisão por zero
    if len(x) < 2:
        return {
            'direcao': 'insuficiente_dados',
            'forca': None,
            'mensagem': 'Dados insuficientes para análise de tendência'
        }
    
    # Coeficiente angular da regressão linear
    slope = np.polyfit(x, y, 1)[0]
    
    # Calcular variação percentual total
    primeiro = valores.iloc[0]
    ultimo = valores.iloc[-1]
    variacao_total = ((ultimo - primeiro) / primeiro) * 100 if primeiro != 0 else 0
    
    # Determinar direção
    if abs(slope) < 0.0001:
        direcao = 'lateral'
    elif slope > 0:
        direcao = 'alta'
    else:
        direcao = 'baixa'
    
    # Calcular força da tendência (R²)
    y_pred = np.polyval(np.polyfit(x, y, 1), x)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    # Classificar força
    if r_squared >= 0.7:
        forca = 'forte'
    elif r_squared >= 0.4:
        forca = 'moderada'
    else:
        forca = 'fraca'
    
    return {
        'direcao': direcao,
        'forca': forca,
        'coeficiente_angular': round(slope, 6),
        'variacao_percentual_total': round(variacao_total, 4),
        'r_quadrado': round(r_squared, 4),
        'observacoes': len(valores)
    }


def panorama() -> pd.DataFrame:
    """
    Retorna todos os principais indicadores econômicos consolidados.
    
    Returns:
        DataFrame com Selic, IPCA, Dólar e IGP-M no mesmo conjunto
    """
    try:
        # Buscar dados recentes (últimos 12 meses aproximadamente)
        selic_df = bacen.selic()
        ipca_df = bacen.ipca()
        dolar_df = bacen.cambio(moeda='USD')
        igpm_df = bacen.igpm()
        
        # Identificar colunas de data
        def get_data_col(df):
            return 'data' if 'data' in df.columns else df.columns[0]
        
        # Preparar cada indicador
        indicadores = {}
        
        # Selic
        col_data_selic = get_data_col(selic_df)
        selic_prepare = selic_df.rename(columns={'valor': 'Selic'})
        indicadores['Selic'] = selic_prepare[[col_data_selic, 'Selic']].copy()
        indicadores['Selic'].rename(columns={col_data_selic: 'data'}, inplace=True)
        
        # IPCA
        col_data_ipca = get_data_col(ipca_df)
        ipca_prepare = ipca_df.rename(columns={'valor': 'IPCA'})
        indicadores['IPCA'] = ipca_prepare[[col_data_ipca, 'IPCA']].copy()
        indicadores['IPCA'].rename(columns={col_data_ipca: 'data'}, inplace=True)
        
        # Dólar
        col_data_dolar = get_data_col(dolar_df)
        dolar_prepare = dolar_df.rename(columns={'valor': 'Dolar_USD'})
        indicadores['Dolar'] = dolar_prepare[[col_data_dolar, 'Dolar_USD']].copy()
        indicadores['Dolar'].rename(columns={col_data_dolar: 'data'}, inplace=True)
        
        # IGP-M
        col_data_igpm = get_data_col(igpm_df)
        igpm_prepare = igpm_df.rename(columns={'valor': 'IGPM'})
        indicadores['IGPM'] = igpm_prepare[[col_data_igpm, 'IGPM']].copy()
        indicadores['IGPM'].rename(columns={col_data_igpm: 'data'}, inplace=True)
        
        # Começar com o indicador que tem mais dados (geralmente Selic ou Dólar)
        df_panorama = indicadores['Selic'].copy()
        
        # Mesclar os demais
        for nome, df_ind in indicadores.items():
            if nome != 'Selic':
                df_panorama = pd.merge(
                    df_panorama,
                    df_ind,
                    on='data',
                    how='outer'
                )
        
        # Ordenar por data
        df_panorama = df_panorama.sort_values('data').reset_index(drop=True)
        
        return df_panorama
        
    except Exception as e:
        raise Exception(f"Erro ao gerar panorama: {str(e)}")


def _obter_ipca_acumulado() -> pd.DataFrame:
    """
    Função interna para obter série do IPCA para cálculos de deflação.
    """
    return bacen.ipca(inicio="01/01/2010")


def deflacionar(df: pd.DataFrame, coluna_valor: str = 'valor', 
                coluna_data: str = 'data', indice: str = 'IPCA') -> pd.DataFrame:
    """
    Remove o efeito da inflação de uma série de valores nominais.
    
    Converte valores para poder de compra da data mais recente usando IPCA.
    
    Args:
        df: DataFrame com valores nominais e datas
        coluna_valor: Nome da coluna com os valores nominais
        coluna_data: Nome da coluna com as datas
        indice: Índice de inflação a usar (apenas 'IPCA' disponível)
    
    Returns:
        DataFrame original com coluna adicional 'valor_real'
    """
    if coluna_valor not in df.columns:
        raise ValueError(f"Coluna '{coluna_valor}' não encontrada no DataFrame.")
    if coluna_data not in df.columns:
        raise ValueError(f"Coluna '{coluna_data}' não encontrada no DataFrame.")
    
    # Obter série do índice de inflação
    if indice.upper() == 'IPCA':
        ipca_df = _obter_ipca_acumulado()
        col_data_ipca = 'data' if 'data' in ipca_df.columns else ipca_df.columns[0]
        col_valor_ipca = 'valor' if 'valor' in ipca_df.columns else ipca_df.columns[1]
    else:
        raise ValueError(f"Índice '{indice}' não suportado. Use apenas 'IPCA'.")
    
    # Criar cópia do DataFrame original
    df_result = df.copy()
    df_result[coluna_data] = pd.to_datetime(df_result[coluna_data])
    
    # Obter último valor do índice (base para deflação)
    ipca_max_date = ipca_df[col_data_ipca].max()
    ipca_base = ipca_df[ipca_df[col_data_ipca] == ipca_max_date][col_valor_ipca].values[0]
    
    # Função para calcular valor real
    def calcular_valor_real(row):
        data_row = row[coluna_data]
        valor_nominal = row[coluna_valor]
        
        # Encontrar valor do IPCA na data mais próxima anterior ou igual
        ipca_filtrado = ipca_df[ipca_df[col_data_ipca] <= data_row]
        if len(ipca_filtrado) == 0:
            # Se não há dado anterior, usar o primeiro disponível
            ipca_periodo = ipca_df[col_valor_ipca].min()
        else:
            ipca_periodo = ipca_filtrado[col_valor_ipca].iloc[-1]
        
        # Calcular valor real
        valor_real = valor_nominal * (ipca_base / ipca_periodo)
        return valor_real
    
    # Aplicar cálculo
    df_result['valor_real'] = df_result.apply(calcular_valor_real, axis=1)
    
    return df_result


def atualizar_monetario(valor: float, data_origem: str, 
                        data_destino: str = None, indice: str = 'IPCA') -> float:
    """
    Atualiza um valor monetário de uma data para outra usando inflação.
    
    Args:
        valor: Valor nominal a ser atualizado
        data_origem: Data de origem ('YYYY-MM-DD' ou 'DD/MM/YYYY')
        data_destino: Data de destino (opcional - usa data mais recente)
        indice: Índice de inflação (apenas 'IPCA' disponível)
    
    Returns:
        Valor atualizado
    
    Exemplo:
        >>> atualizar_monetario(1000, '2020-01-01')
        1234.56  # R$ 1.000 em jan/2020 atualizados para hoje
    """
    # Obter série do índice
    if indice.upper() == 'IPCA':
        ipca_df = _obter_ipca_acumulado()
        col_data = 'data' if 'data' in ipca_df.columns else ipca_df.columns[0]
        col_valor = 'valor' if 'valor' in ipca_df.columns else ipca_df.columns[1]
    else:
        raise ValueError(f"Índice '{indice}' não suportado. Use apenas 'IPCA'.")
    
    # Converter datas
    data_origem_dt = pd.to_datetime(data_origem, dayfirst=False)
    if data_destino:
        data_destino_dt = pd.to_datetime(data_destino, dayfirst=False)
    else:
        data_destino_dt = ipca_df[col_data].max()
    
    # Encontrar valores do índice nas datas
    ipca_origem_df = ipca_df[ipca_df[col_data] <= data_origem_dt]
    if len(ipca_origem_df) == 0:
        raise ValueError(f"Não há dados do índice anteriores a {data_origem}")
    ipca_origem = ipca_origem_df[col_valor].iloc[-1]
    
    ipca_destino_df = ipca_df[ipca_df[col_data] <= data_destino_dt]
    if len(ipca_destino_df) == 0:
        raise ValueError(f"Não há dados do índice anteriores a {data_destino}")
    ipca_destino = ipca_destino_df[col_valor].iloc[-1]
    
    # Calcular valor atualizado
    valor_atualizado = valor * (ipca_destino / ipca_origem)
    
    return round(valor_atualizado, 2)
