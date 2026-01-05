"""
🔍 Sistema de Consulta Tributária - IBS/CBS
Correlação Item LC116, NBS e Classificação Tributária

Aplicação principal Streamlit - Versão Premium Neto Contabilidade
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from config import APP_CONFIG, SEARCH_CONFIG, DATA_FILE
from services import DataService, SearchService


# =============================================================================
# CONFIGURAÇÃO DA PÁGINA E CSS PREMIUM
# =============================================================================

def configure_page():
    """Configura a página do Streamlit com tema premium Neto Contabilidade."""
    st.set_page_config(
        page_title="Sistema de Consulta Tributária IBS/CBS - Neto Contabilidade",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    
    # CSS Premium - Identidade Visual Neto Contabilidade
    st.markdown("""
    <style>
        /* ============================================
           RESET E VARIÁVEIS DE COR
           ============================================ */
        :root {
            --azul-escuro: #1a2332;
            --azul-medio: #2d3e50;
            --dourado: #c9a961;
            --dourado-claro: #e6d5a8;
            --branco: #ffffff;
            --cinza-claro: #b0b8c1;
            --cinza-medio: #8892a0;
        }
        
        /* ============================================
           TEMA GERAL
           ============================================ */
        .main {
            background: linear-gradient(135deg, #1a2332 0%, #2d3e50 100%);
        }
        
        .stApp {
            background: linear-gradient(135deg, #1a2332 0%, #2d3e50 100%);
        }
        
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 2rem;
            max-width: 1400px;
        }
        
        /* Esconder header padrão do Streamlit */
        header[data-testid="stHeader"] {
            display: none;
        }
        
        /* ============================================
           SIDEBAR
           ============================================ */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a2332 0%, #2d3e50 100%);
            border-right: 1px solid rgba(201, 169, 97, 0.3);
        }
        
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: #c9a961 !important;
        }
        
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stMarkdown li,
        [data-testid="stSidebar"] .stMarkdown a {
            color: #b0b8c1 !important;
        }
        
        /* ============================================
           HEADER PREMIUM
           ============================================ */
        .premium-header {
            background: linear-gradient(90deg, #1a2332 0%, #2d3e50 100%);
            padding: 20px 40px;
            border-bottom: 3px solid #c9a961;
            display: flex;
            align-items: center;
            gap: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            margin: -1rem -1rem 2rem -1rem;
        }
        
        .logo-circle {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #c9a961 0%, #e6d5a8 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 24px;
            color: #1a2332;
            box-shadow: 0 4px 15px rgba(201, 169, 97, 0.4);
            flex-shrink: 0;
        }
        
        .header-title {
            font-size: 26px;
            font-weight: 600;
            color: #c9a961;
            margin-bottom: 5px;
        }
        
        .header-subtitle {
            font-size: 14px;
            color: #b0b8c1;
        }
        
        /* ============================================
           HERO DE BUSCA
           ============================================ */
        .search-hero {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(201, 169, 97, 0.3);
            border-radius: 20px;
            padding: 40px 50px;
            margin-bottom: 40px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        }
        
        .search-title {
            font-size: 32px;
            margin-bottom: 15px;
            background: linear-gradient(90deg, #c9a961 0%, #e6d5a8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .search-subtitle {
            color: #b0b8c1;
            margin-bottom: 25px;
            font-size: 16px;
        }
        
        /* ============================================
           CAMPO DE BUSCA ESTILIZADO
           ============================================ */
        .stTextInput > div > div > input {
            background: rgba(255,255,255,0.1) !important;
            border: 2px solid rgba(201, 169, 97, 0.3) !important;
            border-radius: 50px !important;
            padding: 15px 25px !important;
            color: #fff !important;
            font-size: 16px !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #c9a961 !important;
            box-shadow: 0 0 20px rgba(201, 169, 97, 0.3) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #8892a0 !important;
        }
        
        /* ============================================
           SEÇÃO DE CATEGORIAS
           ============================================ */
        .section-title {
            font-size: 22px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            color: #fff;
        }
        
        .section-title::before {
            content: '';
            width: 4px;
            height: 28px;
            background: linear-gradient(180deg, #c9a961 0%, #e6d5a8 100%);
            border-radius: 2px;
        }
        
        /* ============================================
           BOTÕES PREMIUM
           ============================================ */
        .stButton > button {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(201, 169, 97, 0.3) !important;
            border-radius: 12px !important;
            padding: 0.8rem 1.2rem !important;
            font-weight: 500 !important;
            transition: all 0.3s !important;
            color: #c9a961 !important;
            min-height: 90px !important;
        }
        
        .stButton > button:hover {
            background: rgba(201, 169, 97, 0.15) !important;
            border-color: #c9a961 !important;
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(201, 169, 97, 0.25) !important;
        }
        
        .stButton > button[data-testid="stBaseButton-primary"] {
            background: linear-gradient(135deg, rgba(201, 169, 97, 0.3) 0%, rgba(230, 213, 168, 0.2) 100%) !important;
            border: 2px solid #c9a961 !important;
            box-shadow: 0 0 15px rgba(201, 169, 97, 0.3) !important;
        }
        
        /* Botão de limpar/exportar */
        .stDownloadButton > button,
        .stButton > button[kind="secondary"] {
            background: transparent !important;
            border: 2px solid #c9a961 !important;
            color: #c9a961 !important;
            min-height: auto !important;
            padding: 0.5rem 1.5rem !important;
        }
        
        .stDownloadButton > button:hover {
            background: rgba(201, 169, 97, 0.2) !important;
        }
        
        /* ============================================
           TABELA DE RESULTADOS - MELHORIAS CRÍTICAS
           ============================================ */
        [data-testid="stDataFrame"] {
            background: transparent;
            border-radius: 0;
            padding: 20px;
        }
        
        [data-testid="stDataFrame"] table {
            border-collapse: separate !important;
            border-spacing: 0 10px !important; /* ESPAÇO ENTRE LINHAS */
            width: 100% !important;
        }
        
        /* HEADER - VISÍVEL E DESTACADO */
        [data-testid="stDataFrame"] thead th {
            background: rgba(201, 169, 97, 0.25) !important; /* DOURADO MAIS VISÍVEL */
            color: #c9a961 !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            font-size: 13px !important;
            letter-spacing: 1px;
            padding: 16px 15px !important;
            border: none !important;
        }
        
        [data-testid="stDataFrame"] thead th:first-child {
            border-radius: 8px 0 0 8px !important;
        }
        
        [data-testid="stDataFrame"] thead th:last-child {
            border-radius: 0 8px 8px 0 !important;
        }
        
        /* LINHAS - "CARDS" SEPARADOS */
        [data-testid="stDataFrame"] tbody tr {
            background: rgba(255,255,255,0.05) !important; /* FUNDO CLARO VISÍVEL */
            transition: all 0.3s ease;
        }
        
        [data-testid="stDataFrame"] tbody tr:hover {
            background: rgba(255,255,255,0.12) !important; /* MUITO MAIS CLARO NO HOVER */
            transform: scale(1.005);
            box-shadow: 0 4px 20px rgba(201, 169, 97, 0.2) !important;
        }
        
        /* CÉLULAS - ESPAÇOSAS E LEGÍVEIS */
        [data-testid="stDataFrame"] tbody td {
            padding: 18px 15px !important; /* PADDING GENEROSO */
            border-top: 1px solid rgba(201, 169, 97, 0.15) !important;
            border-bottom: 1px solid rgba(201, 169, 97, 0.15) !important;
            font-size: 14px !important;
            color: #e6edf3 !important; /* TEXTO BEM CLARO */
            vertical-align: middle !important;
            line-height: 1.5 !important;
        }
        
        [data-testid="stDataFrame"] tbody td:first-child {
            border-left: 1px solid rgba(201, 169, 97, 0.15) !important;
            border-radius: 8px 0 0 8px !important;
            font-weight: 600 !important;
        }
        
        [data-testid="stDataFrame"] tbody td:last-child {
            border-right: 1px solid rgba(201, 169, 97, 0.15) !important;
            border-radius: 0 8px 8px 0 !important;
        }
        
        /* SCROLLBAR CUSTOMIZADA */
        [data-testid="stDataFrame"]::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        [data-testid="stDataFrame"]::-webkit-scrollbar-track {
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
        }
        
        [data-testid="stDataFrame"]::-webkit-scrollbar-thumb {
            background: rgba(201, 169, 97, 0.5);
            border-radius: 10px;
        }
        
        [data-testid="stDataFrame"]::-webkit-scrollbar-thumb:hover {
            background: rgba(201, 169, 97, 0.8);
        }
        
        /* ============================================
           MENSAGEM SEM RESULTADOS
           ============================================ */
        .no-results {
            text-align: center;
            padding: 60px 20px;
            color: #8892a0;
        }
        
        .no-results-icon {
            font-size: 48px;
            margin-bottom: 20px;
        }
        
        .no-results h3 {
            color: #c9a961;
            margin-bottom: 10px;
        }
        
        /* ============================================
           EXPANDER SIDEBAR
           ============================================ */
        .streamlit-expanderHeader {
            background: rgba(201, 169, 97, 0.1) !important;
            border: 1px solid rgba(201, 169, 97, 0.2) !important;
            border-radius: 8px !important;
            color: #c9a961 !important;
        }
        
        /* ============================================
           DIVIDERS
           ============================================ */
        hr {
            border-color: rgba(201, 169, 97, 0.2) !important;
            margin: 2rem 0 !important;
        }
        
        /* ============================================
           SELECTBOX
           ============================================ */
        .stSelectbox > div > div {
            background: rgba(255,255,255,0.1) !important;
            border: 1px solid rgba(201, 169, 97, 0.3) !important;
            border-radius: 8px !important;
            color: #fff !important;
        }
        
        /* ============================================
           RESULTADOS INFO
           ============================================ */
        .results-info {
            color: #b0b8c1;
            font-size: 14px;
            margin-top: 5px;
        }
        
        /* ============================================
           BADGES - CÓDIGOS E STATUS
           ============================================ */
        .code-badge {
            background: linear-gradient(135deg, #c9a961 0%, #e6d5a8 100%);
            color: #1a2332;
            padding: 7px 14px;
            border-radius: 7px;
            font-weight: 700;
            display: inline-block;
            font-size: 14px;
            box-shadow: 0 2px 10px rgba(201, 169, 97, 0.4);
            letter-spacing: 0.3px;
        }
        
        .nbs-code {
            font-family: 'Courier New', 'Consolas', monospace;
            color: #c9a961;
            font-weight: 600;
            font-size: 13px;
            letter-spacing: 0.5px;
        }
        
        /* ============================================
           ESCONDER ELEMENTOS
           ============================================ */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# MAPEAMENTO DE ÍCONES DAS CATEGORIAS
# =============================================================================

CATEGORY_ICONS = {
    "1. SERVIÇOS FINANCEIROS E BANCÁRIOS": "💼",
    "2. SERVIÇOS DE SAÚDE HUMANA": "🏥",
    "3. SERVIÇOS JURÍDICOS E CONTÁBEIS": "⚖️",
    "4. ENGENHARIA E CONSTRUÇÃO CIVIL": "🏗️",
    "5. TECNOLOGIA DA INFORMAÇÃO": "💻",
    "6. CONSULTORIA E ASSESSORIA": "💡",
    "7. TRANSPORTE E LOGÍSTICA": "🚚",
    "8. EDUCAÇÃO E TREINAMENTO": "📚",
    "9. COMUNICAÇÃO, PUBLICIDADE E EVENTOS": "📢",
    "10. ENTRETENIMENTO E LAZER": "🎭",
    "11. BELEZA E ESTÉTICA": "✨",
    "12. LIMPEZA E CONSERVAÇÃO": "🧹",
    "13. SEGURANÇA": "🔒",
    "14. MANUTENÇÃO E REPARAÇÃO": "🔧",
    "15. RECURSOS HUMANOS": "👥",
    "16. OUTROS SERVIÇOS": "🎯",
}


# =============================================================================
# FUNÇÕES DE EXPORTAÇÃO
# =============================================================================

def export_to_excel(results):
    """Exporta resultados para Excel com formatação profissional."""
    # Preparar dados
    export_data = []
    for item in results:
        for nbs in item.get('nbs_entries', []):
            classificacoes = nbs.get('cclasstrib', [])
            
            # Pegar primeira classificação
            if classificacoes:
                class_info = classificacoes[0]
                cod_class = class_info.get('codigo', '')
                nome_class = class_info.get('nome', '')
                class_completa = f"{cod_class} - {nome_class}"
            else:
                class_completa = "-"
            
            export_data.append({
                'Código LC116': item.get('item_lc116', ''),
                'Descrição do Serviço': item.get('descricao_item', ''),
                'Código NBS': nbs.get('nbs_code', ''),
                'Descrição NBS': nbs.get('descricao_nbs', ''),
                'Prestação Onerosa': 'Sim' if nbs.get('ps_onerosa') == 'S' else 'Não' if nbs.get('ps_onerosa') == 'N' else '-',
                'Aquisição Exterior': 'Sim' if nbs.get('adq_exterior') == 'S' else 'Não' if nbs.get('adq_exterior') == 'N' else '-',
                'INDOP': nbs.get('indop', '-'),
                'Local Incidência IBS': nbs.get('local_incidencia_ibs', '-'),
                'Classificação Tributária': class_completa,
            })
    
    if not export_data:
        return None
    
    # Criar workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Consulta Tributária"
    
    # Definir cabeçalhos
    headers = list(export_data[0].keys())
    ws.append(headers)
    
    # Adicionar dados
    for row_data in export_data:
        ws.append(list(row_data.values()))
    
    # Estilização do cabeçalho
    header_fill = PatternFill(start_color="C9A961", end_color="C9A961", fill_type="solid")
    header_font = Font(name='Calibri', size=11, bold=True, color="1A2332")
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
    
    # Estilização das células de dados
    data_font = Font(name='Calibri', size=10)
    data_alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    
    # Bordas
    thin_border = Border(
        left=Side(style='thin', color='C9A961'),
        right=Side(style='thin', color='C9A961'),
        top=Side(style='thin', color='C9A961'),
        bottom=Side(style='thin', color='C9A961')
    )
    
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=len(headers)):
        for cell in row:
            cell.font = data_font
            cell.alignment = data_alignment
            cell.border = thin_border
    
    # Ajustar largura das colunas
    column_widths = {
        'A': 15,  # Código LC116
        'B': 50,  # Descrição do Serviço
        'C': 18,  # Código NBS
        'D': 50,  # Descrição NBS
        'E': 18,  # Prestação Onerosa
        'F': 18,  # Aquisição Exterior
        'G': 15,  # INDOP
        'H': 40,  # Local Incidência IBS
        'I': 60,  # Classificação
    }
    
    for col_letter, width in column_widths.items():
        ws.column_dimensions[col_letter].width = width
    
    # Criar tabela formatada
    tab = Table(displayName="TabelaTributaria", ref=f"A1:{get_column_letter(len(headers))}{len(export_data)+1}")
    
    # Estilo da tabela (azul escuro e dourado)
    style = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False
    )
    tab.tableStyleInfo = style
    ws.add_table(tab)
    
    # Fixar primeira linha
    ws.freeze_panes = "A2"
    
    # Salvar em BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    return output.getvalue()


# =============================================================================
# COMPONENTES DE UI
# =============================================================================

def render_header():
    """Renderiza o cabeçalho premium."""
    st.markdown("""
    <div class="premium-header">
        <div class="logo-circle">NC</div>
        <div>
            <div class="header-title">Sistema de Consulta Tributária</div>
            <div class="header-subtitle">IBS/CBS - Classificações Tributárias | Neto Contabilidade</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_search_hero():
    """Renderiza a seção hero de busca."""
    st.markdown("""
    <div class="search-hero">
        <div class="search-title">Encontre o Código Tributário Correto</div>
        <div class="search-subtitle">Digite o código LC116, NBS, descrição do serviço ou palavras-chave</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Campo de busca centralizado
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        search_term = st.text_input(
            "Busca",
            placeholder="Ex: Serviços de consultoria, 1.01, administração...",
            label_visibility="collapsed",
            key="main_search"
        )
        
        # Tipo de busca
        col_type1, col_type2, col_type3 = st.columns([1, 1, 1])
        with col_type2:
            search_type = st.selectbox(
                "Tipo",
                ["Contém", "Aproximada", "Exata"],
                label_visibility="collapsed",
                key="search_type"
            )
    
    type_map = {"Contém": "contains", "Aproximada": "fuzzy", "Exata": "exact"}
    return search_term, type_map.get(search_type, "contains")


def render_category_grid(items, search_service):
    """Renderiza o grid de categorias clicáveis."""
    
    # Inicializar session state
    if 'selected_categoria' not in st.session_state:
        st.session_state.selected_categoria = None
    if 'selected_subcategoria' not in st.session_state:
        st.session_state.selected_subcategoria = None
    
    # Contar entradas NBS por categoria (filtrar categorias vazias)
    categoria_counts = {}
    for item in items:
        cat = item.get('filtro_principal', '')
        if cat:  # Ignorar categorias vazias
            nbs_count = len(item.get('nbs_entries', []))
            categoria_counts[cat] = categoria_counts.get(cat, 0) + nbs_count
    
    # Título da seção
    st.markdown('<div class="section-title">Categorias Principais</div>', unsafe_allow_html=True)
    
    # Botão para limpar seleção
    if st.session_state.selected_categoria:
        col_clear = st.columns([1, 2, 1])[1]
        with col_clear:
            if st.button("🔄 Limpar Seleção de Categoria", use_container_width=True, key="clear_cat"):
                st.session_state.selected_categoria = None
                st.session_state.selected_subcategoria = None
                st.rerun()
    
    # Lista de categorias ordenadas alfabeticamente (exceto "OUTROS" que fica por último)
    categorias = sorted(CATEGORY_ICONS.keys())
    
    # Mover "OUTROS SERVIÇOS" para o final
    outros_key = "16. OUTROS SERVIÇOS"
    if outros_key in categorias:
        categorias.remove(outros_key)
        categorias.append(outros_key)
    
    # Grid 4x4
    num_cols = 4
    rows = [categorias[i:i+num_cols] for i in range(0, len(categorias), num_cols)]
    
    for row in rows:
        cols = st.columns(num_cols)
        for idx, cat in enumerate(row):
            with cols[idx]:
                count = categoria_counts.get(cat, 0)
                icon = CATEGORY_ICONS.get(cat, "📋")
                is_selected = st.session_state.selected_categoria == cat
                
                # Nome curto
                cat_name = cat.split(". ", 1)[1] if ". " in cat else cat
                
                # Botão com ícone e nome
                btn_label = f"{icon} {cat_name}\n({count} itens)"
                
                if st.button(btn_label, key=f"cat_{cat}", use_container_width=True, 
                            type="primary" if is_selected else "secondary"):
                    if st.session_state.selected_categoria == cat:
                        st.session_state.selected_categoria = None
                        st.session_state.selected_subcategoria = None
                    else:
                        st.session_state.selected_categoria = cat
                        st.session_state.selected_subcategoria = None
                    st.rerun()
    
    # Subcategorias se houver categoria selecionada
    selected_subcategoria = None
    if st.session_state.selected_categoria:
        st.markdown("---")
        cat_display = st.session_state.selected_categoria.split(". ", 1)[1] if ". " in st.session_state.selected_categoria else st.session_state.selected_categoria
        st.markdown(f'<div class="section-title">📂 Subcategorias de {cat_display}</div>', unsafe_allow_html=True)
        
        subcategorias = search_service.get_subcategorias_by_filtro(items, st.session_state.selected_categoria)
        
        if subcategorias:
            # Contar entradas NBS por subcategoria (filtrar vazias)
            sub_counts = {}
            for item in items:
                if item.get('filtro_principal') == st.session_state.selected_categoria:
                    sub = item.get('subcategoria', '')
                    if sub:  # Ignorar subcategorias vazias
                        nbs_count = len(item.get('nbs_entries', []))
                        sub_counts[sub] = sub_counts.get(sub, 0) + nbs_count
            
            # Botão "Todas"
            col_all = st.columns([1, 2, 1])[1]
            with col_all:
                total = sum(sub_counts.values())
                if st.button(f"📋 Todas as Subcategorias ({total})", key="sub_all", use_container_width=True,
                            type="primary" if st.session_state.selected_subcategoria is None else "secondary"):
                    st.session_state.selected_subcategoria = None
                    st.rerun()
            
            # Grid de subcategorias
            num_sub_cols = 3
            sub_rows = [subcategorias[i:i+num_sub_cols] for i in range(0, len(subcategorias), num_sub_cols)]
            
            for sub_row in sub_rows:
                sub_cols = st.columns(num_sub_cols)
                for idx, sub in enumerate(sub_row):
                    with sub_cols[idx]:
                        count = sub_counts.get(sub, 0)
                        is_sel = st.session_state.selected_subcategoria == sub
                        if st.button(f"📂 {sub} ({count})", key=f"sub_{sub}", use_container_width=True,
                                    type="primary" if is_sel else "secondary"):
                            if st.session_state.selected_subcategoria == sub:
                                st.session_state.selected_subcategoria = None
                            else:
                                st.session_state.selected_subcategoria = sub
                            st.rerun()
            
            selected_subcategoria = st.session_state.selected_subcategoria
    
    return st.session_state.selected_categoria, selected_subcategoria


def render_detailed_view(results):
    """Renderiza visualização detalhada com cards expandiveis."""
    
    st.markdown("""
    <div style='padding: 15px; background: rgba(201, 169, 97, 0.1); border-radius: 8px; margin-bottom: 20px;'>
        <p style='margin: 0; color: #e6d5a8; font-size: 14px;'>
            <strong>Visualizacao Detalhada:</strong> Clique em cada servico para expandir e ver todos os codigos NBS relacionados.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    for item in results:
        lc116 = item.get('item_lc116', '')
        desc_servico = item.get('descricao_item', '')
        nbs_entries = item.get('nbs_entries', [])
        
        # Card do servico LC116
        with st.expander(f"**{lc116}** - {desc_servico[:80]}...", expanded=False):
            
            # Informações do serviço
            st.markdown(f"""
            <div style='background: rgba(45, 62, 80, 0.5); padding: 15px; border-radius: 8px; margin-bottom: 15px;'>
                <div style='color: #c9a961; font-weight: 700; font-size: 16px; margin-bottom: 8px;'>
                    Servico LC116: {lc116}
                </div>
                <div style='color: #e6edf3; font-size: 14px; line-height: 1.6;'>
                    {desc_servico}
                </div>
                <div style='margin-top: 10px; color: #b0b8c1; font-size: 13px;'>
                    <strong>{len(nbs_entries)}</strong> códigos NBS vinculados
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Lista de NBS
            for idx, nbs in enumerate(nbs_entries, 1):
                classificacoes = nbs.get('cclasstrib', [])
                
                # Badge com informações principais
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(201, 169, 97, 0.2) 0%, rgba(230, 213, 168, 0.1) 100%); 
                            border-left: 4px solid #c9a961; padding: 15px; border-radius: 8px; margin-bottom: 12px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                        <div style='color: #c9a961; font-weight: 700; font-size: 15px;'>
                            NBS: {nbs.get('nbs_code', '')}
                        </div>
                        <div style='color: #8892a0; font-size: 12px;'>
                            #{idx} de {len(nbs_entries)}
                        </div>
                    </div>
                    <div style='color: #e6edf3; font-size: 13px; margin-bottom: 12px; line-height: 1.5;'>
                        {nbs.get('descricao_nbs', '')}
                    </div>
                    <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 10px;'>
                        <div style='background: rgba(26, 35, 50, 0.5); padding: 8px; border-radius: 6px;'>
                            <div style='color: #8892a0; font-size: 11px; margin-bottom: 4px;'>Prestação Onerosa</div>
                            <div style='color: #e6d5a8; font-weight: 600; font-size: 13px;'>
                                {'Sim' if nbs.get('ps_onerosa') == 'S' else 'Não' if nbs.get('ps_onerosa') == 'N' else '-'}
                            </div>
                        </div>
                        <div style='background: rgba(26, 35, 50, 0.5); padding: 8px; border-radius: 6px;'>
                            <div style='color: #8892a0; font-size: 11px; margin-bottom: 4px;'>Aquisição Exterior</div>
                            <div style='color: #e6d5a8; font-weight: 600; font-size: 13px;'>
                                {'Sim' if nbs.get('adq_exterior') == 'S' else 'Não' if nbs.get('adq_exterior') == 'N' else '-'}
                            </div>
                        </div>
                        <div style='background: rgba(26, 35, 50, 0.5); padding: 8px; border-radius: 6px;'>
                            <div style='color: #8892a0; font-size: 11px; margin-bottom: 4px;'>INDOP</div>
                            <div style='color: #e6d5a8; font-weight: 600; font-size: 13px; font-family: monospace;'>
                                {nbs.get('indop', '-')}
                            </div>
                        </div>
                        <div style='background: rgba(26, 35, 50, 0.5); padding: 8px; border-radius: 6px;'>
                            <div style='color: #8892a0; font-size: 11px; margin-bottom: 4px;'>Local Incidência IBS</div>
                            <div style='color: #e6d5a8; font-weight: 600; font-size: 12px;'>
                                {nbs.get('local_incidencia_ibs', '-')}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Classificações tributárias
                if classificacoes:
                    st.markdown("""
                    <div style='margin-top: 10px; padding: 10px; background: rgba(201, 169, 97, 0.15); border-radius: 6px;'>
                        <div style='color: #c9a961; font-weight: 700; font-size: 13px; margin-bottom: 8px;'>
                            Classificacoes Tributarias:
                        </div>
                    """, unsafe_allow_html=True)
                    
                    for class_info in classificacoes:
                        st.markdown(f"""
                        <div style='margin-left: 10px; margin-bottom: 5px;'>
                            <span style='color: #c9a961; font-weight: 600; font-family: monospace; font-size: 12px;'>
                                {class_info.get('codigo', '')}
                            </span>
                            <span style='color: #e6edf3; font-size: 12px;'>
                                - {class_info.get('nome', '')}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)


def render_results_table(results, data_service):
    """Renderiza a tabela de resultados profissional com badges e formatação HTML."""
    
    if not results:
        st.markdown("""
        <div class="no-results">
            <div class="no-results-icon">🔍</div>
            <h3>Nenhum resultado encontrado</h3>
            <p>Tente ajustar os filtros ou termos de busca</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Header com contagem e exportação
    total_nbs = sum(len(item.get('nbs_entries', [])) for item in results)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="section-title">Resultados da Busca</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="results-info">{len(results)} serviços, {total_nbs} entradas NBS encontradas</div>', unsafe_allow_html=True)
    
    with col2:
        # Botão de exportação Excel
        excel_data = export_to_excel(results)
        if excel_data:
            from datetime import datetime
            filename = f"consulta_tributaria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            st.download_button(
                label="📊 Exportar Excel",
                data=excel_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Preparar dados para DataFrame com formatação
    table_data = []
    for item in results:
        for nbs in item.get('nbs_entries', []):
            classificacoes = nbs.get('cclasstrib', [])
            
            # Formatar classificação (código + nome)
            if classificacoes:
                class_info = classificacoes[0]  # Pegar primeira classificação
                class_display = f"{class_info.get('codigo', '')}"
                class_nome = class_info.get('nome', '')
            else:
                class_display = "-"
                class_nome = "-"
            
            # Truncar descrições
            desc_servico = item.get('descricao_item', '')
            if len(desc_servico) > 50:
                desc_servico = desc_servico[:50] + '...'
            
            desc_nbs_text = nbs.get('descricao_nbs', '')
            if len(desc_nbs_text) > 50:
                desc_nbs_text = desc_nbs_text[:50] + '...'
            
            # Formatar valores booleanos de forma compacta
            prest_onerosa = nbs.get('ps_onerosa', '')
            if prest_onerosa == 'S':
                prest_onerosa_display = 'Sim'
            elif prest_onerosa == 'N':
                prest_onerosa_display = 'Não'
            else:
                prest_onerosa_display = '-'
            
            aquis_ext = nbs.get('adq_exterior', '')
            if aquis_ext == 'S':
                aquis_ext_display = 'Sim'
            elif aquis_ext == 'N':
                aquis_ext_display = 'Não'
            else:
                aquis_ext_display = '-'
            
            # Truncar local de incidência
            local_incid = nbs.get('local_incidencia_ibs', '')
            if len(local_incid) > 35:
                local_incid = local_incid[:35] + '...'
            
            table_data.append({
                'LC116': item.get("item_lc116", ""),
                'Serviço': desc_servico,
                'NBS': nbs.get("nbs_code", ""),
                'Desc. NBS': desc_nbs_text,
                'Onerosa': prest_onerosa_display,
                'Exterior': aquis_ext_display,
                'INDOP': nbs.get('indop', '-'),
                'Local IBS': local_incid,
                'Cód.': class_display,
                'Classificação': class_nome
            })
    
    if table_data:
        # Usar st.dataframe com estilização customizada
        df = pd.DataFrame(table_data)
        st.markdown("""
        <style>
        div[data-testid="stDataFrame"] {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(201, 169, 97, 0.2);
            border-radius: 15px;
            padding: 15px;
        }
        div[data-testid="stDataFrame"] table {
            color: #e6edf3 !important;
        }
        div[data-testid="stDataFrame"] thead {
            background: rgba(201, 169, 97, 0.25) !important;
        }
        div[data-testid="stDataFrame"] th {
            color: #c9a961 !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            font-size: 13px !important;
            letter-spacing: 1px !important;
            padding: 16px 15px !important;
        }
        div[data-testid="stDataFrame"] tbody tr {
            background: rgba(255,255,255,0.05);
            transition: all 0.3s ease;
        }
        div[data-testid="stDataFrame"] tbody tr:hover {
            background: rgba(255,255,255,0.12) !important;
            box-shadow: 0 4px 20px rgba(201, 169, 97, 0.2);
        }
        div[data-testid="stDataFrame"] td {
            padding: 15px !important;
            font-size: 14px !important;
            color: #e6edf3 !important;
            border-bottom: 1px solid rgba(201, 169, 97, 0.1) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        
        # Tabs para alternar entre visualizacoes
        tab1, tab2 = st.tabs(["Tabela Completa", "Visualizacao Detalhada"])
        
        with tab1:
            # Exibir dataframe com configuracoes otimizadas
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "LC116": st.column_config.TextColumn(
                        "LC116",
                        width="small",
                    ),
                    "Serviço": st.column_config.TextColumn(
                        "Serviço",
                        width="medium",
                    ),
                    "NBS": st.column_config.TextColumn(
                        "NBS",
                        width="medium",
                    ),
                    "Desc. NBS": st.column_config.TextColumn(
                        "Desc. NBS",
                        width="medium",
                    ),
                    "Onerosa": st.column_config.TextColumn(
                        "Onerosa",
                        width="small",
                    ),
                    "Exterior": st.column_config.TextColumn(
                        "Exterior",
                        width="small",
                    ),
                    "INDOP": st.column_config.TextColumn(
                        "INDOP",
                        width="small",
                    ),
                    "Local IBS": st.column_config.TextColumn(
                        "Local IBS",
                        width="medium",
                    ),
                    "Cód.": st.column_config.TextColumn(
                        "Cód.",
                        width="small",
                    ),
                    "Classificação": st.column_config.TextColumn(
                        "Classificação",
                        width="large",
                    ),
                },
                height=600
            )
        
        with tab2:
            # Visualização detalhada com cards expandiveis
            render_detailed_view(results)


def render_sidebar_filters(data_service):
    """Renderiza filtros avançados na sidebar."""
    filters = data_service.filters
    
    st.sidebar.markdown("## ⚙️ Filtros Avançados")
    
    # Botão limpar
    if st.sidebar.button("🔄 Limpar Filtros", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key.startswith('filtro_') or key.startswith('selected_'):
                del st.session_state[key]
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Prestação Onerosa
    with st.sidebar.expander("💰 Prestação Onerosa", expanded=False):
        onerosa = st.radio(
            "Selecione",
            ["Todas", "S", "N"],
            format_func=lambda x: {"Todas": "Todas", "S": "✅ Sim", "N": "❌ Não"}.get(x, x),
            key="filtro_onerosa",
            horizontal=True
        )
    selected_onerosa = None if onerosa == "Todas" else onerosa
    
    # Aquisição Exterior
    with st.sidebar.expander("🌐 Aquisição Exterior", expanded=False):
        exterior = st.radio(
            "Selecione",
            ["Todas", "S", "N"],
            format_func=lambda x: {"Todas": "Todas", "S": "✅ Sim", "N": "❌ Não"}.get(x, x),
            key="filtro_exterior",
            horizontal=True
        )
    selected_exterior = None if exterior == "Todas" else exterior
    
    # Local de Incidência
    with st.sidebar.expander("📍 Local de Incidência", expanded=False):
        locais = ["Todos"] + filters.get('local_incidencia', [])
        local = st.selectbox("Selecione", locais, key="filtro_local")
    selected_local = None if local == "Todos" else local
    
    # Classificação Tributária
    with st.sidebar.expander("🏛️ Classificação Tributária", expanded=False):
        classificacoes = ["Todas"] + filters.get('classificacoes_tributarias', [])
        classificacao = st.selectbox("Selecione", classificacoes, key="filtro_classificacao")
    selected_classificacao = None if classificacao == "Todas" else classificacao
    
    st.sidebar.markdown("---")
    
    # Links úteis
    st.sidebar.markdown("### 📚 Legislação")
    st.sidebar.markdown("""
    - [LC 116/2003](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp116.htm)
    - [Receita Federal](https://www.gov.br/receitafederal)
    - [Reforma Tributária](https://www.gov.br/fazenda/pt-br/assuntos/reforma-tributaria)
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; color: #8892a0; font-size: 11px;">
        <strong>Neto Contabilidade</strong><br>
        Fonte: AnexoVIII Correlação<br>
        v1.0.0 | 2025
    </div>
    """, unsafe_allow_html=True)
    
    return {
        'ps_onerosa': selected_onerosa,
        'adq_exterior': selected_exterior,
        'local_incidencia': selected_local,
        'cclasstrib_filter': selected_classificacao
    }


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """Função principal da aplicação."""
    # Configuração da página
    configure_page()
    
    # Header premium
    render_header()
    
    # Inicializa serviços
    data_service = DataService(DATA_FILE)
    search_service = SearchService(fuzzy_threshold=SEARCH_CONFIG["fuzzy_threshold"])
    
    # Carrega dados
    if not data_service.load_data():
        st.error("❌ Falha ao carregar os dados. Verifique se o arquivo JSON está disponível.")
        st.stop()
    
    # Filtros na sidebar
    sidebar_filters = render_sidebar_filters(data_service)
    
    # Hero de busca
    search_term, search_type = render_search_hero()
    
    # Grid de categorias
    selected_categoria, selected_subcategoria = render_category_grid(data_service.items, search_service)
    
    st.markdown("---")
    
    # Aplicar busca
    results = data_service.items
    
    if search_term and len(search_term) >= SEARCH_CONFIG["min_search_length"]:
        results = search_service.search_items(
            results,
            search_term,
            search_type=search_type
        )
    
    # Aplicar filtros
    results = search_service.filter_items(
        results,
        filtro_principal=selected_categoria,
        subcategoria=selected_subcategoria,
        ps_onerosa=sidebar_filters.get('ps_onerosa'),
        adq_exterior=sidebar_filters.get('adq_exterior'),
        local_incidencia=sidebar_filters.get('local_incidencia'),
        cclasstrib_filter=sidebar_filters.get('cclasstrib_filter')
    )
    
    # Tabela de resultados
    render_results_table(results, data_service)


if __name__ == "__main__":
    main()
