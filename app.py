import streamlit as st
from openai import OpenAI
from datetime import datetime

st.set_page_config(page_title="CFO da Alma e dos Negócios™", page_icon="🌟", layout="centered")

st.title("🌟 CFO DA ALMA E DOS NEGÓCIOS™")
st.markdown("**Versão Deus dos Deuses** — Relatório Premium Profissional")

st.markdown("### Cole sua API Key do Groq")

api_key = st.text_input(
    "API Key:",
    type="password",
    placeholder="gsk_...",
    key="api_key_input"
)

if st.button("🚀 Gerar Relatório Premium Completo", type="primary"):
    if not api_key or len(api_key) < 30:
        st.error("Por favor, cole sua chave Groq completa.")
        st.stop()

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    # === PROMPT FORTE E DETALHADO ===
    SYSTEM_PROMPT = """Você é o CFO DA ALMA E DOS NEGÓCIOS™ — consultor executivo de alto nível, fusão entre Estratégia, Dados e Consciência.

Sempre gere relatórios PREMIUM longos (mínimo 25 páginas simuladas), com linguagem profissional de consultoria internacional (McKinsey, Bain, Deloitte).

Estrutura obrigatória do relatório:
- Capa Impactante
- Resumo Executivo
- Score Executivo com barras visuais (■■■ etc.)
- Análise detalhada de todas as redes sociais (baseado nos prints e dados fornecidos)
- Diagnóstico de marca e posicionamento
- Veredito Absoluto (direto e forte)
- Análise Numerológica (data 25/10/1977)
- Oportunidades ocultas e gargalos
- Plano de Ação 30/90 dias + Roadmap 12 meses (passo a passo prático)
- Recomendações finais e frase de impacto

Use tom executivo, inteligente, transformador e convincente. Seja profundo, específico e surpreendente. Nunca faça relatório curto ou genérico."""

    with st.spinner("Gerando relatório premium completo... Isso pode levar alguns segundos."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": "Gere o relatório completo premium para Luciano Francisco com base em todos os prints e dados das redes sociais que ele forneceu anteriormente."}
                ],
                max_tokens=12000,
                temperature=0.75
            )

            report = response.choices[0].message.content

            st.success("✅ Relatório Premium Gerado!")
            st.markdown(report)

            st.download_button(
                label="📥 Baixar Relatório Completo (Markdown)",
                data=report,
                file_name=f"Relatorio_Premium_Luciano_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"Erro: {str(e)}")

st.caption("Prompt otimizado para gerar relatórios longos e profissionais.")
