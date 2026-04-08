# biblioteca-br

Biblioteca Python open source para acesso unificado a dados econômicos e financeiros brasileiros.

Uma solução completa que integra em um único pacote dados do BACEN, B3 e IBGE, com módulos nativos de análise, visualização gráfica, exportação (Excel, CSV, PDF), calendário econômico e conversor monetário.

## Destaques

- **Dados Oficiais**: Selic, IPCA, IGP-M, câmbio, PTAX, expectativas Focus, juros bancários, Pix e séries do BACEN
- **Mercado Financeiro**: Ibovespa e ações da B3 (PETR4, VALE3, etc.)
- **Análise Integrada**: Resumo estatístico, correlação, tendência, comparação e panorama econômico
- **Visualização Pronta**: Gráficos de linha, barras, área e dispersão com uma linha de código
- **Exportação Fácil**: Exporte para Excel, CSV ou gere relatórios em PDF automaticamente
- **Calendário Econômico**: Datas de divulgações de indicadores (IPCA, Selic, PIB)
- **Conversor Monetário**: Deflacione valores e atualize pela inflação para comparações reais

## Instalação

```bash
pip install biblioteca-br
```

## Exemplo Rápido

```python
from biblioteca_br import bacen, analise, plot, exportar

selic = bacen.selic()
resumo = analise.resumo(selic)
plot.linha(selic, titulo="Evolução da Taxa Selic")
exportar.excel(selic, "selic_historico.xlsx")
```

## Diferenciais vs python-bcb

- Interface unificada BACEN + B3 + IBGE
- Módulo de análise completo
- Calendário Econômico integrado
- Conversor Monetário/Deflacionador
- Gráficos embutidos
- Exportação Excel/CSV/PDF
- Dados do Pix e B3

## Licença

MIT License
