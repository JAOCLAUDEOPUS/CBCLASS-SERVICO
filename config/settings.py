"""
Configurações globais do sistema de pesquisa tributária.
"""
from pathlib import Path

# Diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações da aplicação
APP_CONFIG = {
    "title": "📋 Sistema de Consulta Tributária - IBS/CBS",
    "subtitle": "Correlação Item LC116, NBS e Classificação Tributária",
    "version": "1.0.0",
    "page_icon": "🔍",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Configurações de pesquisa
SEARCH_CONFIG = {
    "min_search_length": 2,
    "max_results_per_page": 50,
    "fuzzy_threshold": 60,
    "highlight_color": "#FFEB3B",
}

# Configurações de exibição
DISPLAY_CONFIG = {
    "show_nbs_limit": 10,
    "expand_all_default": False,
}

# Cores para categorias
CATEGORY_COLORS = {
    "5. TECNOLOGIA DA INFORMAÇÃO": "#3498db",
    "1. SERVIÇOS PROFISSIONAIS": "#9b59b6",
    "2. SAÚDE": "#27ae60",
    "3. EDUCAÇÃO": "#e74c3c",
    "4. CONSTRUÇÃO E IMÓVEIS": "#f39c12",
    "6. COMUNICAÇÃO E MARKETING": "#1abc9c",
    "7. TRANSPORTE E LOGÍSTICA": "#34495e",
    "8. SERVIÇOS FINANCEIROS": "#95a5a6",
    "9. TURISMO E HOSPITALIDADE": "#e91e63",
    "10. MANUTENÇÃO E REPAROS": "#00bcd4",
    "11. SERVIÇOS PESSOAIS": "#ff5722",
    "12. ESPORTES E LAZER": "#4caf50",
    "13. AGRICULTURA E PECUÁRIA": "#8bc34a",
    "14. SERVIÇOS INDUSTRIAIS": "#607d8b",
    "15. ENTRETENIMENTO E CULTURA": "#9c27b0",
    "16. OUTROS SERVIÇOS": "#795548",
}

# Ícones para filtros principais
CATEGORY_ICONS = {
    "5. TECNOLOGIA DA INFORMAÇÃO": "💻",
    "1. SERVIÇOS PROFISSIONAIS": "👔",
    "2. SAÚDE": "🏥",
    "3. EDUCAÇÃO": "📚",
    "4. CONSTRUÇÃO E IMÓVEIS": "🏗️",
    "6. COMUNICAÇÃO E MARKETING": "📢",
    "7. TRANSPORTE E LOGÍSTICA": "🚚",
    "8. SERVIÇOS FINANCEIROS": "💰",
    "9. TURISMO E HOSPITALIDADE": "✈️",
    "10. MANUTENÇÃO E REPAROS": "🔧",
    "11. SERVIÇOS PESSOAIS": "💇",
    "12. ESPORTES E LAZER": "⚽",
    "13. AGRICULTURA E PECUÁRIA": "🌾",
    "14. SERVIÇOS INDUSTRIAIS": "🏭",
    "15. ENTRETENIMENTO E CULTURA": "🎭",
    "16. OUTROS SERVIÇOS": "📦",
}

# Caminho do arquivo de dados
DATA_FILE = BASE_DIR / "data" / "anexoVIII_correlacao_categorizado.json"
