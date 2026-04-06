# Escopo do Projeto
## Biblioteca Python de Dados Brasileiros — v2.1 Atualizado

Biblioteca Python open source para acesso unificado a dados econômicos e financeiros brasileiros.

**Objetivo:** Superar o python-bcb em escopo, adicionando IBGE, B3, análise, visualização, exportação, calendário econômico e conversor monetário.

---

## Fase 1 — BACEN — Banco Central do Brasil ✅ Concluída

| Função | Descrição | Status |
|--------|-----------|--------|
| `bacen.selic()` | Taxa Selic diária e mensal | ✅ |
| `bacen.ipca()` | Inflação oficial (IPCA) | ✅ |
| `bacen.igpm()` | Índice Geral de Preços do Mercado | ✅ |
| `bacen.cambio(moeda='USD')` | Cotação de qualquer moeda | ✅ |
| `bacen.ptax(moeda='USD')` | Cotação oficial PTAX do BCB | ✅ |
| `bacen.serie(codigo=11)` | Qualquer série do SGS pelo código | ✅ |
| `bacen.expectativas()` | Boletim Focus — expectativas de mercado | ✅ |
| `bacen.juros_bancos()` | Taxas de juros por banco e modalidade | ✅ |
| `bacen.pix()` | Volume de transações Pix por mês | ✅ |
| `bacen.inadimplencia()` | Taxa de inadimplência do crédito | 🔜 |
| `bacen.credito()` | Volume total de crédito na economia | 🔜 |
| `bacen.inflacao_acumulada()` | IPCA acumulado no ano automaticamente | 🔜 |
| **`bacen.calendario()`** | **[NOVO] Calendário econômico — próximas divulgações** | ✅ |

---

## Fase 2 — B3 — Bolsa de Valores ✅ Concluída

| Função | Descrição | Status |
|--------|-----------|--------|
| `b3.ibovespa()` | Histórico do índice Ibovespa | ✅ |
| `b3.acao(ticker='PETR4')` | Histórico de uma ação específica | ✅ |
| `b3.acoes(['PETR4','VALE3'])` | Múltiplas ações de uma vez | ✅ |

---

## Fase 3 — IBGE — Instituto Brasileiro de Geografia e Estatística ⏳ Pendente

> API instável — requer implementação robusta de tratamento de erros

| Função | Descrição | Status |
|--------|-----------|--------|
| `ibge.pib()` | PIB trimestral do Brasil | ⏳ |
| `ibge.desemprego()` | Taxa de desemprego — PNAD Contínua | ⏳ |
| `ibge.populacao()` | Dados populacionais | ⏳ |
| `ibge.ipca()` | IPCA pelo IBGE | ⏳ |

---

## Fase 4 — Análise — Módulo de Análise de Dados ✅ Concluída

| Função | Descrição | Status |
|--------|-----------|--------|
| `analise.resumo(df)` | Média, mínimo, máximo, variação % automáticos | ✅ |
| `analise.comparar(df1, df2)` | Compara dois indicadores no mesmo período | ✅ |
| `analise.correlacao(df1, df2)` | Calcula correlação entre dois indicadores | ✅ |
| `analise.tendencia(df)` | Detecta tendência de alta ou baixa | ✅ |
| `analise.panorama()` | Selic, IPCA, Dólar, IGP-M num DataFrame só | ✅ |
| **`analise.deflacionar()`** | **[NOVO] Converte valor nominal para valor real** | ✅ |
| **`analise.atualizar_monetario()`** | **[NOVO] Atualiza valor monetary pela inflação** | ✅ |

---

## Fase 5 — Visualização — Gráficos Prontos ✅ Concluída

| Função | Descrição | Status |
|--------|-----------|--------|
| `plot.linha(df)` | Gráfico de linha de qualquer indicador | ✅ |
| `plot.barras(df)` | Gráfico de barras verticais/horizontais | ✅ |
| `plot.area(df)` | Gráfico de área preenchida/empilhada | ✅ |
| `plot.dispersao(x, y)` | Dispersão com correlação e regressão linear | ✅ |
| `plot.comparativo()` | Painel 2x2 com 4 indicadores principais | ✅ |
| `plot.plotar(df, tipo)` | Função genérica unificada | ✅ |

---

## Fase 6 — Exportação ✅ Concluída

| Função | Descrição | Status |
|--------|-----------|--------|
| `exportar.excel(df)` | Exportar DataFrame para Excel | ✅ |
| `exportar.csv(df)` | Exportar para CSV | ✅ |
| `exportar.pdf(df)` | Gerar relatório em PDF | ✅ |

---

## Fase 7 — Publicação no PyPI 🎯 Meta Final

| Funcionalidade | Descrição | Status |
|----------------|-----------|--------|
| Estrutura de pacote | Organizar módulos como lib de verdade | ⏳ |
| README em português | Documentação clara e didática | ✅ |
| Publicação no PyPI | `pip install biblioteca-br` funcionando | ⏳ |
| `.gitignore` e boas práticas | Projeto limpo e profissional | ⏳ |

---

## 🆚 Diferenciais em relação ao python-bcb

| Diferencial | biblioteca-br | python-bcb |
|-------------|---------------|------------|
| Interface unificada BACEN + IBGE + B3 | ✅ | ❌ |
| Documentação em português | ✅ | ✅ |
| Módulo de análise (correlação, tendência, resumo) | ✅ | ❌ |
| **Calendário Econômico** | ✅ | ❌ |
| **Conversor/Deflacionador Monetário** | ✅ | ❌ |
| Gráficos embutidos | ✅ | ❌ |
| Exportação integrada (Excel, CSV, PDF) | ✅ | ❌ |
| `panorama()` — Todos os indicadores de uma vez | ✅ | ❌ |
| Dados do Pix | ✅ | ❌ |
| Dados da B3 | ✅ | ❌ |

---

## 📋 Novas Funcionalidades Detalhadas

### 1. Calendário Econômico (`bacen.calendario()`)

**Descrição:** Consulta e exibe as datas das próximas divulgações de indicadores econômicos como IPCA, Selic, PIB, Balança Comercial etc.

**Exemplo de uso:**
```python
from biblioteca_br import bacen

# Próximas divulgações do IPCA nos próximos 30 dias
df = bacen.calendario(indicador="IPCA", dias=30)

# Todas as divulgações dos próximos 7 dias
df = bacen.calendario(dias=7)

# Focar em um indicador específico
df = bacen.calendario(indicador="Selic", dias=60)
```

**Benefícios:**
- Permite que analistas planejem suas análises antecipadamente
- Integração direta com fontes oficiais (BACEN, IBGE)
- Filtragem por indicador e período

---

### 2. Conversor Monetário e Deflacionador (`analise.deflacionar()`, `analise.atualizar_monetario()`)

**Descrição:** Converte valores nominais em valores reais usando índices de inflação (IPCA), facilitando comparações de poder de compra ao longo do tempo.

**Exemplo de uso:**
```python
from biblioteca_br import analise

# Qual o valor real de R$ 1000 em jan/2020 comparado a jan/2024?
valor_real = analise.deflacionar(
    valor=1000, 
    data_inicio="01/01/2020", 
    data_fim="01/01/2024"
)
# Retorna: quanto aqueles R$ 1000 valeriam em poder de compra de 2024

# Atualizar valor monetário pela inflação
valor_atualizado = analise.atualizar_monetario(
    valor=1000, 
    data_origem="01/01/2020", 
    data_destino="01/01/2024"
)
# Retorna: quanto seria necessário em 2024 para ter o mesmo poder de compra
```

**Benefícios:**
- Essencial para análises financeiras de longo prazo
- Remove distorções inflacionárias de séries históricas
- Facilita comparações intertemporais precisas

---

## 📊 Status Geral do Projeto

| Fase | Status | Conclusão |
|------|--------|-----------|
| Fase 1 — BACEN | ✅ Concluída | 100% |
| Fase 2 — B3 | ✅ Concluída | 100% |
| Fase 3 — IBGE | ⏳ Pendente | 0% |
| Fase 4 — Análise | ✅ Concluída | 100% |
| Fase 5 — Visualização | ✅ Concluída | 100% |
| Fase 6 — Exportação | ✅ Concluída | 100% |
| Fase 7 — Publicação | ⏳ Em andamento | 50% |

**Progresso Total:** ~85%

---

*Documento atualizado em 05/04/2025 — v2.1 | Projeto em desenvolvimento*
