import streamlit as st
from openai import OpenAI
import plotly.express as px
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import io
import base64

st.set_page_config(page_title="CFO da Alma e dos Negócios™", page_icon="🌟", layout="wide")

st.title("🌟 CFO DA ALMA E DOS NEGÓCIOS™")
st.markdown("**Versão Deus dos Deuses** — Relatório Premium com Gráficos Power BI Style")

api_key = st.sidebar.text_input("API Key (Grok ou OpenAI)", type="password")
model = st.sidebar.selectbox("Modelo", ["grok-beta", "gpt-4o"])

if st.button("🚀 Gerar Relatório PDF Premium Completo", type="primary"):
    if not api_key:
        st.error("Insira sua API Key")
        st.stop()

    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1" if "grok" in model else None)

    with st.spinner("Gerando análise profunda + PDF Premium..."):
        # 1. Gerar conteúdo do relatório via IA
        prompt = "Gere um relatório executivo premium completo para Luciano Francisco, com análise de redes sociais a partir de prints, scores visuais, veredito forte, plano de ação 30/90 dias, numerologia básica e linguagem de consultoria internacional."
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "Você é o CFO da Alma e dos Negócios™. Sempre entregue relatórios de alto nível."},
                      {"role": "user", "content": prompt}],
            max_tokens=10000
        )
        report_text = response.choices[0].message.content

        # 2. Criar gráficos estilo Power BI
        scores = pd.DataFrame({
            'Área': ['Visibilidade', 'Marca', 'Engajamento', 'Autoridade', 'Potencial de Escala'],
            'Score': [28, 35, 22, 68, 82]
        })

        fig = px.bar(scores, x='Área', y='Score', text='Score', title="Score Executivo - Análise Atual")
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(yaxis_range=[0, 100], height=400)

        # Mostrar no app
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(report_text)

        # 3. Gerar PDF Premium com fpdf2
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 15)
                self.cell(0, 10, 'CFO DA ALMA E DOS NEGÓCIOS™ - Relatório Premium', ln=1, align='C')
                self.ln(10)

            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Página {self.page_no()}', align='C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, f"Relatório Executivo - Luciano Francisco\nData: {datetime.now().strftime('%d/%m/%Y')}\n\n")
        pdf.multi_cell(0, 10, report_text)

        # Adicionar gráfico (salvar como imagem temporária)
        img_bytes = fig.to_image(format="png")
        pdf.add_page()
        pdf.cell(0, 10, "Gráfico Score Executivo", ln=1)
        pdf.image(io.BytesIO(img_bytes), x=10, y=30, w=180)

        # Salvar PDF em memória
        pdf_output = pdf.output(dest="S").encode("latin-1")

        st.success("✅ PDF Premium gerado com sucesso!")
        
        st.download_button(
            label="📄 Baixar Relatório PDF Premium (pronto para entregar ao cliente)",
            data=pdf_output,
            file_name=f"Relatorio_Premium_Luciano_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )

st.caption("App configurado para gerar PDF Premium diretamente.")
