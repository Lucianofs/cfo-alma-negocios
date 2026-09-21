import streamlit as st
from openai import OpenAI
from datetime import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import base64
from matplotlib.patches import Circle, Rectangle
import numpy as np

# Configuração Premium da Página
st.set_page_config(
    page_title="CFO da Alma e dos Negócios™ | Executive Intelligence", 
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

st.title(" CFO DA ALMA E DOS NEGÓCIOS™")
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

# Função para criar gráfico de Scorecard
def create_scorecard_chart(metrics_dict):
    """Cria um gráfico de barras horizontal para o scorecard"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    names = list(metrics_dict.keys())
    current = list(metrics_dict.values())
    
    colors = ['#d4af37' if v >= 70 else '#c9a227' if v >= 50 else '#b8941f' for v in current]
    
    y_pos = np.arange(len(names))
    
    bars = ax.barh(y_pos, current, color=colors, height=0.6, edgecolor='black', linewidth=0.5)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=9, fontweight='bold')
    ax.set_xlim(0, 100)
    ax.set_xlabel('Score', fontsize=10, fontweight='bold')
    ax.set_title('Business Scorecard - 5 Dimensões Avaliadas', fontsize=12, fontweight='bold', pad=20)
    
    # Adicionar valores nas barras
    for i, (bar, val) in enumerate(zip(bars, current)):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, 
                f'{val}/100', va='center', fontsize=9, fontweight='bold')
    
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Salvar como bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf.getvalue()

# Função para criar gráfico de Radar
def create_radar_chart(dimensions_scores):
    """Cria um gráfico de radar para visualização multidimensional"""
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    categories = list(dimensions_scores.keys())
    values = list(dimensions_scores.values())
    
    # Número de variáveis
    num_vars = len(categories)
    
    # Calcular ângulos
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Completar o círculo
    values += values[:1]
    
    # Plotar
    ax.plot(angles, values, 'o-', linewidth=2, color='#d4af37', markersize=8, markerfacecolor='#f2d06b')
    ax.fill(angles, values, alpha=0.25, color='#d4af37')
    
    # Configurar
    ax.set_ylim(0, 100)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=9, weight='bold')
    ax.set_title('Matriz de Competências CFO™', size=12, weight='bold', pad=30)
    
    plt.tight_layout()
    
    # Salvar como bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf.getvalue()

# Função para criar gráfico de progresso
def create_progress_chart(current, target, label):
    """Cria um gráfico de gauge/progresso"""
    fig, ax = plt.subplots(figsize=(4, 4))
    
    # Criar gauge
    percentage = (current / target) * 100 if target > 0 else 0
    
    # Criar círculo
    circle = Circle((0.5, 0.5), 0.4, fill=False, linewidth=8, color='#1a1d24')
    ax.add_patch(circle)
    
    # Arco de progresso
    if percentage > 0:
        arc = Rectangle((0.1, 0.1), 0.8, 0.8, angle=0, 
                       fill=True, color='#d4af37', 
                       extent=percentage * 3.6)  # 360 graus * percentage
        ax.add_patch(arc)
    
    # Texto central
    ax.text(0.5, 0.6, f'{current}', ha='center', va='center', 
            fontsize=18, fontweight='bold', color='#d4af37')
    ax.text(0.5, 0.4, f'de {target}', ha='center', va='center', 
            fontsize=10, color='#888')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title(label, fontsize=10, weight='bold', pad=10)
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf.getvalue()

# Função para gerar PDF
def sanitize_text(text):
    if not text:
        return ""
    replacements = {
        '™': '(TM)',
        '©': '(C)',
        '®': '(R)',
        '—': '-',
        '–': '-',
        '•': '-',
        '→': '->',
        '★': '*',
        '■': '[X]',
        '□': '[ ]',
        '✓': 'OK',
        '✗': 'X',
        '👑': '[CFO]',
        '📊': '[DATA]',
        '📥': '[DL]',
        '💡': '[DICA]',
        '⚠️': '[AVISO]',
        '❌': '[ERRO]',
        '✅': '[OK]',
        '🧠': '[IA]',
        '📄': '[DOC]',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    # Remove emojis e caracteres não-ASCII restantes
    text = text.encode('ascii', 'replace').decode('ascii')
    text = text.replace('?', '')  # Remove pontos de interrogação de fallback
    return text

def generate_pdf_report(data, relatorio_texto):
    """Gera um PDF profissional estilo McKinsey com suporte a caracteres especiais"""
    
    # Sanitiza todo o texto antes de usar no PDF
    relatorio_limpo = sanitize_text(relatorio_texto)
    nome_cliente_limpo = sanitize_text(data["nome_cliente"])
    nicho_limpo = sanitize_text(data["nicho"])
    
    pdf = FPDF()
    pdf.add_page()
    
    # ============ CAPA ============
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(212, 175, 55)  # Dourado
    pdf.cell(0, 25, 'CFO DA ALMA E DOS NEGOCIOS', ln=True, align='C')
    
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, '(TM)', ln=True, align='C')
    
    pdf.ln(5)
    pdf.set_font('Helvetica', 'I', 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, 'Relatorio Estrategico Premium', ln=True, align='C')
    pdf.cell(0, 8, 'Metodologia McKinsey-Grade + Diagnostico Holistico', ln=True, align='C')
    
    pdf.ln(15)
    
    # Linha decorativa dourada
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(1)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    
    pdf.ln(15)
    
    # ============ DADOS DO CLIENTE ============
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(0, 8, 'INFORMACOES DO CLIENTE', ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    
    info_items = [
        ('Cliente:', nome_cliente_limpo),
        ('Data:', datetime.now().strftime('%d/%m/%Y')),
        ('Tipo de Analise:', data["tipo_analise"]),
        ('Nicho:', nicho_limpo),
        ('Faturamento Atual:', f"R$ {data.get('faturamento_atual', 'N/I')}"),
        ('Meta:', f"R$ {data.get('faturamento_meta', 'N/I')}"),
        ('Data de Nascimento:', data.get('data_nascimento', 'N/I')),
    ]
    
    for label, value in info_items:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(50, 7, label)
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 7, str(value), ln=True)
    
    pdf.ln(10)
    pdf.set_draw_color(212, 175, 55)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(10)
    
    # ============ SEÇÕES DO RELATÓRIO ============
    secoes = [
        ('01. SUMARIO EXECUTIVO', relatorio_limpo[:2500]),
        ('02. ANALISE DE CONTEXTO', relatorio_limpo[2500:5000]),
        ('03. DIAGNOSTICO DA ALMA', relatorio_limpo[5000:7500]),
        ('04. DIAGNOSTICO DOS NEGOCIOS', relatorio_limpo[7500:10000]),
        ('05. SINTESIS ESTRATEGICA', relatorio_limpo[10000:12500]),
        ('06. PLANO DE ACAO TATICO', relatorio_limpo[12500:15000]),
        ('07. INVESTIMENTO E ROI', relatorio_limpo[15000:17500]),
        ('08. MENSAGEM DE FECHAMENTO', relatorio_limpo[17500:]),
    ]
    
    for titulo, conteudo in secoes:
        if not conteudo.strip():
            continue
            
        pdf.add_page()
        
        # Título da seção
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(212, 175, 55)
        pdf.cell(0, 12, titulo, ln=True)
        
        # Linha decorativa
        pdf.set_draw_color(212, 175, 55)
        pdf.set_line_width(0.5)
        pdf.line(30, pdf.get_y(), 180, pdf.get_y())
        pdf.ln(5)
        
        # Conteúdo
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 6, conteudo)
    
    # ============ RODAPÉ FINAL ============
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(0, 12, 'SOBRE O METODO CFO (TM)', ln=True)
    
    pdf.set_draw_color(212, 175, 55)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(30, 30, 30)
    
    sobre_texto = (
        "Este relatorio foi elaborado com base na metodologia CFO da Alma e dos Negocios (TM), "
        "criada por Luciano Francisco, combinando analise estrategica de nivel McKinsey/Bain com "
        "diagnostico holistico profundo (numerologia, energia, bloqueios internos).\n\n"
        "19 anos de experiencia em educacao, marketing, dados, politica publica e transformacao.\n\n"
        "Mais de 12.000 profissionais treinados | 20+ empresas atendidas | 300+ palestras\n\n"
        "Contato: lucianofrancisco.com.br\n"
        "WhatsApp: Disponivel mediante agendamento"
    )
    pdf.multi_cell(0, 6, sobre_texto)
    
    # Rodapé com numeração
    pdf.ln(10)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, f'Gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")} | CFO da Alma e dos Negocios (TM) | Confidencial', ln=True, align='C')
    
    # Salvar como bytes
    pdf_bytes = pdf.output()
    
    return pdf_bytes

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
                model="openai/gpt-oss-20b",
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
            
            # Exibir relatório na tela
            st.markdown("### 📄 Visualização do Relatório")
            st.markdown(relatorio_gerado)
            st.markdown("---")
            
            # Criar dados para o PDF
            dados_pdf = {
                "nome_cliente": nome_cliente,
                "tipo_analise": tipo_analise,
                "nicho": nicho_mercado or "Não informado",
                "data_nascimento": data_nascimento.strftime('%d/%m/%Y') if data_nascimento else "Não fornecida",
                "faturamento_atual": faturamento_atual or "Não informado",
                "faturamento_meta": faturamento_meta or "Não informada"
            }
            
            # Gerar PDF
            pdf_bytes = generate_pdf_report(dados_pdf, relatorio_gerado)
            
            # Botões de download
            col_download1, col_download2 = st.columns(2)
            
            with col_download1:
                st.download_button(
                    label="📥 Baixar Relatório em PDF (Executivo)",
                    data=pdf_bytes,
                    file_name=f"Relatorio_CFO_{nome_cliente.replace(' ', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            
            with col_download2:
                nome_arquivo_md = f"Relatorio_CFO_{nome_cliente.replace(' ', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d')}.md"
                st.download_button(
                    label="📄 Baixar Relatório em Markdown",
                    data=relatorio_gerado,
                    file_name=nome_arquivo_md,
                    mime="text/markdown"
                )
            
            st.info("💡 **Dica de Uso Executivo:** O PDF está formatado no padrão McKinsey para apresentação a C-levels. Use o Markdown para edições rápidas no Notion/Word.")

        except Exception as e:
            st.error(f"❌ Erro na comunicação com a IA: {str(e)}")
            st.warning("💡 Verifique sua chave API e saldo na conta Groq.")

st.markdown("---")
st.caption("Desenvolvido por Luciano Francisco | CFO da Alma e dos Negócios™ | Metodologia McKinsey-Grade + Diagnóstico Holístico Integrado | 19 Anos de Excelência Estratégica")
