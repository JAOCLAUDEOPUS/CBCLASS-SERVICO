"""
Serviço de carregamento e gerenciamento de dados.
"""
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import streamlit as st


class DataService:
    """Classe para gerenciamento de dados do sistema."""
    
    def __init__(self, data_file: Path):
        self.data_file = data_file
        self._data: Optional[Dict] = None
        self._items: List[Dict] = []
        self._filters: Dict[str, set] = {}
        
    @st.cache_data(ttl=3600)
    def _load_json(_self, file_path: str) -> Dict:
        """Carrega o arquivo JSON com cache."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_data(self) -> bool:
        """Carrega os dados do arquivo JSON."""
        try:
            self._data = self._load_json(str(self.data_file))
            self._items = self._data.get('itens', [])
            self._extract_filters()
            return True
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return False
    
    def _extract_filters(self):
        """Extrai os filtros únicos dos dados."""
        filtros_principais = set()
        subcategorias = set()
        codigos_nbs = set()
        local_incidencia = set()
        cclasstrib_codes = set()
        
        for item in self._items:
            if fp := item.get('filtro_principal'):
                filtros_principais.add(fp)
            if sub := item.get('subcategoria'):
                subcategorias.add(sub)
            
            for nbs in item.get('nbs_entries', []):
                if code := nbs.get('nbs_code'):
                    codigos_nbs.add(code)
                if local := nbs.get('local_incidencia_ibs'):
                    local_incidencia.add(local)
                for cc in nbs.get('cclasstrib', []):
                    if codigo := cc.get('codigo'):
                        cclasstrib_codes.add(f"{codigo} - {cc.get('nome', '')}")
        
        self._filters = {
            'filtros_principais': sorted(filtros_principais),
            'subcategorias': sorted(subcategorias),
            'codigos_nbs': sorted(codigos_nbs),
            'local_incidencia': sorted(local_incidencia),
            'classificacoes_tributarias': sorted(cclasstrib_codes),
        }
    
    @property
    def items(self) -> List[Dict]:
        """Retorna a lista de itens."""
        return self._items
    
    @property
    def filters(self) -> Dict[str, List]:
        """Retorna os filtros disponíveis."""
        return self._filters
    
    @property
    def source_info(self) -> Dict[str, str]:
        """Retorna informações da fonte de dados."""
        if self._data:
            return {
                'fonte': self._data.get('fonte', 'N/A'),
                'sheet': self._data.get('sheet', 'N/A'),
            }
        return {'fonte': 'N/A', 'sheet': 'N/A'}
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas dos dados."""
        total_items = len(self._items)
        total_nbs = sum(len(item.get('nbs_entries', [])) for item in self._items)
        total_cclasstrib = sum(
            len(nbs.get('cclasstrib', []))
            for item in self._items
            for nbs in item.get('nbs_entries', [])
        )
        
        return {
            'total_items': total_items,
            'total_nbs_entries': total_nbs,
            'total_classificacoes': total_cclasstrib,
            'total_filtros_principais': len(self._filters.get('filtros_principais', [])),
            'total_subcategorias': len(self._filters.get('subcategorias', [])),
        }
