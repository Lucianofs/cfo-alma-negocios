import streamlit as st
from openai import OpenAI
from datetime import datetime

# Configuração Premium da Página
st.set_page_config(
    page_title="CFO da Alma e dos Negócios™ | McKinsey-Grade Analytics", 
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Personalizado — Visual McKinsey + Luxury Gold
st.markdown("""
<style>
    .main { background-color: #0a0e14; color: #e0e0e0; }
    .stMarkdown h1 { color: #d4af37; font-weight: 800; font-size: 2.5rem; text-align: center; }
    .stMarkdown h2, .stMarkdown h3 { color: #d4af37; font-weight: 700; }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > select, .stNumberInput > div > div > input {
        background-color: #1a1d24; color: #ffffff; border: 1px solid #d4af37; border-radius: 6px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #d4af37 0%, #f2d06b 50%, #d4af37 100%);
        color: #0a0e14; font-weight: 800; border: none; border-radius: 8px;
        padding: 1rem 2.5rem; font-size: 1.2rem; width: 100%;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    }
    .stButton > button:hover { 
        background: linear-gradient(90deg, #f2d06b 0%, #d4af37 50%, #f2d06b 100%); 
        color: #000000;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
    }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .stRadio > label { color: #d4af37; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.title("👑 CFO DA ALMA E DOS NEGÓCIOS™")
st.markdown("### *Metodologia McKinsey-Grade + Diagnóstico Holístico Integrado*")
st.markdown("### *Por Luciano Francisco | 19 Anos de Excelência Estratégica*")
st.markdown("---")

# Colunas para organização
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    st.markdown("### 🔑 Configuração")
    api_key = st.text_input("Chave de API Groq:", type="password", placeholder="gsk_...")
    
    st.markdown("### 👤 Perfil do Cliente")
    tipo_analise = st.radio(
        "Escopo:",
        ["Pessoa Física", "Pessoa Jurídica", "Híbrido (Dono + Empresa)"],
        index=2
    )
    
    nome_cliente = st.text_input("Nome do Cliente / Empresa:", placeholder="Ex: Tech Solutions Ltda")
    
    nicho_mercado = st.text_input("Nicho / Segmento:", placeholder="Ex: E-commerce de Moda, SaaS B2B")
    
    if tipo_analise in ["Pessoa Física", "Híbrido (Dono + Empresa)"]:
        data_nascimento = st.date_input("Data de Nascimento (Numerologia):", value=datetime(1980, 1, 1))
    else:
        data_nascimento = None

with col2:
    st.markdown("### 📊 Métricas de Negócio")
    
    faturamento_atual = st.text_input("Faturamento Mensal Atual (R$):", placeholder="Ex: 50.000")
    faturamento_meta = st.text_input("Meta de Faturamento (R$):", placeholder="Ex: 150.000")
    
    tamanho_equipe = st.number_input("Tamanho da Equipe:", min_value=1, max_value=10000, value=10)
    
    tempo_mercado = st.selectbox(
        "Tempo de Mercado:",
        ["0-1 ano", "1-3 anos", "3-5 anos", "5-10 anos", "10+ anos"]
    )
    
    principal_desafio = st.text_area(
        "Principal Desafio Atual:",
        height=100,
        placeholder="Ex: Baixa conversão, equipe desmotivada, sem estratégia digital..."
    )

with col3:
    st.markdown("### 📊 Dados Brutos Coletados (Varredura Completa)")
    st.markdown("*(Cole URLs, Reclame Aqui, redes sociais, KPIs, CRM, textos, fotos, documentos)*")
    dados_brutos = st.text_area(
        "Dados Coletados:",
        height=400,
        placeholder="Ex:\n- Site: www.exemplo.com (tráfego 3k/mês, SEO fraco)\n- Reclame Aqui: 12 reclamações sobre entrega\n- Instagram: 5k seguidores, engajamento 1.2%\n- CRM: 40% de churn no primeiro mês\n- Data de nascimento do dono: 15/05/1985\n- Objetivo: Escalar para 500k/mês em 12 meses"
    )

st.markdown("---")

if st.button("👑 GERAR RELATÓRIO ESTRATÉGICO PREMIUM", type="primary"):
    if not api_key or len(api_key) < 30:
        st.error("⚠️ Por favor, insira uma Chave de API Groq válida.")
        st.stop()
    
    if not nome_cliente or not dados_brutos:
        st.error("⚠️ Nome do cliente e dados brutos são obrigatórios.")
        st.stop()

    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

    # SYSTEM PROMPT — McKinsey + CFO da Alma Fusion
    SYSTEM_PROMPT = f"""Você é Luciano Francisco, criador do método "CFO da Alma e dos Negócios™".
Você combina a sofisticação analítica de McKinsey/Bain & Company com 19 anos de expertise em consultoria holística, numerologia e estratégia de negócios.

SUA MISSÃO: Gerar um RELATÓRIO ANALÍTICO-ESTRATÉGICO PREMIUM que funde:
1. Rigor executivo de nível global (ROI, eficiência, crescimento)
2. Profundidade holística (alma, energia, bloqueios internos)
3. Plano de ação cirúrgico (Dia 1, Dia 7, Dia 30, Dia 90)

REGRAS ABSOLUTAS DE ESCRITA:
- Tom: Executivo, sofisticado, direto, focado em resultados
- Proibido: Frases clichês, introduções longas, jargões técnicos excessivos
- Concisão: Frases curtas e ativas
- Formatação: Markdown impecável (negritos, tabelas, listas) — altamente escaneável
- Data Storytelling: Não liste números; explique O PORQUÊ e o impacto financeiro

ESTRUTURA OBRIGATÓRIA DO RELATÓRIO:

1. SUMÁRIO EXECUTIVO (Para o CEO)
   - 2 parágrafos ultra-focados: maior ganho do período + principal desafio superado
   - 3 bullet points com métricas mais impactantes

2. ANÁLISE DE CONTEXTO (Nacional e Internacional)
   - Relacione os dados com tendências globais de mercado de 2026
   - Posicione o cliente: acima ou abaixo da média de mercado?
   - Use dados de benchmarking do setor

3. DIAGNÓSTICO DA ALMA (Se houver data de nascimento)
   - Análise numerológica: Caminho de Vida, Ano Pessoal 2026
   - Bloqueios energéticos e impacto na tomada de decisão
   - Como o estado interno reflete nos resultados externos

4. DIAGNÓSTICO DOS NEGÓCIOS
   - Análise fria dos dados, URLs, KPIs
   - Gargalos operacionais, falhas de marketing, oportunidades de CRM
   - Data Storytelling: Causa → Efeito → Impacto Financeiro

5. A SÍNTESE (O Pulo do Gato)
   - Como a "Alma" do dono impacta diretamente os "Negócios"
   - Conexão entre bloqueios internos e gargalos externos

6. PLANO DE AÇÃO TÁTICO (Visão de Futuro)
   - 3 recomendações estratégicas prioritárias, ordenadas por:
     * Impacto (Alto/Médio/Baixo)
     * Esforço de implementação (Alto/Médio/Baixo)
   - Cronograma cirúrgico:
     * Dia 1: Ação imediata de estancamento
     * Dia 2-7: Organização e preparação
     * Dia 30: Primeira vitória rápida (Quick Win) + métrica esperada
     * Dia 90: Consolidação e escala

7. ESTIMATIVA DE INVESTIMENTO & ROI
   - Sugestão macro de alocação de recursos
   - Retorno esperado em 30, 60, 90 dias

8. MENSAGEM DE FECHAMENTO
   - Convite elegante e profissional para contratar sua consultoria
   - Tom: Exclusivo, transformador, orientado a resultados

DADOS DO CLIENTE:
- Nome: {nome_cliente}
- Nicho: {nicho_mercado if nicho_mercado else 'Não informado'}
- Tipo de Análise: {tipo_analise}
- Faturamento Atual: R$ {faturamento_atual if faturamento_atual else 'Não informado'}
- Meta de Faturamento: R$ {faturamento_meta if faturamento_meta else 'Não informada'}
- Tamanho da Equipe: {tamanho_equipe} pessoas
- Tempo de Mercado: {tempo_mercado}
- Principal Desafio: {principal_desafio if principal_desafio else 'Não informado'}
- Data de Nascimento: {data_nascimento.strftime('%d/%m/%Y') if data_nascimento else 'Não fornecida'}
"""

    with st.spinner("🧠 Processando matriz de dados com metodologia McKinsey-Grade + Diagnóstico Holístico..."):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",  # ✅ MODELO CONFIRMADO FUNCIONAL
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"DADOS BRUTOS COLETADOS PARA ANÁLISE:\n\n{dados_brutos}"}
                ],
                max_tokens=6000,
                temperature=0.3
            )

            relatorio_gerado = response.choices[0].message.content

            st.success("✅ Relatório Estratégico Premium Gerado com Sucesso!")
            st.markdown("---")
            st.markdown(relatorio_gerado)
            st.markdown("---")

            nome_arquivo = f"Relatorio_Estrategico_CFO_{nome_cliente.replace(' ', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d')}.md"
            st.download_button(
                label="📥 Baixar Relatório Premium (Markdown)",
                data=relatorio_gerado,
                file_name=nome_arquivo,
                mime="text/markdown"
            )
            
            st.info("💡 **Dica de Uso Executivo:** Copie o texto, cole no Word/Notion, aplique sua identidade visual e envie ao cliente como 'Diagnóstico Estratégico Preliminar' — uma arma poderosa para fechar consultorias de alto ticket.")

        except Exception as e:
            st.error(f"❌ Erro na comunicação com a IA: {str(e)}")
            st.warning("💡 Verifique sua chave API e saldo na conta Groq.")

st.markdown("---")
st.caption("Desenvolvido por Luciano Francisco | CFO da Alma e dos Negócios™ | Metodologia McKinsey-Grade + Diagnóstico Holístico Integrado | 19 Anos de Excelência Estratégica")
