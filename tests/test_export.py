"""
Teste do Módulo de Exportação - biblioteca-br
"""

import pandas as pd
from datetime import datetime, timedelta
import os

# Importar módulo de exportação
from biblioteca_br.export import excel, csv, pdf, json

# Criar DataFrame de teste
print("[INFO] Criando dados de teste...")
datas = pd.date_range(start="2023-01-01", periods=100, freq="D")
df_teste = pd.DataFrame({
    'data': datas,
    'selic': [10.5 + (i * 0.05) % 5 for i in range(100)],
    'ipca': [0.3 + (i * 0.02) % 1 for i in range(100)],
    'dolar': [5.0 + (i * 0.03) % 2 for i in range(100)],
    'volume': [1000000 + i * 50000 for i in range(100)]
})
df_teste.set_index('data', inplace=True)

print(f"[OK] DataFrame criado: {len(df_teste)} registros, {len(df_teste.columns)} colunas")
print(df_teste.head())
print()

# Diretório de saída
diretorio_saida = "testes_exportacao"
os.makedirs(diretorio_saida, exist_ok=True)

# Teste 1: Exportar para Excel
print("=" * 60)
print("TESTE 1: Exportação para Excel")
print("=" * 60)
try:
    caminho_excel = excel(
        df_teste, 
        f"{diretorio_saida}/dados_economicos.xlsx",
        nome_planilha="Indicadores"
    )
    print(f"[OK] Excel criado com sucesso: {caminho_excel}")
    tamanho = os.path.getsize(caminho_excel) / 1024
    print(f"   Tamanho: {tamanho:.2f} KB")
except Exception as e:
    print(f"[ERRO] Erro na exportação Excel: {e}")

print()

# Teste 2: Exportar para CSV
print("=" * 60)
print("TESTE 2: Exportação para CSV")
print("=" * 60)
try:
    caminho_csv = csv(
        df_teste,
        f"{diretorio_saida}/dados_economicos.csv",
        separador=';',
        decimais=',',
        codificacao='utf-8'
    )
    print(f"[OK] CSV criado com sucesso: {caminho_csv}")
    tamanho = os.path.getsize(caminho_csv) / 1024
    print(f"   Tamanho: {tamanho:.2f} KB")
    
    # Mostrar primeiras linhas
    with open(caminho_csv, 'r', encoding='utf-8') as f:
        print("   Amostra:")
        for i, linha in enumerate(f):
            if i < 3:
                print(f"   {linha.strip()}")
except Exception as e:
    print(f"[ERRO] Erro na exportação CSV: {e}")

print()

# Teste 3: Exportar para JSON
print("=" * 60)
print("TESTE 3: Exportação para JSON")
print("=" * 60)
try:
    caminho_json = json(
        df_teste.reset_index(),
        f"{diretorio_saida}/dados_economicos.json",
        orient='records',
        indent=2
    )
    print(f"[OK] JSON criado com sucesso: {caminho_json}")
    tamanho = os.path.getsize(caminho_json) / 1024
    print(f"   Tamanho: {tamanho:.2f} KB")
    
    # Mostrar início do arquivo
    with open(caminho_json, 'r', encoding='utf-8') as f:
        conteudo = f.read(200)
        print(f"   Amostra: {conteudo}...")
except Exception as e:
    print(f"[ERRO] Erro na exportação JSON: {e}")

print()

# Teste 4: Exportar para PDF (sem gráfico)
print("=" * 60)
print("TESTE 4: Exportação para PDF (apenas tabela)")
print("=" * 60)
try:
    caminho_pdf = pdf(
        df_teste.reset_index(),
        f"{diretorio_saida}/relatorio_simples.pdf",
        titulo="Relatório de Indicadores Econômicos",
        subtitulo="Período: Janeiro a Abril 2023",
        incluir_grafico=False
    )
    print(f"[OK] PDF criado com sucesso: {caminho_pdf}")
    tamanho = os.path.getsize(caminho_pdf) / 1024
    print(f"   Tamanho: {tamanho:.2f} KB")
except Exception as e:
    print(f"[ERRO] Erro na exportação PDF: {e}")

print()

# Teste 5: Exportar para PDF (com gráfico)
print("=" * 60)
print("TESTE 5: Exportação para PDF (com gráfico)")
print("=" * 60)
try:
    caminho_pdf_completo = pdf(
        df_teste.reset_index(),
        f"{diretorio_saida}/relatorio_completo.pdf",
        titulo="Relatório Completo - Indicadores Econômicos",
        subtitulo="Análise com Gráficos Integrados",
        incluir_grafico=True,
        colunas_grafico=['selic', 'ipca', 'dolar'],
        autor="Teste biblioteca-br"
    )
    print(f"[OK] PDF com gráfico criado com sucesso: {caminho_pdf_completo}")
    tamanho = os.path.getsize(caminho_pdf_completo) / 1024
    print(f"   Tamanho: {tamanho:.2f} KB")
except Exception as e:
    print(f"[ERRO] Erro na exportação PDF com gráfico: {e}")

print()

# Teste 6: Usando aliases
print("=" * 60)
print("TESTE 6: Usando aliases (to_excel, to_csv, etc.)")
print("=" * 60)
try:
    from biblioteca_br.export import to_excel, to_csv, to_json, to_pdf
    
    to_excel(df_teste.head(10), f"{diretorio_saida}/amostra.xlsx")
    to_csv(df_teste.head(10), f"{diretorio_saida}/amostra.csv")
    to_json(df_teste.head(10).reset_index(), f"{diretorio_saida}/amostra.json")
    
    print("[OK] Aliases funcionam corretamente!")
except Exception as e:
    print(f"[ERRO] Erro com aliases: {e}")

print()

# Resumo final
print("=" * 60)
print("RESUMO DOS ARQUIVOS GERADOS")
print("=" * 60)
arquivos = os.listdir(diretorio_saida)
for arquivo in sorted(arquivos):
    caminho_completo = os.path.join(diretorio_saida, arquivo)
    tamanho = os.path.getsize(caminho_completo) / 1024
    print(f"   [ARQUIVO] {arquivo:30s} {tamanho:8.2f} KB")

print()
print("=" * 60)
print("[OK] TODOS OS TESTES DE EXPORTAÇÃO FORAM CONCLUÍDOS!")
print("=" * 60)
