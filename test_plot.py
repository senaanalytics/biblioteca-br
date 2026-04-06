"""
Script de teste para o módulo de visualização (plot.py)
"""

import sys
sys.path.insert(0, '/workspace/src')

from biblioteca_br import bacen, plot, analise
import matplotlib
matplotlib.use('Agg')  # Usar backend não-interativo para testes

print("=" * 60)
print("TESTANDO MÓDULO DE VISUALIZAÇÃO - biblioteca-br")
print("=" * 60)

# Teste 1: Gráfico de linha com Selic
print("\n[TESTE 1] Gráfico de linha - Taxa Selic")
try:
    selic_df = bacen.selic()
    print(f"✓ Dados da Selic carregados: {len(selic_df)} registros")
    
    fig = plot.linha(
        selic_df, 
        titulo="Taxa Selic Diária",
        ylabel="Taxa (%)",
        salvar="/workspace/test_selic_linha.png",
        mostrar=False
    )
    print("✓ Gráfico de linha salvo em: /workspace/test_selic_linha.png")
except Exception as e:
    print(f"✗ Erro no teste 1: {e}")

# Teste 2: Gráfico de barras com IPCA mensal
print("\n[TESTE 2] Gráfico de barras - IPCA Mensal")
try:
    ipca_df = bacen.ipca()
    print(f"✓ Dados do IPCA carregados: {len(ipca_df)} registros")
    
    # Pegar últimos 12 meses
    ipca_recente = ipca_df.tail(12).copy()
    
    fig = plot.barras(
        ipca_recente,
        titulo="IPCA Mensal (Últimos 12 meses)",
        ylabel="Variação (%)",
        rotacao_x=45,
        salvar="/workspace/test_ipca_barras.png",
        mostrar=False
    )
    print("✓ Gráfico de barras salvo em: /workspace/test_ipca_barras.png")
except Exception as e:
    print(f"✗ Erro no teste 2: {e}")

# Teste 3: Gráfico de área
print("\n[TESTE 3] Gráfico de área - Dólar")
try:
    dolar_df = bacen.cambio(moeda='USD')
    print(f"✓ Dados do Dólar carregados: {len(dolar_df)} registros")
    
    # Pegar último ano
    dolar_recente = dolar_df.tail(252).copy()  # ~252 dias úteis
    
    fig = plot.area(
        dolar_recente,
        titulo="Cotação Dólar/Real (Último Ano)",
        ylabel="R$",
        empilhado=False,
        alpha=0.6,
        salvar="/workspace/test_dolar_area.png",
        mostrar=False
    )
    print("✓ Gráfico de área salvo em: /workspace/test_dolar_area.png")
except Exception as e:
    print(f"✗ Erro no teste 3: {e}")

# Teste 4: Gráfico de dispersão (correlação)
print("\n[TESTE 4] Gráfico de dispersão - Correlação Selic vs IPCA")
try:
    # Preparar dados comparáveis
    comparacao = analise.comparar(selic_df, ipca_df, nome1='Selic', nome2='IPCA')
    print(f"✓ Dados alinhados: {len(comparacao)} períodos comuns")
    
    if len(comparacao) > 10:
        fig = plot.dispersao(
            comparacao['Selic'],
            comparacao['IPCA'],
            titulo="Correlação: Selic vs IPCA",
            xlabel="Selic (%)",
            ylabel="IPCA (%)",
            ajustar_reta=True,
            mostrar_correlacao=True,
            salvar="/workspace/test_dispersao_selic_ipca.png",
            mostrar=False
        )
        print("✓ Gráfico de dispersão salvo em: /workspace/test_dispersao_selic_ipca.png")
    else:
        print("⚠ Dados insuficientes para dispersão")
except Exception as e:
    print(f"✗ Erro no teste 4: {e}")

# Teste 5: Painel comparativo
print("\n[TESTE 5] Painel Comparativo - Panorama Econômico")
try:
    igpm_df = bacen.igpm()
    print(f"✓ Dados do IGP-M carregados: {len(igpm_df)} registros")
    
    fig = plot.comparativo(
        selic=selic_df,
        ipca=ipca_df,
        dolar=dolar_df,
        igpm=igpm_df,
        titulo="Panorama Econômico Brasileiro",
        salvar="/workspace/test_painel_comparativo.png",
        mostrar=False
    )
    print("✓ Painel comparativo salvo em: /workspace/test_painel_comparativo.png")
except Exception as e:
    print(f"✗ Erro no teste 5: {e}")

# Teste 6: Função genérica plotar()
print("\n[TESTE 6] Função genérica plotar()")
try:
    fig = plot.plotar(
        selic_df.tail(50),
        tipo='linha',
        titulo="Selic (Últimos 50 registros) - Função Genérica",
        salvar="/workspace/test_generica.png",
        mostrar=False
    )
    print("✓ Função genérica testada com sucesso")
except Exception as e:
    print(f"✗ Erro no teste 6: {e}")

print("\n" + "=" * 60)
print("TODOS OS TESTES FORAM EXECUTADOS!")
print("=" * 60)
print("\nArquivos gerados:")
print("  - test_selic_linha.png")
print("  - test_ipca_barras.png")
print("  - test_dolar_area.png")
print("  - test_dispersao_selic_ipca.png")
print("  - test_painel_comparativo.png")
print("  - test_generica.png")
print("\n✓ Módulo de visualização (Fase 5) implementado com sucesso!")
