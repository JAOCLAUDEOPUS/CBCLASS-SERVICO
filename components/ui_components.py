"""
Componentes de UI reutilizáveis para o sistema.
"""
import streamlit as st
from typing import Dict, List, Any, Optional


def render_item_card(item: Dict, expanded: bool = False, highlight_query: str = None) -> None:
    """Renderiza um card de item com suas informações."""
    item_code = item.get('item_lc116', 'N/A')
    descricao = item.get('descricao_item', 'Sem descrição')
    filtro_principal = item.get('filtro_principal', 'N/A')
    subcategoria = item.get('subcategoria', 'N/A')
    nbs_entries = item.get('nbs_entries', [])
    
    # Título do expander
    title = f"📌 **{item_code}** - {descricao[:80]}{'...' if len(descricao) > 80 else ''}"
    
    with st.expander(title, expanded=expanded):
        # Informações principais
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**🏷️ Item LC116:** `{item_code}`")
            st.markdown(f"**📁 Filtro Principal:** {filtro_principal}")
        
        with col2:
            st.markdown(f"**📂 Subcategoria:** {subcategoria}")
            st.markdown(f"**📊 Total NBS:** `{len(nbs_entries)}`")
        
        st.markdown("---")
        st.markdown(f"**📝 Descrição Completa:**")
        st.info(descricao)
        
        # Tabela de NBS
        if nbs_entries:
            st.markdown("### 📋 Entradas NBS")
            render_nbs_table(nbs_entries)


def render_nbs_table(nbs_entries: List[Dict]) -> None:
    """Renderiza a tabela de entradas NBS."""
    for idx, nbs in enumerate(nbs_entries, 1):
        with st.container():
            st.markdown(f"#### NBS {idx}: `{nbs.get('nbs_code', 'N/A')}`")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                ps_value = "✅ Sim" if nbs.get('ps_onerosa') == 'S' else "❌ Não"
                st.markdown(f"**PS Onerosa:** {ps_value}")
            
            with col2:
                adq_value = "✅ Sim" if nbs.get('adq_exterior') == 'S' else "❌ Não"
                st.markdown(f"**Adq. Exterior:** {adq_value}")
            
            with col3:
                st.markdown(f"**INDOP:** `{nbs.get('indop', 'N/A')}`")
            
            with col4:
                st.markdown(f"**Local Incidência:** {nbs.get('local_incidencia_ibs', 'N/A')}")
            
            st.markdown(f"**Descrição NBS:** {nbs.get('descricao_nbs', 'N/A')}")
            
            # Classificações tributárias
            cclasstrib = nbs.get('cclasstrib', [])
            if cclasstrib:
                st.markdown("**🏛️ Classificações Tributárias:**")
                for cc in cclasstrib:
                    codigo = cc.get('codigo', 'N/A')
                    nome = cc.get('nome', 'N/A')
                    st.markdown(f"  - `{codigo}`: {nome}")
            
            if idx < len(nbs_entries):
                st.markdown("---")


def render_statistics_cards(stats: Dict[str, Any]) -> None:
    """Renderiza cards de estatísticas."""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="📌 Total de Itens",
            value=f"{stats.get('total_items', 0):,}".replace(',', '.')
        )
    
    with col2:
        st.metric(
            label="📋 Entradas NBS",
            value=f"{stats.get('total_nbs_entries', 0):,}".replace(',', '.')
        )
    
    with col3:
        st.metric(
            label="🏛️ Classificações",
            value=f"{stats.get('total_classificacoes', 0):,}".replace(',', '.')
        )
    
    with col4:
        st.metric(
            label="📁 Filtros Principais",
            value=stats.get('total_filtros_principais', 0)
        )
    
    with col5:
        st.metric(
            label="📂 Subcategorias",
            value=stats.get('total_subcategorias', 0)
        )


def render_search_box() -> tuple:
    """Renderiza a caixa de pesquisa."""
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "🔍 Pesquisar",
            placeholder="Digite o termo de busca (descrição, código, NBS...)",
            key="search_query",
            help="Pesquise por descrição do item, código LC116, código NBS ou descrição NBS"
        )
    
    with col2:
        search_type = st.selectbox(
            "Tipo de Busca",
            options=["contains", "fuzzy", "exact", "regex"],
            format_func=lambda x: {
                "contains": "📝 Contém",
                "fuzzy": "🔮 Aproximada",
                "exact": "🎯 Exata",
                "regex": "⚡ Regex"
            }.get(x, x),
            key="search_type"
        )
    
    return query, search_type


def render_filters_sidebar(filters: Dict[str, List], items: List[Dict], search_service) -> Dict:
    """Renderiza os filtros na sidebar."""
    st.sidebar.markdown("## 🎛️ Filtros")
    
    selected_filters = {}
    
    # Filtro Principal
    st.sidebar.markdown("### 📁 Filtro Principal")
    filtros_principais = ["Todos"] + filters.get('filtros_principais', [])
    selected_filtro = st.sidebar.selectbox(
        "Categoria",
        options=filtros_principais,
        key="filtro_principal",
        label_visibility="collapsed"
    )
    selected_filters['filtro_principal'] = None if selected_filtro == "Todos" else selected_filtro
    
    # Subcategoria (dinâmica baseada no filtro principal)
    st.sidebar.markdown("### 📂 Subcategoria")
    if selected_filters['filtro_principal']:
        subcategorias = ["Todas"] + search_service.get_subcategorias_by_filtro(
            items, selected_filters['filtro_principal']
        )
    else:
        subcategorias = ["Todas"] + filters.get('subcategorias', [])
    
    selected_sub = st.sidebar.selectbox(
        "Subcategoria",
        options=subcategorias,
        key="subcategoria",
        label_visibility="collapsed"
    )
    selected_filters['subcategoria'] = None if selected_sub == "Todas" else selected_sub
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Filtros Secundários")
    
    # PS Onerosa
    ps_options = ["Todos", "S", "N"]
    selected_ps = st.sidebar.selectbox(
        "Prestação Onerosa",
        options=ps_options,
        format_func=lambda x: {"Todos": "Todos", "S": "✅ Sim", "N": "❌ Não"}.get(x, x),
        key="ps_onerosa"
    )
    selected_filters['ps_onerosa'] = None if selected_ps == "Todos" else selected_ps
    
    # Aquisição Exterior
    adq_options = ["Todos", "S", "N"]
    selected_adq = st.sidebar.selectbox(
        "Aquisição Exterior",
        options=adq_options,
        format_func=lambda x: {"Todos": "Todos", "S": "✅ Sim", "N": "❌ Não"}.get(x, x),
        key="adq_exterior"
    )
    selected_filters['adq_exterior'] = None if selected_adq == "Todos" else selected_adq
    
    # Local de Incidência
    st.sidebar.markdown("### 📍 Local de Incidência")
    locais = ["Todos"] + filters.get('local_incidencia', [])
    selected_local = st.sidebar.selectbox(
        "Local",
        options=locais,
        key="local_incidencia",
        label_visibility="collapsed"
    )
    selected_filters['local_incidencia'] = None if selected_local == "Todos" else selected_local
    
    # Classificação Tributária
    st.sidebar.markdown("### 🏛️ Classificação Tributária")
    classificacoes = ["Todas"] + filters.get('classificacoes_tributarias', [])
    selected_class = st.sidebar.selectbox(
        "Classificação",
        options=classificacoes,
        key="cclasstrib",
        label_visibility="collapsed"
    )
    selected_filters['cclasstrib_filter'] = None if selected_class == "Todas" else selected_class
    
    return selected_filters


def render_results_header(total_results: int, total_items: int) -> None:
    """Renderiza o cabeçalho dos resultados."""
    if total_results == total_items:
        st.markdown(f"### 📊 Exibindo todos os **{total_results}** itens")
    else:
        st.markdown(f"### 📊 Encontrados **{total_results}** de **{total_items}** itens")


def render_pagination(total_items: int, items_per_page: int = 20) -> tuple:
    """Renderiza controles de paginação."""
    total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if total_pages > 1:
            current_page = st.number_input(
                f"Página (de {total_pages})",
                min_value=1,
                max_value=total_pages,
                value=1,
                key="current_page"
            )
        else:
            current_page = 1
    
    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    
    return start_idx, end_idx, current_page, total_pages


def render_no_results():
    """Renderiza mensagem de nenhum resultado encontrado."""
    st.warning("🔍 Nenhum item encontrado com os critérios selecionados.")
    st.markdown("""
    **Sugestões:**
    - Tente termos de busca mais genéricos
    - Verifique a ortografia
    - Use a busca aproximada (fuzzy) para encontrar termos similares
    - Remova alguns filtros
    """)
