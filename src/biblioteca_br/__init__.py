from .bacen import selic, ipca as bacen_ipca, igpm, cambio, expectativas, juros_bancos
from .b3 import ibovespa, acao, acoes
from .ibge import pib, desemprego, populacao, ipca as ibge_ipca
from .analise import resumo, comparar, correlacao, tendencia, panorama
from .plot import linha, barras, area, dispersao, comparativo, plotar
from .export import excel, csv, pdf, json, to_excel, to_csv, to_pdf, to_json

# Alias para módulo exportar
import sys
from types import ModuleType

# Criar módulo virtual 'exportar' para acesso via biblioteca_br.exportar
exportar = ModuleType('biblioteca_br.exportar')
exportar.excel = excel
exportar.csv = csv
exportar.pdf = pdf
exportar.json = json
exportar.to_excel = to_excel
exportar.to_csv = to_csv
exportar.to_pdf = to_pdf
exportar.to_json = to_json
sys.modules['biblioteca_br.exportar'] = exportar

__version__ = '2.0.0'
__author__ = 'Isaque Sena'
__all__ = [
    # Bacen
    'selic', 'bacen_ipca', 'igpm', 'cambio', 'expectativas', 'juros_bancos',
    # B3
    'ibovespa', 'acao', 'acoes',
    # IBGE
    'pib', 'desemprego', 'populacao', 'ibge_ipca',
    # Análise
    'resumo', 'comparar', 'correlacao', 'tendencia', 'panorama',
    # Plot
    'linha', 'barras', 'area', 'dispersao', 'comparativo', 'plotar',
    # Exportação
    'excel', 'csv', 'pdf', 'json', 'to_excel', 'to_csv', 'to_pdf', 'to_json', 'exportar'
]