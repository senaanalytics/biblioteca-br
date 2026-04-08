"""
Módulo de Visualização - biblioteca-br

Funções para criação de gráficos prontos (linha, barras, área, dispersão)
e painéis comparativos com dados econômicos.

Autor: Isaque Sena
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Union, List, Optional, Tuple
from datetime import datetime

# Configurar estilo padrão
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14


def linha(df: pd.DataFrame, 
          colunas: Optional[Union[str, List[str]]] = None,
          coluna_data: str = 'data',
          titulo: str = '',
          xlabel: str = 'Data',
          ylabel: str = 'Valor',
          figsize: Tuple[int, int] = (12, 6),
          grid: bool = True,
          legenda: bool = True,
          rotacao_x: int = 0,
          salvar: Optional[str] = None,
          mostrar: bool = True) -> plt.Figure:
    """
    Cria um gráfico de linha para séries temporais.
    
    Args:
        df: DataFrame com os dados
        colunas: Nome(s) da(s) coluna(s) a plotar (usa todas as numéricas se None)
        coluna_data: Nome da coluna de data (padrão: 'data')
        titulo: Título do gráfico
        xlabel: Rótulo do eixo X
        ylabel: Rótulo do eixo Y
        figsize: Tamanho da figura (largura, altura)
        grid: Mostrar grade
        legenda: Mostrar legenda
        rotacao_x: Rotação dos rótulos do eixo X em graus
        salvar: Caminho para salvar a figura (opcional)
        mostrar: Mostrar o gráfico (padrão: True)
    
    Returns:
        A figura criada
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Identificar colunas para plotar
    if colunas is None:
        colunas_para_plotar = df.select_dtypes(include=[np.number]).columns.tolist()
    elif isinstance(colunas, str):
        colunas_para_plotar = [colunas]
    else:
        colunas_para_plotar = colunas
    
    # Verificar se há coluna de data
    if coluna_data not in df.columns:
        # Tentar usar o índice como data
        x_values = df.index
        if isinstance(df.index[0], (pd.Timestamp, datetime)):
            eh_data = True
        else:
            eh_data = False
    else:
        x_values = df[coluna_data]
        eh_data = True
    
    # Plotar cada coluna
    for coluna in colunas_para_plotar:
        if coluna in df.columns:
            if eh_data:
                ax.plot(x_values, df[coluna], label=coluna, marker='o', markersize=4, linewidth=2)
            else:
                ax.plot(x_values, df[coluna], label=coluna, marker='o', markersize=4, linewidth=2)
    
    # Formatar eixo X se for data
    if eh_data and len(df) > 0:
        try:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=max(1, len(df)//12)))
            plt.xticks(rotation=rotacao_x)
        except:
            plt.xticks(rotation=rotacao_x)
    else:
        plt.xticks(rotation=rotacao_x)
    
    # Configurar labels e título
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    if titulo:
        ax.set_title(titulo, fontsize=14, fontweight='bold')
    
    # Grade
    if grid:
        ax.grid(True, alpha=0.3, linestyle='--')
    
    # Legenda
    if legenda and len(colunas_para_plotar) > 1:
        ax.legend(loc='best', framealpha=0.9)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar se especificado
    if salvar:
        fig.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    # Mostrar se solicitado
    if mostrar:
        plt.show()
    
    return fig


def barras(df: pd.DataFrame,
           colunas: Optional[Union[str, List[str]]] = None,
           coluna_data: str = 'data',
           titulo: str = '',
           xlabel: str = 'Categoria',
           ylabel: str = 'Valor',
           figsize: Tuple[int, int] = (12, 6),
           horizontal: bool = False,
           empilhado: bool = False,
           grid: bool = True,
           legenda: bool = True,
           rotacao_x: int = 45,
           salvar: Optional[str] = None,
           mostrar: bool = True) -> plt.Figure:
    """
    Cria um gráfico de barras (verticais ou horizontais).
    
    Args:
        : DataFrame com os dados.
        colunas (str ou list): Nome(s) da(s) coluna(s) a plotar.
        coluna_data (str): Nome da coluna para categorias/eixo X.
        titulo (str): Título do gráfico.
        xlabel (str): Rótulo do eixo X.
        ylabel (str): Rótulo do eixo Y.
        figsize (tuple): Tamanho da figura.
        horizontal (bool): Gráfico de barras horizontais.
        empilhado (bool): Barras empilhadas (para múltiplas colunas).
        grid (bool): Mostrar grade.
        legenda (bool): Mostrar legenda.
        rotacao_x (int): Rotação dos rótulos do eixo X.
        salvar (str): Caminho para salvar a figura.
        mostrar (bool): Mostrar o gráfico.
    
    Returns:
        A figura criada: A figura criada.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Identificar colunas para plotar
    if colunas is None:
        colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        colunas_para_plotar = [c for c in colunas_numericas if c != coluna_data]
    elif isinstance(colunas, str):
        colunas_para_plotar = [colunas]
    else:
        colunas_para_plotar = colunas
    
    # Preparar dados
    if coluna_data in df.columns:
        x_labels = df[coluna_data].astype(str).tolist()
    else:
        x_labels = df.index.astype(str).tolist()
    
    x_positions = np.arange(len(x_labels))
    width = 0.8 / len(colunas_para_plotar) if len(colunas_para_plotar) > 1 else 0.8
    
    # Plotar barras
    for i, coluna in enumerate(colunas_para_plotar):
        if coluna in df.columns:
            valores = df[coluna].values
            
            if horizontal:
                if empilhado and i > 0:
                    left = np.cumsum([df[colunas_para_plotar[j]].values for j in range(i)], axis=0)[-1]
                    ax.barh(x_positions, valores, left=left, height=width, label=coluna)
                else:
                    offset = (i - len(colunas_para_plotar)/2 + 0.5) * width
                    ax.barh(x_positions + offset, valores, height=width, label=coluna)
            else:
                if empilhado and i > 0:
                    bottom = np.cumsum([df[colunas_para_plotar[j]].values for j in range(i)], axis=0)[-1]
                    ax.bar(x_positions, valores, width=width, bottom=bottom, label=coluna)
                else:
                    offset = (i - len(colunas_para_plotar)/2 + 0.5) * width
                    ax.bar(x_positions + offset, valores, width=width, label=coluna)
    
    # Configurar eixos
    if horizontal:
        ax.set_yticks(x_positions)
        ax.set_yticklabels(x_labels, rotation=rotacao_x)
        ax.set_xlabel(ylabel, fontsize=12)
        ax.set_ylabel(xlabel, fontsize=12)
    else:
        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_labels, rotation=rotacao_x, ha='right')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
    
    # Título
    if titulo:
        ax.set_title(titulo, fontsize=14, fontweight='bold')
    
    # Grade
    if grid:
        axis = 'y' if not horizontal else 'x'
        ax.grid(axis=axis, alpha=0.3, linestyle='--')
    
    # Legenda
    if legenda and len(colunas_para_plotar) > 1:
        ax.legend(loc='best', framealpha=0.9)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar se especificado
    if salvar:
        fig.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    # Mostrar se solicitado
    if mostrar:
        plt.show()
    
    return fig


def area(df: pd.DataFrame,
         colunas: Optional[Union[str, List[str]]] = None,
         coluna_data: str = 'data',
         titulo: str = '',
         xlabel: str = 'Data',
         ylabel: str = 'Valor',
         figsize: Tuple[int, int] = (12, 6),
         empilhado: bool = True,
         alpha: float = 0.7,
         grid: bool = True,
         legenda: bool = True,
         salvar: Optional[str] = None,
         mostrar: bool = True) -> plt.Figure:
    """
    Cria um gráfico de área (preenchido).
    
    Args:
        : DataFrame com os dados.
        colunas (str ou list): Nome(s) da(s) coluna(s) a plotar.
        coluna_data (str): Nome da coluna de data.
        titulo (str): Título do gráfico.
        xlabel (str): Rótulo do eixo X.
        ylabel (str): Rótulo do eixo Y.
        figsize (tuple): Tamanho da figura.
        empilhado (bool): Áreas empilhadas.
        alpha (float): Transparência (0-1).
        grid (bool): Mostrar grade.
        legenda (bool): Mostrar legenda.
        salvar (str): Caminho para salvar a figura.
        mostrar (bool): Mostrar o gráfico.
    
    Returns:
        A figura criada: A figura criada.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Identificar colunas para plotar
    if colunas is None:
        colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        colunas_para_plotar = [c for c in colunas_numericas if c != coluna_data]
    elif isinstance(colunas, str):
        colunas_para_plotar = [colunas]
    else:
        colunas_para_plotar = colunas
    
    # Preparar dados
    if coluna_data in df.columns:
        x_values = df[coluna_data]
    else:
        x_values = df.index
    
    # Plotar áreas
    dados_para_area = df[colunas_para_plotar].values.T
    
    if empilhado:
        ax.stackplot(x_values, dados_para_area, labels=colunas_para_plotar, alpha=alpha)
    else:
        for i, coluna in enumerate(colunas_para_plotar):
            ax.fill_between(x_values, df[coluna].values, alpha=alpha, label=coluna)
    
    # Configurar labels
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    if titulo:
        ax.set_title(titulo, fontsize=14, fontweight='bold')
    
    # Grade
    if grid:
        ax.grid(True, alpha=0.3, linestyle='--')
    
    # Legenda
    if legenda and len(colunas_para_plotar) > 1:
        ax.legend(loc='best', framealpha=0.9)
    
    # Formatar eixo X se for data
    if isinstance(x_values.iloc[0] if hasattr(x_values, 'iloc') else x_values[0], (pd.Timestamp, datetime)):
        try:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=max(1, len(df)//12)))
            plt.xticks(rotation=45)
        except:
            plt.xticks(rotation=45)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar se especificado
    if salvar:
        fig.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    # Mostrar se solicitado
    if mostrar:
        plt.show()
    
    return fig


def dispersao(x: pd.Series, y: pd.Series,
              titulo: str = '',
              xlabel: str = 'X',
              ylabel: str = 'Y',
              figsize: Tuple[int, int] = (10, 8),
              ajustar_reta: bool = True,
              cor_pontos: str = 'blue',
              alpha: float = 0.6,
              tamanho_pontos: int = 50,
              grid: bool = True,
              mostrar_correlacao: bool = True,
              salvar: Optional[str] = None,
              mostrar: bool = True) -> plt.Figure:
    """
    Cria um gráfico de dispersão entre duas variáveis.
    
    Args:
        : Série para eixo X.
        y (pd.Series): Série para eixo Y.
        titulo (str): Título do gráfico.
        xlabel (str): Rótulo do eixo X.
        ylabel (str): Rótulo do eixo Y.
        figsize (tuple): Tamanho da figura.
        ajustar_reta (bool): Adicionar linha de regressão linear.
        cor_pontos (str): Cor dos pontos.
        alpha (float): Transparência dos pontos.
        tamanho_pontos (int): Tamanho dos pontos.
        grid (bool): Mostrar grade.
        mostrar_correlacao (bool): Exibir coeficiente de correlação no gráfico.
        salvar (str): Caminho para salvar a figura.
        mostrar (bool): Mostrar o gráfico.
    
    Returns:
        A figura criada: A figura criada.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Remover valores NaN
    mask = x.notna() & y.notna()
    x_clean = x[mask]
    y_clean = y[mask]
    
    # Plotar pontos
    ax.scatter(x_clean, y_clean, c=cor_pontos, alpha=alpha, s=tamanho_pontos, edgecolors='black', linewidth=0.5)
    
    # Ajustar reta de regressão
    if ajustar_reta and len(x_clean) > 1:
        coeficientes = np.polyfit(x_clean, y_clean, 1)
        reta = np.poly1d(coeficientes)
        x_ajuste = np.linspace(x_clean.min(), x_clean.max(), 100)
        ax.plot(x_ajuste, reta(x_ajuste), 'r--', linewidth=2, label=f'Regressão Linear')
        
        # Calcular e mostrar correlação
        if mostrar_correlacao:
            correlacao = x_clean.corr(y_clean)
            texto_corr = f'Correlação: {correlacao:.4f}'
            ax.text(0.05, 0.95, texto_corr, transform=ax.transAxes, fontsize=12,
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Labels e título
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    if titulo:
        ax.set_title(titulo, fontsize=14, fontweight='bold')
    
    # Grade
    if grid:
        ax.grid(True, alpha=0.3, linestyle='--')
    
    # Legenda
    if ajustar_reta:
        ax.legend(loc='best', framealpha=0.9)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar se especificado
    if salvar:
        fig.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {salvar}")
    
    # Mostrar se solicitado
    if mostrar:
        plt.show()
    
    return fig


def comparativo(selic: Optional[pd.DataFrame] = None,
                ipca: Optional[pd.DataFrame] = None,
                dolar: Optional[pd.DataFrame] = None,
                igpm: Optional[pd.DataFrame] = None,
                titulo: str = 'Panorama Econômico Brasileiro',
                figsize: Tuple[int, int] = (14, 10),
                salvar: Optional[str] = None,
                mostrar: bool = True) -> plt.Figure:
    """
    Cria um painel 2x2 com os principais indicadores econômicos.
    
    Args:
        : DataFrame com dados da Selic.
        ipca (pd.DataFrame): DataFrame com dados do IPCA.
        dolar (pd.DataFrame): DataFrame com dados do Dólar.
        igpm (pd.DataFrame): DataFrame com dados do IGP-M.
        titulo (str): Título geral do painel.
        figsize (tuple): Tamanho da figura.
        salvar (str): Caminho para salvar a figura.
        mostrar (bool): Mostrar o gráfico.
    
    Returns:
        A figura criada: A figura criada com 4 subplots.
    """
    # Importar bacen para buscar dados se não fornecidos
    from . import bacen
    
    # Buscar dados se não fornecidos
    if selic is None:
        try:
            selic = bacen.selic()
        except:
            selic = None
    
    if ipca is None:
        try:
            ipca = bacen.ipca()
        except:
            ipca = None
    
    if dolar is None:
        try:
            dolar = bacen.cambio(moeda='USD')
        except:
            dolar = None
    
    if igpm is None:
        try:
            igpm = bacen.igpm()
        except:
            igpm = None
    
    # Criar figura com 4 subplots
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle(titulo, fontsize=16, fontweight='bold')
    
    # Configurar cada subplot
    indicadores = [
        (selic, 'Selic', 'Taxa Selic (%)', axes[0, 0]),
        (ipca, 'IPCA', 'IPCA (%)', axes[0, 1]),
        (dolar, 'Dólar', 'USD/BRL (R$)', axes[1, 0]),
        (igpm, 'IGP-M', 'IGP-M (%)', axes[1, 1])
    ]
    
    for dados, nome, ylabel, ax in indicadores:
        if dados is not None and len(dados) > 0:
            # Identificar colunas
            col_data = 'data' if 'data' in dados.columns else dados.columns[0]
            col_valor = 'valor' if 'valor' in dados.columns else dados.columns[1]
            
            # Plotar linha
            ax.plot(dados[col_data], dados[col_valor], linewidth=2, marker='o', markersize=3)
            ax.set_title(f'{nome}', fontsize=14, fontweight='bold')
            ax.set_xlabel('Data')
            ax.set_ylabel(ylabel)
            ax.grid(True, alpha=0.3, linestyle='--')
            
            # Formatar eixo X
            try:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                ax.xaxis.set_major_locator(mdates.MonthLocator(interval=max(1, len(dados)//12)))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            except:
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        else:
            ax.text(0.5, 0.5, f'Dados de {nome}\nindisponíveis', 
                   transform=ax.transAxes, ha='center', va='center', fontsize=12)
            ax.set_title(f'{nome}', fontsize=14, fontweight='bold')
            ax.grid(False)
    
    # Ajustar layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Salvar se especificado
    if salvar:
        fig.savefig(salvar, dpi=300, bbox_inches='tight')
        print(f"Painel salvo em: {salvar}")
    
    # Mostrar se solicitado
    if mostrar:
        plt.show()
    
    return fig


# Função de conveniência para criar todos os tipos de gráficos rapidamente
def plotar(df: pd.DataFrame, tipo: str = 'linha', **kwargs) -> plt.Figure:
    """
    Função genérica para criar diferentes tipos de gráficos.
    
    Args:
        : DataFrame com os dados.
        tipo (str): Tipo de gráfico ('linha', 'barra', 'area', 'dispersao').
        **kwargs: Argumentos específicos para cada tipo de gráfico.
    
    Returns:
        A figura criada: A figura criada.
    """
    if tipo == 'linha':
        return linha(df, **kwargs)
    elif tipo == 'barra' or tipo == 'barras':
        return barras(df, **kwargs)
    elif tipo == 'area':
        return area(df, **kwargs)
    elif tipo == 'dispersao' or tipo == 'scatter':
        if 'x' in kwargs and 'y' in kwargs:
            return dispersao(kwargs['x'], kwargs['y'], **{k: v for k, v in kwargs.items() if k not in ['x', 'y']})
        else:
            raise ValueError("Para gráfico de dispersão, é necessário fornecer 'x' e 'y'.")
    else:
        raise ValueError(f"Tipo de gráfico '{tipo}' não suportado. Use: 'linha', 'barra', 'area' ou 'dispersao'.")