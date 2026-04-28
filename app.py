import streamlit as st
from openai import OpenAI
from datetime import datetime

st.set_page_config(page_title="CFO da Alma e dos Negócios™", page_icon="🌟", layout="centered")

st.title("🌟 CFO DA ALMA E DOS NEGÓCIOS™")
st.markdown("**Versão Deus dos Deuses**")

st.markdown("### Cole sua API Key do Groq")

api_key = st.text_input(
    "API Key:",
    type="password",
    placeholder="gsk_...",
    key="api_key_input"
)

if st.button("🚀 Gerar Relatório Premium", type="primary"):
    if not api_key or len(api_key) < 30:
        st.error("Por favor, cole sua chave Groq completa.")
        st.stop()

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    SYSTEM_PROMPT = """Você é o CFO DA ALMA E DOS NEGÓCIOS™. 
Gere relatórios executivos PREMIUM longos, profissionais e transformadores, no estilo McKinsey/Bain.
Sempre inclua: Capa, Resumo Executivo, Scores visuais, Análise detalhada das redes, Veredito forte, 
Análise numerológica (data 25/10/1977), Plano de ação 30/90 dias e Recomendações práticas."""

    with st.spinner("Gerando relatório premium..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",   # Modelo mais leve e rápido, dentro do limite
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": "Gere um relatório completo e detalhado para Luciano Francisco baseado em sua presença digital, prints de redes sociais, site e contexto fornecido anteriormente. Seja profundo e profissional."}
                ],
                max_tokens=6000,
                temperature=0.7
            )

            report = response.choices[0].message.content

            st.success("✅ Relatório gerado!")
            st.markdown(report)

            st.download_button(
                label="📥 Baixar Relatório (Markdown)",
                data=report,
                file_name=f"Relatorio_Premium_Luciano_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"Erro: {str(e)}")

st.caption("Versão otimizada para limite de tokens do Groq.")
