# 🤖 BIA: Briefing de Inteligência Automática - Assistente de Reserva & Gastos

> Desafio de Projeto desenvolvido para o Laboratório "Construa seu Assistente Virtual com Inteligência Artificial" da plataforma DIO.

O objetivo deste projeto é evoluir um chatbot financeiro tradicional para um **Agente Inteligente, Proativo e Consultivo**. Focado na realidade socioeconômica brasileira, o sistema atua na raiz do endividamento: identificando "vazamentos financeiros" ocultos e guiando o usuário de forma totalmente segura na construção de sua primeira **Reserva de Emergência**.

---

## 📌 Funcionalidades Principais

* **Diagnóstico de Vazamentos (Estancamento):** Varre e processa o histórico de transações (`transacoes.csv`) via Pandas para categorizar despesas e alertar o usuário sobre gastos invisíveis e gargalos orçamentários.
* **Projeção de Reserva de Emergência:** Calcula automaticamente o custo de vida médio mensal do usuário e estipula a meta ideal para cobrir 6 meses de imprevistos.
* **Filtro de Alocação Segura:** Recomenda onde guardar o capital poupado utilizando única e estritamente os ativos de Renda Fixa com liquidez imediata listados no catálogo institucional (`produtos_financeiros.json`).
* **Arquitetura Anti-Alucinação (Zero-Risk):** Uso de instruções de sistema (*System Instructions*) severas e parametrização de baixa temperatura (`0.2`) no modelo Gemini para mitigar riscos de recomendações falsas ou fora de conformidade.

---

## ⚙️ Interface da Aplicação

### Tela Principal do Chatbot
Assim que iniciado, o sistema carrega os dados mockados em segundo plano e a assistente BIA inicia a abordagem de forma contextualizada e acolhedora:

![alt text](images/apresentação_Bia.png)

### Teste de Inteligência e Restrição de Contexto
Ao ser questionada sobre investimentos voláteis (Renda Variável/Criptoativos) ou temas fora do escopo, a BIA barra a solicitação educadamente e mantém o foco no colchão de liquidez:


![alt text](images/resposta_1.jpeg)



![alt text](images/resposta_2.jpeg)

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Linguagem:** Python 3.10+
* **Framework Web:** Streamlit (Criação da interface de chat interativa)
* **Manipulação de Dados:** Pandas (Pipeline de ingestão, parsing de data e agregação de despesas)
* **Modelo de Linguagem (LLM):** Gemini 2.5 Flash (via SDK oficial atualizado `google-genai`)

---

## 📐 Arquitetura do Sistema

O fluxo de processamento de mensagens e ancoragem de contexto (Grounding) segue a estrutura técnica mapeada abaixo:

```mermaid
flowchart TD
    A[Cliente / Usuário] -->|Mensagem de Texto| B[Interface Visual Streamlit]
    B --> C[Orquestrador Python]
    D[(Base de Dados: CSV / JSON)] -->|Pipeline Pandas Cacheado| C
    C -->|Prompt + Contexto Métrico Consolidado| E[LLM Gemini 2.5 Flash]
    E -->|Validação por Baixa Temperatura| F[Resposta Segura e Embasada]
    F --> B
