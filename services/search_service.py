"""
Serviço de busca e filtragem de dados.
"""
from typing import Dict, List, Optional, Tuple
from unidecode import unidecode
from rapidfuzz import fuzz, process
import re


class SearchService:
    """Classe para operações de busca e filtragem."""
    
    def __init__(self, fuzzy_threshold: int = 60):
        self.fuzzy_threshold = fuzzy_threshold
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normaliza texto para busca (remove acentos, lowercase)."""
        if not text:
            return ""
        return unidecode(text.lower().strip())
    
    def search_items(
        self,
        items: List[Dict],
        query: str,
        search_type: str = "contains",
        search_fields: List[str] = None
    ) -> List[Dict]:
        """
        Pesquisa itens baseado na query.
        
        Args:
            items: Lista de itens para pesquisar
            query: Termo de busca
            search_type: Tipo de busca ('contains', 'exact', 'fuzzy', 'regex')
            search_fields: Campos para pesquisar
        
        Returns:
            Lista de itens que correspondem à busca
        """
        if not query or len(query) < 2:
            return items
        
        if search_fields is None:
            search_fields = ['descricao_item', 'item_lc116']
        
        normalized_query = self.normalize_text(query)
        results = []
        
        for item in items:
            if self._item_matches(item, normalized_query, search_type, search_fields):
                results.append(item)
        
        return results
    
    def _item_matches(
        self,
        item: Dict,
        query: str,
        search_type: str,
        search_fields: List[str]
    ) -> bool:
        """Verifica se um item corresponde à query."""
        for field in search_fields:
            value = item.get(field, '')
            if not value:
                continue
            
            normalized_value = self.normalize_text(str(value))
            
            if search_type == "contains":
                if query in normalized_value:
                    return True
            elif search_type == "exact":
                if query == normalized_value:
                    return True
            elif search_type == "fuzzy":
                score = fuzz.partial_ratio(query, normalized_value)
                if score >= self.fuzzy_threshold:
                    return True
            elif search_type == "regex":
                try:
                    if re.search(query, normalized_value, re.IGNORECASE):
                        return True
                except re.error:
                    if query in normalized_value:
                        return True
        
        # Busca também nas descrições NBS
        for nbs in item.get('nbs_entries', []):
            nbs_desc = self.normalize_text(nbs.get('descricao_nbs', ''))
            nbs_code = self.normalize_text(nbs.get('nbs_code', ''))
            
            if search_type == "contains":
                if query in nbs_desc or query in nbs_code:
                    return True
            elif search_type == "fuzzy":
                if fuzz.partial_ratio(query, nbs_desc) >= self.fuzzy_threshold:
                    return True
        
        return False
    
    def filter_items(
        self,
        items: List[Dict],
        filtro_principal: Optional[str] = None,
        subcategoria: Optional[str] = None,
        ps_onerosa: Optional[str] = None,
        adq_exterior: Optional[str] = None,
        local_incidencia: Optional[str] = None,
        cclasstrib_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Aplica filtros aos itens.
        
        Returns:
            Lista de itens filtrados
        """
        results = items.copy()
        
        if filtro_principal:
            results = [i for i in results if i.get('filtro_principal') == filtro_principal]
        
        if subcategoria:
            results = [i for i in results if i.get('subcategoria') == subcategoria]
        
        if ps_onerosa:
            results = [
                i for i in results
                if any(nbs.get('ps_onerosa') == ps_onerosa for nbs in i.get('nbs_entries', []))
            ]
        
        if adq_exterior:
            results = [
                i for i in results
                if any(nbs.get('adq_exterior') == adq_exterior for nbs in i.get('nbs_entries', []))
            ]
        
        if local_incidencia:
            results = [
                i for i in results
                if any(nbs.get('local_incidencia_ibs') == local_incidencia for nbs in i.get('nbs_entries', []))
            ]
        
        if cclasstrib_filter:
            codigo_filter = cclasstrib_filter.split(' - ')[0] if ' - ' in cclasstrib_filter else cclasstrib_filter
            results = [
                i for i in results
                if any(
                    cc.get('codigo') == codigo_filter
                    for nbs in i.get('nbs_entries', [])
                    for cc in nbs.get('cclasstrib', [])
                )
            ]
        
        return results
    
    def get_subcategorias_by_filtro(
        self,
        items: List[Dict],
        filtro_principal: str
    ) -> List[str]:
        """Retorna subcategorias disponíveis para um filtro principal."""
        subcategorias = set()
        for item in items:
            if item.get('filtro_principal') == filtro_principal:
                if sub := item.get('subcategoria'):
                    subcategorias.add(sub)
        return sorted(subcategorias)
    
    def highlight_text(self, text: str, query: str, highlight_color: str = "#FFEB3B") -> str:
        """Destaca o termo de busca no texto."""
        if not query or not text:
            return text
        
        normalized_query = self.normalize_text(query)
        normalized_text = self.normalize_text(text)
        
        # Encontra a posição no texto normalizado
        pos = normalized_text.find(normalized_query)
        if pos == -1:
            return text
        
        # Aplica o highlight no texto original
        highlighted = (
            f"{text[:pos]}"
            f"<mark style='background-color: {highlight_color}; padding: 2px 4px; border-radius: 3px;'>"
            f"{text[pos:pos+len(query)]}</mark>"
            f"{text[pos+len(query):]}"
        )
        return highlighted
