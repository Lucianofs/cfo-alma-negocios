import streamlit as st
from openai import OpenAI
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="CFO da Alma e dos Negócios™", page_icon="🌟", layout="wide")

st.title("🌟 CFO DA ALMA E DOS NEGÓCIOS™")
st.markdown("**Versão Deus dos Deuses** — Relatório Premium")

# === CAMPO DE API KEY CORRIGIDO ===
st.sidebar.header("Configuração")
api_key = st.sidebar.text_input(
    "🔑 Cole sua API Key aqui",
    type="password",
    placeholder="gsk_xxxxxxxxxxxxxxxxxxxxxxxx",
    help="Use sua chave do Groq, Grok ou OpenAI"
)

model = st.sidebar.selectbox(
    "Escolha o Modelo",
    ["groq-llama3.1-70b", "groq-llama3.1-8b", "gpt-4o-mini"]
)

if st.button("🚀 Gerar Relatório Premium Completo", type="primary"):
    if not api_key:
        st.error("⚠️ Por favor, cole sua API Key no campo ao lado.")
        st.stop()

    # Configuração para Groq
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    with st.spinner("Analisando seus dados e gerando relatório premium..."):
        prompt = """
        Você é o CFO da Alma e dos Negócios™. 
        Gere um relatório executivo premium completo para Luciano Francisco.
        Inclua análise de redes sociais, scores visuais, veredito forte, plano de ação e linguagem profissional.
        """

        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",   # Modelo bom e rápido no Groq
            messages=[
                {"role": "system", "content": "Você é um consultor executivo de alto nível."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=8000,
            temperature=0.7
        )

        report_text = response.choices[0].message.content

        # Gráfico exemplo
        scores = pd.DataFrame({
            'Categoria': ['Visibilidade', 'Marca', 'Engajamento', 'Autoridade', 'Potencial'],
            'Score': [28, 35, 22, 68, 82]
        })

        fig = px.bar(scores, x='Categoria', y='Score', text='Score', title="Score Executivo")
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(yaxis_range=[0, 100])

        st.success("✅ Relatório gerado com sucesso!")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(report_text)

        st.download_button(
            label="📥 Baixar Relatório (Markdown)",
            data=report_text,
            file_name=f"Relatorio_CFO_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )

st.info("💡 Cole sua chave Groq no campo acima e clique no botão vermelho.")
