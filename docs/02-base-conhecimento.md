# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `perfil_investidor.json` | JSON | Personalizar recomendações |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Os dados originais foram mantidos em sua estrutura nativa, porém o pipeline em Python realiza uma **transformação em tempo de execução**. A coluna `data` do arquivo `transacoes.csv` é convertida para o tipo `datetime` para cálculo preciso do histórico. Além disso, o agente aplica um filtro dinâmico separando as entradas (receitas como o salário) das saídas (despesas), garantindo que a análise de vazamentos financeiros considere unicamente o fluxo de escoamento de capital (gastos do usuário).

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os dados são carregados logo na inicialização da aplicação através de um pipeline em Python otimizado com o decorador `@st.cache_data` do Streamlit. Isso garante que a leitura dos arquivos JSON e CSV ocorra apenas uma vez (ou quando os arquivos forem modificados), poupando memória e acelerando o tempo de resposta do chatbot a cada nova mensagem enviada pelo usuário.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados não são jogados de forma bruta para a LLM. O script em Python processa o CSV utilizando a biblioteca Pandas, calcula o custo médio mensal e consolida um dicionário estruturado com as maiores despesas categorizadas e o valor exato necessário para cobrir 6 meses de custo de vida. Essas métricas consolidadas, junto com os catálogos em JSON, são injetadas dinamicamente dentro da tag `system_instruction` do Gemini 2.5 Flash a cada requisição, servindo como uma "âncora de realidade" indelével para o modelo.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Abaixo está a estrutura exata de como o Python consolida e injeta as variáveis de contexto dentro das instruções de sistema (`system_instruction`) enviadas à API:

```text
[CONHECIMENTO DO CLIENTE (DADOS REAIS)]
- Perfil oficial do Suitability: Moderado
- Análise métrica de gastos extraída do CSV: 
{
  "gasto_total_saidas_analisado": 2472.90,
  "custo_medio_mensal_estimado": 2472.90,
  "reserva_emergencia_ideal_6_meses": 14837.40,
  "maiores_vazamentos_por_categoria": {
    "moradia": 1380.00,
    "alimentacao": 570.00,
    "transporte": 295.00,
    "saude": 188.00,
    "lazer": 55.90
  }
}

[CATÁLOGO DE PRODUTOS PERMITIDOS]
{
  "produtos": [
    {
      "nome": "CDB Rendimento Ágil",
      "risco": "Baixo",
      "rentabilidade": "110% CDI",
      "liquidez": "Imediata"
    }
  ]
}