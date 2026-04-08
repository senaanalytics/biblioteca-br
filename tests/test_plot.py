"""
Script de teste para o módulo de visualizacao (plot.py)
"""

from biblioteca_br import bacen, plot, analise
import matplotlib
matplotlib.use('Agg')  # Usar backend nao-interativo para testes

import os
diretorio_saida = "testes_graficos"
os.makedirs(diretorio_saida, exist_ok=True)

print("=" * 60)
print("TESTANDO MODULO DE VISUALIZACAO - biblioteca-br")
print("=" * 60)

# Teste 1: Grafico de linha com Selic
print("\n[TESTE 1] Grafico de linha - Taxa Selic")
try:
    selic_df = bacen.selic()
    print(f"[OK] Dados da Selic carregados: {len(selic_df)} registros")
    
    fig = plot.linha(
        selic_df, 
        titulo="Taxa Selic Diaria",
        ylabel="Taxa (%)",
        salvar=f"{diretorio_saida}/test_selic_linha.png",
        mostrar=False
    )
    print(f"[OK] Grafico de linha salvo em: {diretorio_saida}/test_selic_linha.png")
except Exception as e:
    print(f"[ERRO] Erro no teste 1: {e}")

# Teste 2: Grafico de barras com IPCA mensal
print("\n[TESTE 2] Grafico de barras - IPCA Mensal")
try:
    ipca_df = bacen.ipca()
    print(f"[OK] Dados do IPCA carregados: {len(ipca_df)} registros")
    
    # Pegar ultimos 12 meses
    ipca_recente = ipca_df.tail(12).copy()
    
    fig = plot.barras(
        ipca_recente,
        titulo="IPCA Mensal (Ultimos 12 meses)",
        ylabel="Variacao (%)",
        rotacao_x=45,
        salvar=f"{diretorio_saida}/test_ipca_barras.png",
        mostrar=False
    )
    print(f"[OK] Grafico de barras salvo em: {diretorio_saida}/test_ipca_barras.png")
except Exception as e:
    print(f"[ERRO] Erro no teste 2: {e}")

# Teste 3: Grafico de area
print("\n[TESTE 3] Grafico de area - Dolar")
try:
    dolar_df = bacen.cambio(moeda='USD')
    print(f"[OK] Dados do Dolar carregados: {len(dolar_df)} registros")
    
    # Pegar ultimo ano
    dolar_recente = dolar_df.tail(252).copy()  # ~252 dias uteis
    
    fig = plot.area(
        dolar_recente,
        titulo="Cotacao Dolar/Real (Ultimo Ano)",
        ylabel="R$",
        empilhado=False,
        alpha=0.6,
        salvar=f"{diretorio_saida}/test_dolar_area.png",
        mostrar=False
    )
    print(f"[OK] Grafico de area salvo em: {diretorio_saida}/test_dolar_area.png")
except Exception as e:
    print(f"[ERRO] Erro no teste 3: {e}")

# Teste 4: Grafico de dispersao (correlacao)
print("\n[TESTE 4] Grafico de dispersao - Correlacao Selic vs IPCA")
try:
    # Preparar dados comparaveis
    comparacao = analise.comparar(selic_df, ipca_df, nome1='Selic', nome2='IPCA')
    print(f"[OK] Dados alinhados: {len(comparacao)} periodos comuns")
    
    if len(comparacao) > 10:
        fig = plot.dispersao(
            comparacao['Selic'],
            comparacao['IPCA'],
            titulo="Correlacao: Selic vs IPCA",
            xlabel="Selic (%)",
            ylabel="IPCA (%)",
            ajustar_reta=True,
            mostrar_correlacao=True,
            salvar=f"{diretorio_saida}/test_dispersao_selic_ipca.png",
            mostrar=False
        )
        print(f"[OK] Grafico de dispersao salvo em: {diretorio_saida}/test_dispersao_selic_ipca.png")
    else:
        print("[AVISO] Dados insuficientes para dispersao")
except Exception as e:
    print(f"[ERRO] Erro no teste 4: {e}")

# Teste 5: Painel comparativo
print("\n[TESTE 5] Painel Comparativo - Panorama Economico")
try:
    igpm_df = bacen.igpm()
    print(f"[OK] Dados do IGP-M carregados: {len(igpm_df)} registros")
    
    fig = plot.comparativo(
        selic=selic_df,
        ipca=ipca_df,
        dolar=dolar_df,
        igpm=igpm_df,
        titulo="Panorama Economico Brasileiro",
        salvar=f"{diretorio_saida}/test_painel_comparativo.png",
        mostrar=False
    )
    print(f"[OK] Painel comparativo salvo em: {diretorio_saida}/test_painel_comparativo.png")
except Exception as e:
    print(f"[ERRO] Erro no teste 5: {e}")

# Teste 6: Funcao generica plotar()
print("\n[TESTE 6] Funcao generica plotar()")
try:
    fig = plot.plotar(
        selic_df.tail(50),
        tipo='linha',
        titulo="Selic (Ultimos 50 registros) - Funcao Generica",
        salvar=f"{diretorio_saida}/test_generica.png",
        mostrar=False
    )
    print("[OK] Funcao generica testada com sucesso")
except Exception as e:
    print(f"[ERRO] Erro no teste 6: {e}")

print("\n" + "=" * 60)
print("TODOS OS TESTES FORAM EXECUTADOS!")
print("=" * 60)
print("\nArquivos gerados:")
print(f"  - {diretorio_saida}/test_selic_linha.png")
print(f"  - {diretorio_saida}/test_ipca_barras.png")
print(f"  - {diretorio_saida}/test_dolar_area.png")
print(f"  - {diretorio_saida}/test_dispersao_selic_ipca.png")
print(f"  - {diretorio_saida}/test_painel_comparativo.png")
print(f"  - {diretorio_saida}/test_generica.png")
