import streamlit as st
from openai import OpenAI
from datetime import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import re
import json
import numpy as np

# ============================================================
# Configuração Premium da Página
# ============================================================
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

# ============================================================
# Formulário
# ============================================================
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

# ============================================================
# Paleta Dark Mode Premium
# ============================================================
BG = "#0B0F19"
DOURADO = "#D4AF37"
DOURADO_CLARO = "#F2D06B"
AZUL = "#00E5FF"
AZUL_CLARO = "#4FD1FF"
TEXTO_CLARO = "#E0E0E0"


def _estilo_dark(fig, ax):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.tick_params(colors=TEXTO_CLARO)
    for spine in ax.spines.values():
        spine.set_color("#333333")
    ax.xaxis.label.set_color(TEXTO_CLARO)
    ax.yaxis.label.set_color(TEXTO_CLARO)


def parse_valor_brl(texto):
    """Converte string em formato brasileiro (ex: '50.000' ou 'R$ 50.000,00') em float."""
    if not texto:
        return 0.0
    limpo = re.sub(r"[^\d,.]", "", str(texto))
    if not limpo:
        return 0.0
    if "," in limpo and "." in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    elif "," in limpo:
        limpo = limpo.replace(",", ".")
    elif "." in limpo:
        # Sem vírgula: um ponto seguido de exatamente 3 dígitos é separador
        # de milhar no padrão brasileiro (ex: "50.000" = 50 mil), não decimal.
        partes = limpo.split(".")
        if len(partes) > 1 and len(partes[-1]) == 3:
            limpo = limpo.replace(".", "")
    try:
        return float(limpo)
    except ValueError:
        return 0.0


# ============================================================
# Gráficos (agora em Dark Mode Premium e efetivamente usados no PDF)
# ============================================================

def create_scorecard_chart(metrics_dict):
    """Gráfico de barras horizontal — Business Scorecard"""
    fig, ax = plt.subplots(figsize=(9, 5))
    names = list(metrics_dict.keys())
    current = list(metrics_dict.values())

    colors = [DOURADO if v >= 70 else AZUL if v >= 50 else "#7a5c1f" for v in current]
    y_pos = np.arange(len(names))

    bars = ax.barh(y_pos, current, color=colors, height=0.55, edgecolor="black", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=10, fontweight="bold", color=TEXTO_CLARO)
    ax.set_xlim(0, 100)
    ax.set_title("Business Scorecard — Dimensões Avaliadas", fontsize=13, fontweight="bold",
                 color=DOURADO, pad=18)

    for bar, val in zip(bars, current):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
                 f"{val:.0f}/100", va="center", fontsize=9, fontweight="bold", color=TEXTO_CLARO)

    ax.grid(axis="x", alpha=0.15, linestyle="--", color="#888888")
    _estilo_dark(fig, ax)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close()
    return buf.getvalue()


def create_radar_chart(dimensions_scores):
    """Radar — Matriz de Competências / Alinhamento"""
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(projection="polar"))
    categories = list(dimensions_scores.keys())
    values = list(dimensions_scores.values())

    num_vars = len(categories)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    values = values + values[:1]

    ax.plot(angles, values, "o-", linewidth=2, color=DOURADO, markersize=8, markerfacecolor=DOURADO_CLARO)
    ax.fill(angles, values, alpha=0.25, color=DOURADO)

    ax.set_ylim(0, 100)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=9, weight="bold", color=TEXTO_CLARO)
    ax.set_title("Matriz de Competências CFO™", size=13, weight="bold", color=DOURADO, pad=28)
    ax.spines["polar"].set_color("#333333")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.grid(color="#333333", alpha=0.5)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close()
    return buf.getvalue()


def create_progress_chart(current, target, label):
    """Gauge — % da meta atingida"""
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(projection="polar"))
    percentage = min((current / target) * 100, 100) if target > 0 else 0

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 2 * np.pi)

    # trilha de fundo
    theta_bg = np.linspace(0, 2 * np.pi, 200)
    ax.bar(theta_bg, [1] * len(theta_bg), width=(2 * np.pi / 200), bottom=0.4,
           color="#1a1d24", edgecolor=None)

    # arco de progresso
    theta_max = 2 * np.pi * (percentage / 100)
    if theta_max > 0:
        theta_fg = np.linspace(0, theta_max, 200)
        ax.bar(theta_fg, [1] * len(theta_fg), width=(theta_max / 200) if theta_max else 0.01,
               bottom=0.4, color=DOURADO, edgecolor=None)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["polar"].set_visible(False)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    ax.text(0, 0, f"{percentage:.0f}%", ha="center", va="center",
             fontsize=26, fontweight="bold", color=DOURADO)
    fig.text(0.5, 0.02, label, ha="center", fontsize=10, color=TEXTO_CLARO, fontweight="bold")

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close()
    return buf.getvalue()


def create_waterfall_chart(atual, meta, marketing_pct, alinhamento_pct):
    """Waterfall — Do Cenário Atual ao Cenário Promessa (o gráfico de impacto financeiro)"""
    gap = max(meta - atual, 0)
    total_pct = max(marketing_pct + alinhamento_pct, 1)
    marketing_pct_norm = marketing_pct / total_pct
    alinhamento_pct_norm = alinhamento_pct / total_pct

    ganho_mkt = gap * marketing_pct_norm
    ganho_alin = gap * alinhamento_pct_norm
    promessa = atual + ganho_mkt + ganho_alin

    labels = ["Cenário\nAtual", "Correção de\nCanais / Funil", "Alinhamento\n(Alma)", "Cenário\nPromessa"]
    heights = [atual, ganho_mkt, ganho_alin, promessa]
    bottoms = [0, atual, atual + ganho_mkt, 0]
    colors = [AZUL, AZUL_CLARO, DOURADO, DOURADO_CLARO]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for i in range(4):
        ax.bar(i, heights[i], bottom=bottoms[i], color=colors[i], edgecolor="black", width=0.55)
        rotulo = f"R$ {heights[i]:,.0f}".replace(",", ".")
        ax.text(i, bottoms[i] + heights[i] + (promessa * 0.02), rotulo,
                 ha="center", fontsize=9, fontweight="bold", color=TEXTO_CLARO)

    ax.set_xticks(range(4))
    ax.set_xticklabels(labels, fontsize=9, fontweight="bold", color=TEXTO_CLARO)
    ax.set_title("Impacto Financeiro: Cenário Atual → Cenário Promessa", fontsize=12,
                 fontweight="bold", color=DOURADO, pad=16)
    ax.grid(axis="y", alpha=0.15, color="#888888")
    _estilo_dark(fig, ax)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close()
    return buf.getvalue(), ganho_mkt, ganho_alin, promessa


# ============================================================
# Sanitização de texto para o PDF (CORRIGIDO — antes destruía acentos)
# ============================================================

def sanitize_text(text):
    if not text:
        return ""
    replacements = {
        "™": "(TM)", "©": "(C)", "®": "(R)", "—": "-", "–": "-", "•": "-",
        "→": "->", "★": "*", "■": "[X]", "□": "[ ]", "✓": "OK", "✗": "X",
        "👑": "[CFO]", "📊": "[DATA]", "📥": "[DL]", "💡": "[DICA]",
        "⚠️": "[AVISO]", "❌": "[ERRO]", "✅": "[OK]", "🧠": "[IA]", "📄": "[DOC]",
    }
    for char, repl in replacements.items():
        text = text.replace(char, repl)
    # As fontes nativas do fpdf2 (Helvetica) usam WinAnsi/Latin-1, que já cobre
    # acentuação do português (á, ã, ç, é, í, ó, ú, ê, ô, à, ü...).
    # Antes este código forçava ASCII puro e apagava TODOS os acentos —
    # era o principal motivo de o PDF sair com o português quebrado.
    text = text.encode("latin-1", "ignore").decode("latin-1")
    return text


# ============================================================
# Parser do relatório da IA — marcadores reais em vez de corte por posição
# ============================================================

SECOES_ORDEM = [
    ("SUMARIO_EXECUTIVO", "01. SUMÁRIO EXECUTIVO"),
    ("CONTEXTO", "02. ANÁLISE DE CONTEXTO (Nacional e Internacional)"),
    ("ALMA", "03. DIAGNÓSTICO DA ALMA"),
    ("NEGOCIOS", "04. DIAGNÓSTICO DOS NEGÓCIOS"),
    ("SINTESE", "05. A SÍNTESE (O Pulo do Gato)"),
    ("PLANO_ACAO", "06. PLANO DE AÇÃO TÁTICO"),
    ("ROI", "07. ESTIMATIVA DE INVESTIMENTO & ROI"),
    ("FECHAMENTO", "08. MENSAGEM DE FECHAMENTO"),
]

SCORES_PADRAO = {
    "scorecard": {
        "Produto / Oferta": 55, "Marketing / Aquisição": 50, "Operação / Processos": 55,
        "Financeiro / Gestão": 55, "Pessoas / Energia": 50,
    },
    "radar": {
        "Estratégia": 55, "Execução": 50, "Energia / Alinhamento": 50,
        "Presença Digital": 45, "Potencial de Crescimento": 70,
    },
    "atribuicao_gap": {"marketing_pct": 55, "alinhamento_pct": 45},
}


def parse_relatorio_ia(texto):
    """Separa o texto da IA em seções reais (por marcador) e extrai o bloco JSON de scores."""
    scores = json.loads(json.dumps(SCORES_PADRAO))  # cópia profunda do padrão

    match_scores = re.search(r"===SCORES===\s*(\{.*?\})\s*===FIM===", texto, re.DOTALL)
    if match_scores:
        try:
            scores_ia = json.loads(match_scores.group(1))
            for chave in ("scorecard", "radar", "atribuicao_gap"):
                if isinstance(scores_ia.get(chave), dict) and scores_ia[chave]:
                    scores[chave] = scores_ia[chave]
        except (json.JSONDecodeError, AttributeError):
            pass
        texto = texto[: match_scores.start()]

    secoes = {}
    partes = re.split(r"===SECAO:([A-Z_]+)===", texto)
    if len(partes) > 1:
        it = iter(partes[1:])
        for chave, conteudo in zip(it, it):
            secoes[chave.strip()] = conteudo.strip()
    else:
        # Fallback: a IA não seguiu o formato de marcadores — mostra tudo em uma seção só
        secoes["SUMARIO_EXECUTIVO"] = texto.strip()

    return secoes, scores


# ============================================================
# Geração do PDF — agora com os gráficos de fato inseridos
# ============================================================

def generate_pdf_report(data, secoes, scores):
    relatorio_ok = {k: sanitize_text(v) for k, v in secoes.items()}
    nome_cliente_limpo = sanitize_text(data["nome_cliente"])
    nicho_limpo = sanitize_text(data["nicho"])

    atual = parse_valor_brl(data.get("faturamento_atual"))
    meta = parse_valor_brl(data.get("faturamento_meta"))
    atribuicao = scores.get("atribuicao_gap", SCORES_PADRAO["atribuicao_gap"])

    pdf = FPDF()

    # ============ CAPA ============
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(0, 25, "CFO DA ALMA E DOS NEGOCIOS", ln=True, align="C")

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "(TM)", ln=True, align="C")

    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Relatorio Estrategico Premium", ln=True, align="C")
    pdf.cell(0, 8, "Diagnostico Integrado: Dados + Alma", ln=True, align="C")

    pdf.ln(15)
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(1)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(15)

    # ============ DADOS DO CLIENTE ============
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(0, 8, "INFORMACOES DO CLIENTE", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)

    info_items = [
        ("Cliente:", nome_cliente_limpo),
        ("Data:", datetime.now().strftime("%d/%m/%Y")),
        ("Tipo de Analise:", data["tipo_analise"]),
        ("Nicho:", nicho_limpo),
        ("Faturamento Atual:", f"R$ {data.get('faturamento_atual', 'N/I')}"),
        ("Meta:", f"R$ {data.get('faturamento_meta', 'N/I')}"),
        ("Data de Nascimento:", data.get("data_nascimento", "N/I")),
    ]
    for label, value in info_items:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(50, 7, label)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, str(value), ln=True)

    # ============ PAINEL DE INDICADORES VISUAIS (novo) ============
    graficos = [
        ("PAINEL DE INDICADORES - SCORECARD", create_scorecard_chart(scores["scorecard"])),
        ("PAINEL DE INDICADORES - MATRIZ DE COMPETENCIAS", create_radar_chart(scores["radar"])),
        ("PAINEL DE INDICADORES - TERMOMETRO DA META",
         create_progress_chart(atual, meta if meta > 0 else max(atual, 1), "Faturamento Atual vs. Meta")),
    ]

    waterfall_png, ganho_mkt, ganho_alin, promessa = create_waterfall_chart(
        atual, meta if meta > atual else atual * 1.3,
        atribuicao.get("marketing_pct", 55), atribuicao.get("alinhamento_pct", 45)
    )
    graficos.append(("GRAFICO DE IMPACTO FINANCEIRO", waterfall_png))

    for titulo_grafico, imagem_bytes in graficos:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(212, 175, 55)
        pdf.cell(0, 12, titulo_grafico, ln=True)
        pdf.set_draw_color(212, 175, 55)
        pdf.set_line_width(0.5)
        pdf.line(30, pdf.get_y(), 180, pdf.get_y())
        pdf.ln(8)
        pdf.image(io.BytesIO(imagem_bytes), x=20, w=170)

    # ============ SECOES DO RELATORIO (por marcador real, nao por posicao) ============
    for chave, titulo in SECOES_ORDEM:
        conteudo = relatorio_ok.get(chave, "").strip()
        if not conteudo:
            continue
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(212, 175, 55)
        pdf.cell(0, 12, titulo, ln=True)
        pdf.set_draw_color(212, 175, 55)
        pdf.set_line_width(0.5)
        pdf.line(30, pdf.get_y(), 180, pdf.get_y())
        pdf.ln(5)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 6, conteudo)

    # ============ RODAPE FINAL ============
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(0, 12, "SOBRE O METODO CFO (TM)", ln=True)
    pdf.set_draw_color(212, 175, 55)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(30, 30, 30)

    sobre_texto = sanitize_text(
        "Este relatório foi elaborado com base na metodologia CFO da Alma e dos Negócios™, "
        "criada por Luciano Francisco, combinando análise estratégica de nível McKinsey/Bain com "
        "diagnóstico holístico profundo (numerologia, energia, bloqueios internos).\n\n"
        "19 anos de experiência em educação, marketing, dados, política pública e transformação.\n\n"
        "Mais de 12.000 profissionais treinados | 20+ empresas atendidas | 300+ palestras\n\n"
        "Contato: lucianofrancisco.com.br\n"
        "WhatsApp: Disponível mediante agendamento"
    )
    pdf.multi_cell(0, 6, sobre_texto)

    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, f'Gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")} | CFO da Alma e dos Negocios (TM) | Confidencial',
             ln=True, align="C")

    return bytes(pdf.output())


st.markdown("---")

# ============================================================
# Botão de Geração
# ============================================================
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

FORMATO DE SAÍDA — SIGA EXATAMENTE, SEM DESVIOS (isso alimenta o sistema de geração do PDF):

Escreva cada seção precedida EXATAMENTE pelo marcador abaixo (sem markdown ao redor do marcador, sem traduzir, sem espaços extras):

===SECAO:SUMARIO_EXECUTIVO===
(2 parágrafos ultra-focados: maior ganho do período + principal desafio superado, seguidos de 3 bullets com as métricas mais impactantes)

===SECAO:CONTEXTO===
(relacione os dados com tendências globais de mercado de 2026; posicione o cliente acima ou abaixo da média do setor; use benchmarking)

===SECAO:ALMA===
(SOMENTE se houver data de nascimento: Caminho de Vida, Ano Pessoal 2026, bloqueios energéticos e como o estado interno reflete nos resultados externos. Se não houver data de nascimento, escreva uma breve nota dizendo que a análise energética individual requer a data de nascimento)

===SECAO:NEGOCIOS===
(análise fria dos dados/URLs/KPIs; gargalos operacionais, falhas de marketing, oportunidades de CRM; Data Storytelling: Causa → Efeito → Impacto Financeiro)

===SECAO:SINTESE===
(como a "Alma" do dono impacta diretamente os "Negócios"; conexão entre bloqueios internos e gargalos externos)

===SECAO:PLANO_ACAO===
(3 recomendações estratégicas prioritárias, ordenadas por Impacto e Esforço; cronograma: Dia 1, Dia 2-7, Dia 30 com quick win e métrica esperada, Dia 90 com consolidação e escala)

===SECAO:ROI===
(sugestão macro de alocação de recursos; retorno esperado em 30, 60, 90 dias)

===SECAO:FECHAMENTO===
(convite elegante e profissional para contratar a consultoria; tom exclusivo, transformador, orientado a resultados)

Depois de TODAS as seções de texto, inclua OBRIGATORIAMENTE este bloco de dados estruturados (números inteiros de 0 a 100, sua avaliação honesta com base nos dados fornecidos — isso alimenta os gráficos do relatório, então preencha com critério real, não valores genéricos):

===SCORES===
{{
  "scorecard": {{"Produto / Oferta": 0, "Marketing / Aquisição": 0, "Operação / Processos": 0, "Financeiro / Gestão": 0, "Pessoas / Energia": 0}},
  "radar": {{"Estratégia": 0, "Execução": 0, "Energia / Alinhamento": 0, "Presença Digital": 0, "Potencial de Crescimento": 0}},
  "atribuicao_gap": {{"marketing_pct": 0, "alinhamento_pct": 0}}
}}
===FIM===

Nota sobre atribuicao_gap: marketing_pct + alinhamento_pct deve somar 100. Reflete o quanto do salto entre o faturamento atual e a meta vem de correção de canais/funil (marketing_pct) versus de alinhamento humano/energético (alinhamento_pct), na sua avaliação honesta dos dados.

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

            relatorio_bruto = response.choices[0].message.content
            secoes, scores = parse_relatorio_ia(relatorio_bruto)

            st.success("✅ Relatório Estratégico Premium Gerado com Sucesso!")
            st.markdown("---")

            st.markdown("### 📄 Visualização do Relatório")
            for chave, titulo in SECOES_ORDEM:
                if secoes.get(chave):
                    st.markdown(f"#### {titulo}")
                    st.markdown(secoes[chave])
            st.markdown("---")

            dados_pdf = {
                "nome_cliente": nome_cliente,
                "tipo_analise": tipo_analise,
                "nicho": nicho_mercado or "Não informado",
                "data_nascimento": data_nascimento.strftime('%d/%m/%Y') if data_nascimento else "Não fornecida",
                "faturamento_atual": faturamento_atual or "0",
                "faturamento_meta": faturamento_meta or "0",
            }

            pdf_bytes = generate_pdf_report(dados_pdf, secoes, scores)

            col_download1, col_download2 = st.columns(2)
            with col_download1:
                st.download_button(
                    label="📥 Baixar Relatório em PDF (Executivo)",
                    data=pdf_bytes,
                    file_name=f"Relatorio_CFO_{nome_cliente.replace(' ', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            with col_download2:
                texto_md = "\n\n".join(secoes.get(chave, "") for chave, _ in SECOES_ORDEM if secoes.get(chave))
                nome_arquivo_md = f"Relatorio_CFO_{nome_cliente.replace(' ', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d')}.md"
                st.download_button(
                    label="📄 Baixar Relatório em Markdown",
                    data=texto_md,
                    file_name=nome_arquivo_md,
                    mime="text/markdown"
                )

            st.info("💡 **Dica de Uso Executivo:** O PDF está formatado no padrão McKinsey para apresentação a C-levels, com painel de indicadores visuais (scorecard, radar, termômetro de meta e gráfico de impacto financeiro). Use o Markdown para edições rápidas no Notion/Word.")

        except Exception as e:
            st.error(f"❌ Erro na comunicação com a IA: {str(e)}")
            st.warning("💡 Verifique sua chave API e saldo na conta Groq.")

st.markdown("---")
st.caption("Desenvolvido por Luciano Francisco | CFO da Alma e dos Negócios™ | Metodologia McKinsey-Grade + Diagnóstico Holístico Integrado | 19 Anos de Excelência Estratégica")
