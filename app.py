import streamlit as st
from openai import OpenAI
from datetime import datetime

st.set_page_config(page_title="CFO da Alma e dos Negócios™", page_icon="🌟", layout="centered")

st.title("🌟 CFO DA ALMA E DOS NEGÓCIOS™")
st.markdown("**Versão Deus dos Deuses**")

st.markdown("### Insira sua API Key do Groq")

api_key = st.text_input(
    "Cole sua chave Groq aqui:",
    type="password",
    placeholder="gsk_pyKM9FmSCroeDO5Uv8cgWGdyb3FYQwt8CvXrSzl9...",
    key="api_key_input"
)

if st.button("🚀 Gerar Relatório Premium", type="primary"):
    if not api_key or len(api_key) < 20:
        st.error("Por favor, cole sua chave Groq completa no campo acima.")
        st.stop()

    st.success("Chave detectada! Conectando ao Groq...")

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

        with st.spinner("Gerando análise profunda e relatório premium..."):
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": "Você é o CFO da Alma e dos Negócios™. Gere relatórios executivos de alto nível."},
                    {"role": "user", "content": "Gere um relatório completo de análise para Luciano Francisco, incluindo diagnóstico de redes sociais, scores, veredito e plano de ação."}
                ],
                max_tokens=6000,
                temperature=0.7
            )

            report = response.choices[0].message.content

        st.success("✅ Relatório gerado com sucesso!")
        st.markdown(report)

        st.download_button(
            label="📥 Baixar Relatório (Markdown)",
            data=report,
            file_name=f"Relatorio_CFO_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown"
        )

    except Exception as e:
        st.error(f"Erro: {str(e)}")

st.caption("App simplificado para resolver problema de digitação no campo de API Key.")
