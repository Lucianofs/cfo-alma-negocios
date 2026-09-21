import streamlit as st
from openai import OpenAI
from datetime import datetime

# Configuração Premium da Página
st.set_page_config(
    page_title="CFO da Alma e dos Negócios™", 
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Personalizado para Visual "Deus dos Deuses" (Dark & Gold)
st.markdown("""
<style>
    .main { background-color: #0f1115; color: #e0e0e0; }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #d4af37; font-weight: 700; }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > select {
        background-color: #1a1d24; color: #ffffff; border: 1px solid #d4af37;
    }
    .stButton > button {
        background: linear-gradient(90deg, #d4af37 0%, #f2d06b 100%);
        color: #0f1115; font-weight: bold; border: none; border-radius: 8px;
        padding: 0.75rem 2rem; font-size: 1.1rem; width: 100%;
    }
    .stButton > button:hover { background: linear-gradient(90deg, #f2d06b 0%, #d4af37 100%); color: #000000; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

st.title("👑 CFO DA ALMA E DOS NEGÓCIOS™")
st.markdown("### *Sistema de Diagnóstico e Arquitetura de Crescimento por Luciano Francisco*")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🔑 Configuração")
    api_key = st.text_input("Chave de API Groq:", type="password", placeholder="gsk_...")
    
    # SELETOR DE MODELO BLINDADO
    st.markdown("### ⚙️ Motor de IA")
    modelo_escolhido = st.selectbox(
        "Selecione o modelo (Se um falhar, troque aqui):",
        options=[
            "mixtral-8x7b-32768",       # ✅ Mais estável, ótimo para textos longos (Reclame Aqui, URLs)
            "llama-3.1-70b-versatile",  # ✅ Excelente raciocínio estratégico
            "gemma2-9b-it"              # ✅ Leve e rápido (fallback de emergência)
        ],
        index=0
    )
    st.caption("Recomendado: Mixtral 8x7b para análises de grandes volumes de texto.")
    
    st.markdown("### 👤 Perfil do Cliente")
    tipo_analise = st.radio(
        "Escopo da Análise:",
        ["Pessoa Física (Apenas Alma)", "Pessoa Jurídica (Apenas Negócios)", "Híbrido (Dono + Empresa)"],
        index=2
    )
    
    nome_cliente = st.text_input("Nome do Cliente / Empresa:", placeholder="Ex: João Silva / Tech Solutions Ltda")
    
    if tipo_analise in ["Pessoa Física (Apenas Alma)", "Híbrido (Dono + Empresa)"]:
        data_nascimento = st.date_input("Data de Nascimento (Essencial p/ Numerologia):", value=datetime(1980, 1, 1))
    else:
        data_nascimento = None
        
    if tipo_analise in ["Pessoa Jurídica (Apenas Negócios)", "Híbrido (Dono + Empresa)"]:
        nicho_mercado = st.text_input("Nicho de Mercado / Segmento:", placeholder="Ex: Tecnologia, Saúde, Varejo")
    else:
        nicho_mercado = None

with col2:
    st.markdown("### 📊 Dados Brutos Coletados (Varredura)")
    st.markdown("*(Cole aqui URLs, resumos do Reclame Aqui, textos de redes sociais, KPIs, anotações de CRM)*")
    dados_brutos = st.text_area(
        "Insira os dados coletados:",
        height=350,
        placeholder="Ex:\n- Site: www.exemplo.com (tráfego baixo)\n- Reclame Aqui: 3 reclamações sobre demora\n- Instagram: 5k seguidores, engajamento 1%\n- Data de nascimento do dono: 15/05/1985\n- Objetivo: Faturar 100k/mês em 6 meses."
    )

st.markdown("---")

if st.button("👑 GERAR DIAGNÓSTICO PREMIUM CFO™", type="primary"):
    if not api_key or len(api_key) < 30:
        st.error("⚠️ Por favor, insira uma Chave de API Groq válida.")
        st.stop()
    
    if not nome_cliente or not dados_brutos:
        st.error("⚠️ O nome do cliente e os dados brutos coletados são obrigatórios.")
        st.stop()

    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

    # O CÉREBRO DO LUCIANO: System Prompt Ultra-Detalhado
    SYSTEM_PROMPT = f"""Você é Luciano Francisco, criador do método "CFO da Alma e dos Negócios™". 
Você tem 19 anos de experiência como Arquiteto de Sistemas de Crescimento, Terapeuta Holístico e Consultor de Dados.
Sua missão é analisar os dados brutos fornecidos e gerar um RELATÓRIO EXECUTIVO PREMIUM, cirúrgico e transformador.

REGRAS ABSOLUTAS:
1. NÃO invente dados. Use APENAS as informações fornecidas. Se algo for inferência, chame de "Hipótese Estratégica".
2. Tom de voz: Autoritário, Empático, Estratégico, Holístico e Orientado a Resultados.
3. Formatação: Markdown impecável, profissional, pronto para ser enviado a um cliente de alto ticket.

ESTRUTURA OBRIGATÓRIA DO RELATÓRIO:
1. CAPA EXECUTIVA: Nome do Cliente, Data, Título Impactante ("Diagnóstico Estratégico CFO™").
2. RESUMO EXECUTIVO: 1 parágrafo poderoso sobre a situação atual e o potencial oculto.
3. DIAGNÓSTICO DA ALMA (Se houver data de nascimento): Análise numerológica (Caminho de Vida, Ano Pessoal), bloqueios energéticos e impacto na tomada de decisão.
4. DIAGNÓSTICO DOS NEGÓCIOS: Análise fria dos dados, URLs e KPIs. Gargalos, falhas de marketing, oportunidades de CRM.
5. A SÍNTESE (O Pulo do Gato): Como o estado da "Alma" do dono reflete nos resultados dos "Negócios" (e vice-versa).
6. PLANO DE AÇÃO TÁTICO (Obrigatório): 
   - Dia 1: Ação imediata de estancamento.
   - Dia 2 a Dia 7: Organização e preparação.
   - Dia 30: Primeira vitória rápida (Quick Win) e métrica.
   - Dia 90: Consolidação e escala.
7. ESTIMATIVA DE INVESTIMENTO & ROI: Sugestão macro de alocação de recursos.
8. MENSAGEM DE FECHAMENTO: Convite elegante para contratar a sua consultoria para implementar este plano.

Dados do Cliente: {nome_cliente}
Tipo de Análise: {tipo_analise}
Data de Nascimento: {data_nascimento.strftime('%d/%m/%Y') if data_nascimento else 'Não fornecida'}
Nicho: {nicho_mercado if nicho_mercado else 'Não fornecido'}
"""

    with st.spinner("🧠 O CFO da Alma e dos Negócios está processando a matriz de dados e gerando a estratégia..."):
        try:
            response = client.chat.completions.create(
                model=modelo_escolhido, # Usa o modelo selecionado no dropdown
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"DADOS BRUTOS COLETADOS PARA ANÁLISE:\n\n{dados_brutos}"}
                ],
                max_tokens=4000, # Ajustado para evitar estouro no plano gratuito da Groq
                temperature=0.3  # Baixa para garantir precisão estratégica e profissionalismo
            )

            relatorio_gerado = response.choices[0].message.content

            st.success("✅ Diagnóstico Premium Gerado com Sucesso!")
            st.markdown("---")
            st.markdown(relatorio_gerado)
            st.markdown("---")

            nome_arquivo = f"Diagnostico_CFO_{nome_cliente.replace(' ', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d')}.md"
            st.download_button(
                label="📥 Baixar Relatório Premium (Markdown)",
                data=relatorio_gerado,
                file_name=nome_arquivo,
                mime="text/markdown"
            )
            
            st.info("💡 **Dica de Uso:** Copie o texto, cole no Word/Notion, aplique sua identidade visual e envie ao cliente como 'Análise Prévia de Valor' para fechar a consultoria.")

        except Exception as e:
            st.error(f"❌ Erro na comunicação com a IA: {str(e)}")
            st.warning("💡 **Solução Rápida:** Volte ao topo da página, no campo 'Motor de IA', selecione um modelo diferente (ex: gemma2-9b-it) e tente gerar novamente.")

st.markdown("---")
st.caption("Desenvolvido por Luciano Francisco | CFO da Alma e dos Negócios™ | Tecnologia de Ponta a Serviço da Transformação.")
