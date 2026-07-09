import streamlit as st
import pandas as pd
import json
import os
from google import genai
from google.genai import types

# ==============================================================================
# 1. CONFIGURAÇÃO DA API DO GEMINI
# ==============================================================================
# Certifique-se de configurar a variável de ambiente GEMINI_API_KEY no seu sistema
# ou substitua diretamente pela sua chave para testes locais.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "sua_chave")
client = genai.Client(api_key=GEMINI_API_KEY)

# ==============================================================================
# 2. CARREGAMENTO E PROCESSAMENTO DOS DADOS (CONTEXTO)
# ==============================================================================
@st.cache_data
def carregar_e_processar_dados():
    """Carrega os datasets do desafio e extrai métricas para o prompt do sistema."""
    path_perfil = "../data/perfil_investidor.json"
    path_produtos = "../data/produtos_financeiros.json"
    path_transacoes = "../data/transacoes.csv"
    
    # Fallbacks padrão
    perfil = {"nome_cliente": "Cliente DIO", "perfil": "Moderado"}
    produtos = {"produtos": [{"nome": "CDB Liquidez Diária", "risco": "Baixo", "rentabilidade": "100% CDI"}]}
    resumo_gastos = "Não foi possível carregar o histórico de transações."
    
    if os.path.exists(path_perfil):
        with open(path_perfil, "r", encoding="utf-8") as f:
            perfil = json.load(f)
            
    if os.path.exists(path_produtos):
        with open(path_produtos, "r", encoding="utf-8") as f:
            produtos = json.load(f)
            
    if os.path.exists(path_transacoes):
        try:
            # Lendo o CSV
            df = pd.read_csv(path_transacoes, encoding="utf-8")
            
            # CORREÇÃO 1: Converter a coluna 'data' para o formato datetime do Pandas
            df['data'] = pd.to_datetime(df['data'], errors='coerce')
            
            # CORREÇÃO 2: Filtrar apenas as despesas (tipo == 'saida') para a análise de vazamentos
            df_saidas = df[df['tipo'] == 'saida'].copy()
            
            if 'categoria' in df_saidas.columns and 'valor' in df_saidas.columns:
                gastos_por_categoria = df_saidas.groupby('categoria')['valor'].sum().to_dict()
                gasto_total = df_saidas['valor'].sum()
                
                # Calcular quantos meses únicos existem no arquivo para tirar a média real
                qtd_meses = max(1, len(df['data'].dt.to_period('M').unique()))
                custo_medio_mensal = gasto_total / qtd_meses
                
                resumo_gastos = {
                    "gasto_total_saidas_analisado": gasto_total,
                    "custo_medio_mensal_estimado": custo_medio_mensal,
                    "reserva_emergencia_ideal_6_meses": custo_medio_mensal * 6,
                    "maiores_vazamentos_por_categoria": gastos_por_categoria
                }
        except Exception as e:
            resumo_gastos = f"Erro ao processar as transações: {str(e)}"

    return perfil, produtos, resumo_gastos
perfil_cliente, produtos_banco, analise_financeira = carregar_e_processar_dados()

# ==============================================================================
# 3. INTERFACE VISUAL (STREAMLIT)
# ==============================================================================
st.set_page_config(page_title="BIA - Inteligência Financeira", page_icon="📈", layout="centered")

st.title("🤖 BIA: Assistente de Reserva & Gastos")
st.markdown("---")

# Inicialização do histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Olá, {perfil_cliente.get('nome_cliente', 'cliente')}! Sou a BIA. Analisei suas transações recentes e estou pronta para te ajudar a identificar vazamentos financeiros e montar sua reserva de emergência ideal. Como posso te ajudar hoje?"}
    ]

# Renderizar mensagens anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================================================================
# 4. ENGENHARIA DE PROMPT & INTEGRAÇÃO COM GEMINI
# ==============================================================================
if prompt_usuario := st.chat_input("Ex: Onde estou gastando demais? / Qual minha reserva ideal?"):
    
    # Exibir prompt do usuário
    st.chat_message("user").markdown(prompt_usuario)
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    
    # PROMPT DE SISTEMA: Define comportamento, dados reais e travas contra alucinação
    system_instruction = f"""
    Você é a BIA (Briefing de Inteligência Automática), uma assistente virtual financeira cirúrgica, proativa e educadora.
    Seu escopo é focado EXCLUSIVAMENTE em:
    1. Apontar vazamentos financeiros (gastos supérfluos, categorias muito altas).
    2. Calcular e guiar a montagem de uma Reserva de Emergência (foco em cobrir 6 meses de custo de vida).
    3. Indicar onde alocar esse dinheiro da reserva de emergência usando UNICAMENTE produtos de Renda Fixa com liquidez diária do catálogo fornecido.

    [CONHECIMENTO DO CLIENTE (DADOS REAIS)]
    - Perfil oficial do Suitability: {perfil_cliente.get('perfil')}
    - Análise métrica de gastos extraída do CSV: {json.dumps(analise_financeira, ensure_ascii=False, indent=2)}

    [CATÁLOGO DE PRODUTOS PERMITIDOS]
    {json.dumps(produtos_banco, ensure_ascii=False, indent=2)}

    REGRAS RÍGIDAS DE COMPLIANCE E COMPORTAMENTO:
    - Se o usuário perguntar sobre ações, criptomoedas, fundos imobiliários ou qualquer produto fora do catálogo fornecido, diga educadamente que seu escopo é restrito a ajudá-lo a blindar suas finanças com a reserva de emergência e que o banco não oferece esses ativos para este propósito.
    - Se o usuário questionar se você é um consultor oficial, adicione um pequeno disclaimer de que você é um simulador educacional automatizado.
    - Use dados numéricos objetivos do contexto de gastos para dar broncas amigáveis ou insights (ex: 'Você gastou X com Delivery, se cortasse metade, atingiria sua reserva Y meses mais rápido').
    - Nunca invente taxas ou produtos financeiros (risco de alucinação zero).
    """

    # Chamar o modelo da Google
    with st.chat_message("assistant"):
        placeholder_resposta = st.empty()
        
        try:
            config = types.GenerateContentConfig(
            system_instruction=system_instruction,
                temperature=0.2,  # Baixíssima temperatura para evitar desvios e alucinações
            )
            
            # Usando o modelo ideal para chat de texto rápido
            resposta_gemini = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_usuario,
                config=config
            )
            
            texto_final = resposta_gemini.text
            placeholder_resposta.markdown(texto_final)
            st.session_state.messages.append({"role": "assistant", "content": texto_final})
            
        except Exception as e:
            st.error(f"Ocorreu um erro na comunicação com a IA: {e}")