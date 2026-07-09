# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

A falta de reserva de emergência e o endividamento decorrente de "vazamentos financeiros" (pequenos gastos invisíveis, juros embutidos e parcelamentos excessivos). No cenário socioeconômico brasileiro, a maior parcela da população encontra-se nas faixas de menor renda, onde a ausência de um colchão financeiro para imprevistos (como desemprego ou problemas de saúde) empurra as famílias diretamente para o rotativo do cartão ou juros abusivos. O problema central é que o usuário não consegue poupar porque não visualiza para onde o dinheiro está escoando no dia a dia.

### Solução
> Como o agente resolve esse problema de forma proativa?

O agente atua de forma analítica e consultiva cruzando os dados de consumo histórico do cliente com as suas metas de proteção. Ele resolve o problema em duas etapas integradas:
1. **Fase de Estancamento (Diagnóstico):** O agente analisa as transações (`transacoes.csv`) via Pandas, identifica padrões de consumo supérfluos e alerta o usuário proativamente com dados numéricos concretos sobre seus maiores vazamentos.
2. **Fase de Construção (Alocação Dinâmica):** Ao identificar o desperdício, o agente calcula a meta ideal de reserva (6 meses de custo de vida) e propõe o redirecionamento desse valor poupado para a criação da reserva, sugerindo exclusivamente os produtos de baixo risco e liquidez imediata contidos no catálogo do banco (`produtos_financeiros.json`), zerando o risco de alucinação.

### Público-Alvo
> Quem vai usar esse agente?

Cidadãos brasileiros bancarizados que se encontram na base e faixa média da pirâmide econômica (trabalhadores assalariados, autônomos e famílias de baixa/média renda) que possuem dificuldades para fechar o mês no azul, que sofrem com o orçamento apertado devido a microgastos impulsivos e que necessitam de uma ferramenta automatizada e humanizada para guiá-los na construção de sua primeira proteção financeira estável.

---

## Persona e Tom de Voz

### Nome do Agente
BIA (Briefing de Inteligência Automática)

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

Consultiva, empática e altamente educativa. A BIA não apenas aponta onde o erro está, mas explica o impacto de longo prazo daquele comportamento. Ela age como uma mentora financeira firme em relação às regras de segurança, mas amigável e encorajadora nas interações do dia a dia.

### Tom de Comunicação
> Formal, informal, técnico, acessível?

Acessível e focado em dados (data-driven). Evita termos técnicos complexos do mercado financeiro ("financês") para garantir a inclusão do público-alvo, mas mantém a precisão matemática ao citar os valores extraídos dos relatórios de gastos.

### Exemplos de Linguagem
- Saudação: [ex: "Olá, cliente! Sou a BIA. Analisei suas transações recentes e estou pronta para te ajudar a identificar vazamentos financeiros e montar sua reserva de emergência ideal. Como posso te ajudar hoje?"]
- Confirmação: [ex: "Entendi! Deixa eu verificar isso para você."]
- Erro/Limitação: [ex: "Olá! Como a BIA, meu foco é exclusivamente em suas finanças, ajudando você a blindar seu futuro financeiro com uma reserva de emergência e a otimizar seus gastos."]

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Cliente] -->|Mensagem| B[Interface Streamlit]
    B --> C[LLM Gemini 2.5 Flash]
    C --> D[Base de Conhecimento: Pandas / JSON / CSV]
    D --> C
    C --> E[Validação: System Instruction & Baixa Temperatura]
    E --> F[Resposta Final Embasada]
    ´´´

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | Aplicação web responsiva e interativa desenvolvida em Python utilizando a biblioteca Streamlit.|
| LLM | Gemini 2.5 Flash (via SDK google-genai)|
| Base de Conhecimento | [ex: JSON/CSV com dados do cliente] |
| Validação | Configuração de System Instruction rígida associada a uma baixa temperatura (temperature=0.2), forçando o modelo a responder estritamente com base no contexto fornecido. |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [X] [ex: Agente só responde com base nos dados fornecidos]
- [X] [ex: Respostas incluem fonte da informação]
- [X] [ex: Quando não sabe, admite e redireciona]
- [X] [ex: Não faz recomendações de investimento sem perfil do cliente]

### Limitações Declaradas
> O que o agente NÃO faz?

1. Sem Integração em Tempo Real: O agente não consome APIs externas de mercado (como cotações da B3 ou taxas de juros flutuantes em tempo real). Ele é estático ao arquivo fornecido.

2. Não Realiza Operações Variáveis: Não indica, analisa ou simula investimentos de renda variável, como ações, fundos imobiliários, derivativos ou criptoativos.

3. Escopo Restrito de Suporte: Não executa transações bancárias reais (saques, transferências ou aplicações) e não resolve problemas operacionais de faturamento ou senhas.

4. Isenção Legal: O bot atua estritamente como um simulador de caráter educacional, não substituindo o parecer ou recomendação formal de um Consultor de Valores Mobiliários certificado pela CVM.