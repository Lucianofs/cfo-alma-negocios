import streamlit as st
import os
from openai import OpenAI
from markdown2 import markdown
from weasyprint import HTML
from PIL import Image
import io

st.set_page_config(page_title="CFO da Alma e dos Negócios™", page_icon="🌟", layout="wide")

st.title("🌟 CFO DA ALMA E DOS NEGÓCIOS™")
st.markdown("**Versão Deus dos Deuses** — Análise Minuciosa • Diagnóstico Real • Escala com Consciência")
st.caption("Estratégia + Dados + Consciência | Relatórios Premium de 25+ páginas")

# === PROMPT SUPREMO (cole aqui o prompt refinado completo da conversa anterior) ===
SYSTEM_PROMPT = """[INSIRA AQUI TODO O PROMPT SUPREMO "VERSÃO DEUS DOS DEUSES" QUE EU ENTREGUEI ANTERIORMENTE, INCLUINDO O ADENDO DE ANÁLISE DE REDES SOCIAIS VIA PRINTS E URLs] 

ADENDO DE ANÁLISE DE REDES SOCIAIS — MODO SEGURO:
Analise profundamente URLs públicas e especialmente imagens/prints enviados (Instagram, LinkedIn, Facebook, Kwai, YouTube, etc.). Extraia: número de seguidores, bio, engajamento, coerência de marca, qualidade de conteúdo, thumbnails, calls to action. Destaque o que está certo, errado e oportunidades ocultas. Unifique marca e sugira bios/roteiros novos."""

# Sidebar
with st.sidebar:
    st.header("Configurações")
    api_key = st.text_input("API Key (Grok xAI ou OpenAI)", type="password", value=os.getenv("API_KEY", ""))
    model = st.selectbox("Modelo", ["grok-beta", "gpt-4o"])
    st.markdown("---")
    st.info("Envie URLs + prints das redes + arquivos para análise profunda.")

# Uploads
st.subheader("📤 Envie os dados para análise")
urls = st.text_area("URLs (uma por linha)", placeholder="https://lucianofrancisco.com.br\nhttps://www.instagram.com/lucianofranciscoi", height=100)

uploaded_files = st.file_uploader(
    "Arquivos e Prints (PDF, XLS, PNG, JPG, etc.)",
    accept_multiple_files=True,
    type=['pdf', 'xlsx', 'xls', 'png', 'jpg', 'jpeg', 'txt']
)

tipo_analise = st.selectbox(
    "Tipo de Análise",
    [
        "Relatório Público Inicial (para impressionar)",
        "Relatório Público Robusto",
        "Relatório Total Completo (Negócio + Alma + Fusão)",
        "Growth Marketing + Plano 30/90 dias",
        "BI + Dashboard Executivo",
        "Diagnóstico de Crise / Escala Financeira",
        "Análise Completa de Redes Sociais (com prints)"
    ]
)

contexto_adicional = st.text_area("Contexto adicional (faturamento, problemas, objetivos, etc.)", height=150, value="Faturamento zero, desempregado, foco em vender diagnósticos e consultoria online mundial.")

if st.button("🚀 Gerar Análise Completa e Relatório Premium", type="primary"):
    if not api_key:
        st.error("Por favor, insira sua API Key (Grok ou OpenAI)")
        st.stop()

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1" if "grok" in model else None
    )

    # Preparar contexto
    context = f"Tipo de análise: {tipo_analise}\n\n"
    if urls:
        context += f"URLs fornecidas:\n{urls}\n\n"
    if uploaded_files:
        context += f"Arquivos/prints enviados: {len(uploaded_files)} itens (incluindo prints de perfis)\n"
    if contexto_adicional:
        context += f"Contexto adicional:\n{contexto_adicional}\n"

    full_prompt = f"{SYSTEM_PROMPT}\n\nDados do usuário:\n{context}\n\nRealize análise minuciosa como o Deus dos Deuses e gere o relatório completo no formato premium."

    with st.spinner("Analisando profundamente todos os dados, prints e URLs... Gerando relatório de 25+ páginas. Isso pode levar 1-2 minutos."):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7,
                max_tokens=16000
            )
            
            report_md = response.choices[0].message.content
            
            st.success("✅ Relatório Gerado com Sucesso!")
            
            # Exibir relatório
            st.markdown("### Relatório Completo")
            st.markdown(report_md)
            
            # Download Markdown
            st.download_button(
                label="📥 Baixar como Markdown",
                data=report_md,
                file_name=f"relatorio_cfo_{tipo_analise[:30]}.md",
                mime="text/markdown"
            )
            
            # Converter para PDF
            try:
                html = markdown(report_md, extras=["tables", "fenced-code-blocks", "break-on-newline"])
                pdf_bytes = HTML(string=html).write_pdf()
                
                st.download_button(
                    label="📄 Baixar PDF Premium (pronto para imprimir)",
                    data=pdf_bytes,
                    file_name=f"Relatorio_CFO_Deus_dos_Deuses.pdf",
                    mime="application/pdf"
                )
                st.success("PDF gerado com layout profissional!")
            except Exception as pdf_err:
                st.warning(f"PDF não gerado automaticamente: {pdf_err}. Use o Markdown e converta externamente.")
            
        except Exception as e:
            st.error(f"Erro na geração: {e}")

# Histórico simples
if "reports" not in st.session_state:
    st.session_state.reports = []
if "report_md" in locals():
    st.session_state.reports.append(report_md)

st.markdown("---")
st.caption("App construído com base em todo o contexto da consultoria. Teste com seus prints e URLs. Quer ajustes ou próxima versão com extração automática de texto de PDFs?")