"""
Serviço de busca e filtragem de dados - VERSÃO APRIMORADA
Implementa melhorias de busca: sinônimos, correspondência parcial, normalização de acentos,
busca por código, autocompletar e destaque de termos.
"""
from typing import Dict, List, Optional, Tuple, Set
from unidecode import unidecode
from rapidfuzz import fuzz, process
import re


# =============================================================================
# DICIONÁRIO DE SINÔNIMOS E PALAVRAS-CHAVE
# =============================================================================

SINONIMOS_SERVICOS = {
    # Tecnologia e Informática
    "desenvolvimento de sistemas": ["software", "programação", "aplicativo", "app", "sistema", "código", "developer", "dev", "programador"],
    "análise de sistemas": ["analista", "requisitos", "especificação", "levantamento"],
    "processamento de dados": ["dados", "data", "processamento", "batch", "etl"],
    "consultoria em informática": ["ti", "tecnologia", "computação", "suporte técnico", "help desk"],
    "licenciamento de software": ["licença", "software", "programa", "aplicativo", "assinatura"],
    "hospedagem": ["hosting", "servidor", "cloud", "nuvem", "datacenter", "data center"],
    "manutenção de computadores": ["hardware", "equipamento", "reparo", "conserto", "assistência técnica"],
    
    # Contabilidade e Finanças
    "contabilidade": ["contador", "contábil", "escrituração", "balanço", "balancete", "demonstrações"],
    "auditoria": ["auditor", "revisão", "exame", "verificação", "conformidade"],
    "consultoria financeira": ["finanças", "investimento", "planejamento financeiro", "gestão financeira"],
    "assessoria tributária": ["impostos", "tributos", "fiscal", "tributação", "tax"],
    "perícia contábil": ["perito", "laudo", "judicial", "cálculo judicial"],
    
    # Jurídico
    "advocacia": ["advogado", "jurídico", "direito", "legal", "assessoria jurídica"],
    "consultoria jurídica": ["parecer", "opinião legal", "análise jurídica"],
    
    # Saúde
    "medicina": ["médico", "saúde", "clínica", "hospital", "atendimento médico"],
    "odontologia": ["dentista", "dental", "dente", "odonto"],
    "psicologia": ["psicólogo", "terapia", "psicoterapia", "saúde mental"],
    "fisioterapia": ["fisioterapeuta", "reabilitação", "rpg", "pilates terapêutico"],
    "enfermagem": ["enfermeiro", "home care", "cuidador"],
    "exames": ["laboratório", "análise clínica", "diagnóstico", "imagem"],
    
    # Engenharia e Construção
    "engenharia": ["engenheiro", "projeto", "cálculo estrutural", "obra"],
    "arquitetura": ["arquiteto", "projeto arquitetônico", "design de interiores"],
    "construção civil": ["obra", "edificação", "reforma", "construção"],
    "instalações": ["elétrica", "hidráulica", "ar condicionado", "climatização"],
    
    # Marketing e Comunicação
    "publicidade": ["propaganda", "anúncio", "mídia", "marketing", "advertising"],
    "design gráfico": ["designer", "arte", "layout", "identidade visual", "logo"],
    "assessoria de imprensa": ["comunicação", "pr", "relações públicas", "mídia"],
    
    # Educação
    "ensino": ["educação", "curso", "aula", "treinamento", "capacitação"],
    "escola": ["colégio", "instituição de ensino", "educacional"],
    
    # Transporte
    "transporte": ["frete", "logística", "entrega", "distribuição", "carga"],
    "mudança": ["remoção", "transferência", "mudanças"],
    
    # Outros
    "limpeza": ["higienização", "conservação", "zeladoria", "faxina"],
    "segurança": ["vigilância", "monitoramento", "proteção", "alarme"],
    "manutenção": ["reparo", "conserto", "assistência", "suporte"],
    "locação": ["aluguel", "arrendamento", "cessão"],
}

# Mapeamento de classificações tributárias para descrições didáticas
CLASSIFICACOES_DIDATICAS = {
    # Tributação Integral
    "000001": {
        "categoria": "Tributação Integral",
        "descricao": "Serviço tributado integralmente pelo IBS/CBS",
        "cor": "#4CAF50",  # Verde
        "icone": "💰"
    },
    # Alíquota Reduzida / Regimes Especiais (códigos 200xxx)
    "200029": {
        "categoria": "Alíquota Reduzida",
        "descricao": "Serviços de saúde humana (Anexo III) - Redução de alíquota",
        "cor": "#2196F3",  # Azul
        "icone": "🏥"
    },
    "200039": {
        "categoria": "Alíquota Reduzida",
        "descricao": "Produções artísticas nacionais (Anexo X) - Redução de alíquota",
        "cor": "#9C27B0",  # Roxo
        "icone": "🎭"
    },
    "200040": {
        "categoria": "Regime Especial",
        "descricao": "Comunicação institucional à administração pública",
        "cor": "#FF9800",  # Laranja
        "icone": "📢"
    },
    "200052": {
        "categoria": "Alíquota Reduzida",
        "descricao": "Serviços de profissões intelectuais - Redução de alíquota",
        "cor": "#00BCD4",  # Ciano
        "icone": "🎓"
    },
    # Planos e Seguros (códigos 011xxx)
    "011001": {
        "categoria": "Regime Especial",
        "descricao": "Planos de assistência funerária",
        "cor": "#795548",  # Marrom
        "icone": "📋"
    },
    # Isenções (códigos 400xxx, 410xxx)
    "400001": {
        "categoria": "Isenção/Não Incidência",
        "descricao": "Operação isenta de IBS/CBS",
        "cor": "#607D8B",  # Cinza azulado
        "icone": "🚫"
    },
    "410001": {
        "categoria": "Imunidade",
        "descricao": "Operação imune (exportação de serviços)",
        "cor": "#9E9E9E",  # Cinza
        "icone": "🌍"
    },
}

# Categorias padrão para códigos não mapeados
CATEGORIA_PADRAO_POR_PREFIXO = {
    "000": {"categoria": "Tributação Integral", "cor": "#4CAF50", "icone": "💰"},
    "011": {"categoria": "Regime Especial", "cor": "#FF9800", "icone": "📋"},
    "200": {"categoria": "Alíquota Reduzida", "cor": "#2196F3", "icone": "📉"},
    "220": {"categoria": "Alíquota Reduzida", "cor": "#2196F3", "icone": "📉"},
    "400": {"categoria": "Isenção/Não Incidência", "cor": "#607D8B", "icone": "🚫"},
    "410": {"categoria": "Imunidade", "cor": "#9E9E9E", "icone": "🌍"},
    "510": {"categoria": "Regime Especial", "cor": "#FF9800", "icone": "⚙️"},
    "550": {"categoria": "Regime Especial", "cor": "#FF9800", "icone": "⚙️"},
}

# Grupos de serviços da LC 116
GRUPOS_LC116 = {
    "1": "Serviços de Informática e Congêneres",
    "2": "Pesquisas e Desenvolvimento",
    "3": "Locação de Bens Móveis",
    "4": "Serviços de Saúde, Assistência e Congêneres",
    "5": "Medicina e Assistência Veterinária",
    "6": "Cuidados Pessoais, Estética e Congêneres",
    "7": "Engenharia, Arquitetura, Geologia, etc.",
    "8": "Educação, Ensino, Orientação Pedagógica",
    "9": "Hospedagem, Turismo, Viagens e Congêneres",
    "10": "Intermediação e Congêneres",
    "11": "Guarda, Estacionamento e Congêneres",
    "12": "Diversões, Lazer, Entretenimento",
    "13": "Fotografia e Cinematografia",
    "14": "Reprografia e Digitalização",
    "15": "Serralheria, Chaveiros e Congêneres",
    "16": "Transporte, Armazenagem, Carga e Congêneres",
    "17": "Apoio Técnico, Administrativo e Congêneres",
    "18": "Regulação e Fiscalização",
    "19": "Hospedagem e Turismo",
    "20": "Portuários, Aeroportuários e Congêneres",
    "21": "Registros Públicos, Cartorários e Notariais",
    "22": "Exploração de Rodovias",
    "23": "Programação Visual, Desenho Industrial",
    "24": "Chaveiros, Confecção de Carimbos e Congêneres",
    "25": "Funerários",
    "26": "Coleta, Remessa e Entrega de Correspondências",
    "27": "Assistência Social",
    "28": "Avaliação de Bens",
    "29": "Biblioteconomia",
    "30": "Biologia, Biotecnologia e Química",
    "31": "Serviços Técnicos em Edificações",
    "32": "Desenhos Técnicos",
    "33": "Desembaraço Aduaneiro, Despachantes",
    "34": "Investigações Particulares, Detetives",
    "35": "Reportagem, Jornalismo, Relações Públicas",
    "36": "Meteorologia",
    "37": "Artistas, Atletas, Modelos",
    "38": "Museologia",
    "39": "Ourivesaria e Lapidação",
    "40": "Obras de Arte sob Encomenda",
}


class SearchServiceEnhanced:
    """Classe para operações de busca e filtragem aprimoradas."""

    def __init__(self, fuzzy_threshold: int = 60):
        self.fuzzy_threshold = fuzzy_threshold
        self._build_keyword_index()

    def _build_keyword_index(self):
        """Constrói índice invertido de sinônimos para busca rápida."""
        self.keyword_index = {}
        for termo_principal, sinonimos in SINONIMOS_SERVICOS.items():
            # Indexar termo principal
            normalized_principal = self.normalize_text(termo_principal)
            self.keyword_index[normalized_principal] = termo_principal
            # Indexar sinônimos
            for sinonimo in sinonimos:
                normalized_sin = self.normalize_text(sinonimo)
                self.keyword_index[normalized_sin] = termo_principal

    @staticmethod
    def normalize_text(text: str) -> str:
        """Normaliza texto para busca (remove acentos, lowercase, espaços extras)."""
        if not text:
            return ""
        # Remove acentos e converte para lowercase
        normalized = unidecode(text.lower().strip())
        # Remove caracteres especiais exceto números e pontos (para códigos)
        normalized = re.sub(r'[^\w\s\.]', ' ', normalized)
        # Remove espaços múltiplos
        normalized = re.sub(r'\s+', ' ', normalized)
        return normalized.strip()

    def expand_query_with_synonyms(self, query: str) -> Set[str]:
        """Expande a query com sinônimos relacionados."""
        normalized_query = self.normalize_text(query)
        terms = set([normalized_query])
        
        # Verificar se a query corresponde a algum sinônimo
        for key, principal in self.keyword_index.items():
            if normalized_query in key or key in normalized_query:
                # Adicionar termo principal e todos os sinônimos
                terms.add(self.normalize_text(principal))
                for sin in SINONIMOS_SERVICOS.get(principal, []):
                    terms.add(self.normalize_text(sin))
        
        # Verificar match parcial em sinônimos
        for termo_principal, sinonimos in SINONIMOS_SERVICOS.items():
            normalized_principal = self.normalize_text(termo_principal)
            if normalized_query in normalized_principal:
                terms.add(normalized_principal)
                for sin in sinonimos:
                    terms.add(self.normalize_text(sin))
            for sin in sinonimos:
                if normalized_query in self.normalize_text(sin):
                    terms.add(normalized_principal)
                    terms.add(self.normalize_text(sin))
        
        return terms

    def is_code_query(self, query: str) -> Tuple[bool, str]:
        """Verifica se a query é um código (LC116, NBS, etc)."""
        normalized = self.normalize_text(query)
        
        # Padrão LC116: X.XX ou XX.XX
        lc116_pattern = r'^\d{1,2}\.\d{2}$'
        # Padrão NBS: X.XXXX.XX.XX
        nbs_pattern = r'^\d\.\d{4}\.\d{2}\.\d{2}$'
        # Padrão parcial de código
        partial_code_pattern = r'^[\d\.]+$'
        
        if re.match(lc116_pattern, normalized):
            return True, "lc116"
        elif re.match(nbs_pattern, normalized):
            return True, "nbs"
        elif re.match(partial_code_pattern, normalized) and len(normalized) >= 2:
            return True, "partial"
        
        return False, ""

    def search_items(
        self,
        items: List[Dict],
        query: str,
        search_type: str = "contains",
        search_fields: List[str] = None,
        use_synonyms: bool = True
    ) -> List[Dict]:
        """
        Pesquisa itens baseado na query com suporte aprimorado.

        Args:
            items: Lista de itens para pesquisar
            query: Termo de busca
            search_type: Tipo de busca ('contains', 'exact', 'fuzzy', 'regex')
            search_fields: Campos para pesquisar
            use_synonyms: Se deve usar expansão por sinônimos

        Returns:
            Lista de itens que correspondem à busca, ordenados por relevância
        """
        if not query or len(query) < 2:
            return items

        if search_fields is None:
            search_fields = ['descricao_item', 'item_lc116']

        # Verificar se é busca por código
        is_code, code_type = self.is_code_query(query)
        
        if is_code:
            return self._search_by_code(items, query, code_type)

        # Busca normal com possível expansão por sinônimos
        normalized_query = self.normalize_text(query)
        
        # Expandir query com sinônimos se habilitado
        search_terms = set([normalized_query])
        if use_synonyms and search_type != "exact":
            search_terms = self.expand_query_with_synonyms(query)

        results_with_scores = []

        for item in items:
            match_score = self._calculate_match_score(
                item, search_terms, search_type, search_fields, normalized_query
            )
            if match_score > 0:
                results_with_scores.append((item, match_score))

        # Ordenar por relevância (score) decrescente
        results_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [item for item, score in results_with_scores]

    def _search_by_code(self, items: List[Dict], query: str, code_type: str) -> List[Dict]:
        """Busca específica por código."""
        normalized_query = self.normalize_text(query)
        results = []

        for item in items:
            # Buscar no código LC116
            item_code = self.normalize_text(item.get('item_lc116', ''))
            if normalized_query in item_code or item_code.startswith(normalized_query):
                results.append(item)
                continue

            # Buscar nos códigos NBS
            for nbs in item.get('nbs_entries', []):
                nbs_code = self.normalize_text(nbs.get('nbs_code', ''))
                if normalized_query in nbs_code:
                    results.append(item)
                    break

        return results

    def _calculate_match_score(
        self,
        item: Dict,
        search_terms: Set[str],
        search_type: str,
        search_fields: List[str],
        original_query: str
    ) -> float:
        """Calcula score de relevância para um item."""
        max_score = 0.0

        for field in search_fields:
            value = item.get(field, '')
            if not value:
                continue

            normalized_value = self.normalize_text(str(value))

            for term in search_terms:
                score = 0.0

                if search_type == "contains":
                    if term in normalized_value:
                        # Bonus para match exato no início
                        if normalized_value.startswith(term):
                            score = 100.0
                        else:
                            score = 80.0
                        # Bonus se for o termo original (não sinônimo)
                        if term == original_query:
                            score += 20.0
                            
                elif search_type == "exact":
                    if term == normalized_value:
                        score = 100.0
                        
                elif search_type == "fuzzy":
                    ratio = fuzz.partial_ratio(term, normalized_value)
                    if ratio >= self.fuzzy_threshold:
                        score = ratio
                        # Bonus para match com termo original
                        if term == original_query:
                            score += 10.0
                            
                elif search_type == "regex":
                    try:
                        if re.search(term, normalized_value, re.IGNORECASE):
                            score = 80.0
                    except re.error:
                        if term in normalized_value:
                            score = 70.0

                max_score = max(max_score, score)

        # Busca também nas descrições NBS
        for nbs in item.get('nbs_entries', []):
            nbs_desc = self.normalize_text(nbs.get('descricao_nbs', ''))
            nbs_code = self.normalize_text(nbs.get('nbs_code', ''))

            for term in search_terms:
                if search_type == "contains":
                    if term in nbs_desc:
                        score = 60.0  # Score menor para match em NBS
                        if term == original_query:
                            score += 10.0
                        max_score = max(max_score, score)
                    if term in nbs_code:
                        max_score = max(max_score, 90.0)  # Score alto para código
                        
                elif search_type == "fuzzy":
                    ratio = fuzz.partial_ratio(term, nbs_desc)
                    if ratio >= self.fuzzy_threshold:
                        max_score = max(max_score, ratio * 0.7)  # Peso menor

        return max_score

    def get_autocomplete_suggestions(
        self,
        items: List[Dict],
        partial_query: str,
        max_suggestions: int = 10
    ) -> List[Dict]:
        """
        Retorna sugestões de autocompletar baseadas na query parcial.

        Returns:
            Lista de dicts com: {'texto': str, 'tipo': str, 'codigo': str}
        """
        if not partial_query or len(partial_query) < 2:
            return []

        normalized_query = self.normalize_text(partial_query)
        suggestions = []
        seen = set()

        # Verificar se parece código
        is_code, _ = self.is_code_query(partial_query)

        for item in items:
            # Sugestões por código LC116
            item_code = item.get('item_lc116', '')
            if item_code and self.normalize_text(item_code).startswith(normalized_query):
                key = f"lc116_{item_code}"
                if key not in seen:
                    desc = item.get('descricao_item', '')[:50]
                    suggestions.append({
                        'texto': f"{item_code} - {desc}",
                        'tipo': 'LC116',
                        'codigo': item_code,
                        'score': 100 if is_code else 80
                    })
                    seen.add(key)

            # Sugestões por descrição do serviço
            desc = item.get('descricao_item', '')
            normalized_desc = self.normalize_text(desc)
            if normalized_query in normalized_desc:
                key = f"desc_{item.get('item_lc116', '')}"
                if key not in seen:
                    suggestions.append({
                        'texto': f"{desc[:60]}... ({item.get('item_lc116', '')})",
                        'tipo': 'Serviço',
                        'codigo': item.get('item_lc116', ''),
                        'score': 90 if normalized_desc.startswith(normalized_query) else 70
                    })
                    seen.add(key)

            # Sugestões por código NBS
            for nbs in item.get('nbs_entries', []):
                nbs_code = nbs.get('nbs_code', '')
                if nbs_code and self.normalize_text(nbs_code).startswith(normalized_query):
                    key = f"nbs_{nbs_code}"
                    if key not in seen:
                        nbs_desc = nbs.get('descricao_nbs', '')[:40]
                        suggestions.append({
                            'texto': f"{nbs_code} - {nbs_desc}",
                            'tipo': 'NBS',
                            'codigo': nbs_code,
                            'score': 95 if is_code else 75
                        })
                        seen.add(key)

        # Ordenar por score e limitar
        suggestions.sort(key=lambda x: x['score'], reverse=True)
        return suggestions[:max_suggestions]

    def filter_items(
        self,
        items: List[Dict],
        filtro_principal: Optional[str] = None,
        subcategoria: Optional[str] = None,
        ps_onerosa: Optional[str] = None,
        adq_exterior: Optional[str] = None,
        local_incidencia: Optional[str] = None,
        cclasstrib_filter: Optional[str] = None,
        tipo_tributacao: Optional[str] = None,  # NOVO: Filtro didático
        grupo_lc116: Optional[str] = None  # NOVO: Filtro por grupo
    ) -> List[Dict]:
        """
        Aplica filtros aos itens com suporte a filtros didáticos.

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

        # NOVO: Filtro por tipo de tributação (didático)
        if tipo_tributacao:
            results = self._filter_by_tipo_tributacao(results, tipo_tributacao)

        # NOVO: Filtro por grupo LC116
        if grupo_lc116:
            results = self._filter_by_grupo_lc116(results, grupo_lc116)

        return results

    def _filter_by_tipo_tributacao(self, items: List[Dict], tipo: str) -> List[Dict]:
        """Filtra itens pela categoria didática de tributação."""
        tipo_lower = tipo.lower()
        
        def item_matches_tipo(item: Dict) -> bool:
            for nbs in item.get('nbs_entries', []):
                for cc in nbs.get('cclasstrib', []):
                    codigo = cc.get('codigo', '')
                    info = self.get_classificacao_didatica(codigo)
                    if tipo_lower in info['categoria'].lower():
                        return True
            return False

        return [i for i in items if item_matches_tipo(i)]

    def _filter_by_grupo_lc116(self, items: List[Dict], grupo: str) -> List[Dict]:
        """Filtra itens pelo grupo da LC116."""
        # Extrair número do grupo se vier com descrição
        grupo_num = grupo.split(' ')[0].replace('.', '') if ' ' in grupo else grupo
        
        def item_in_grupo(item: Dict) -> bool:
            item_code = item.get('item_lc116', '')
            if not item_code:
                return False
            # Extrair número do grupo do código (parte antes do ponto)
            item_grupo = item_code.split('.')[0]
            return item_grupo == grupo_num

        return [i for i in items if item_in_grupo(i)]

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

    def get_grupos_lc116_disponiveis(self, items: List[Dict]) -> List[Dict]:
        """Retorna lista de grupos LC116 disponíveis nos dados."""
        grupos_encontrados = set()
        for item in items:
            item_code = item.get('item_lc116', '')
            if item_code:
                grupo_num = item_code.split('.')[0]
                grupos_encontrados.add(grupo_num)
        
        # Montar lista com número e descrição
        resultado = []
        for grupo_num in sorted(grupos_encontrados, key=lambda x: int(x)):
            descricao = GRUPOS_LC116.get(grupo_num, f"Grupo {grupo_num}")
            resultado.append({
                'numero': grupo_num,
                'descricao': descricao,
                'display': f"{grupo_num} - {descricao}"
            })
        return resultado

    def get_tipos_tributacao_disponiveis(self, items: List[Dict]) -> List[Dict]:
        """Retorna tipos de tributação disponíveis com descrições didáticas."""
        tipos = {
            "Tributação Integral": {
                "descricao": "Serviço sujeito à alíquota padrão de IBS/CBS",
                "icone": "💰",
                "cor": "#4CAF50"
            },
            "Alíquota Reduzida": {
                "descricao": "Serviço com benefício de redução de alíquota",
                "icone": "📉",
                "cor": "#2196F3"
            },
            "Regime Especial": {
                "descricao": "Serviço sujeito a regime tributário especial",
                "icone": "⚙️",
                "cor": "#FF9800"
            },
            "Isenção/Não Incidência": {
                "descricao": "Serviço não sujeito a IBS/CBS (isenções)",
                "icone": "🚫",
                "cor": "#607D8B"
            },
            "Imunidade": {
                "descricao": "Serviço imune (ex: exportações)",
                "icone": "🌍",
                "cor": "#9E9E9E"
            },
        }
        
        return [
            {"nome": nome, **info}
            for nome, info in tipos.items()
        ]

    @staticmethod
    def get_classificacao_didatica(codigo: str) -> Dict:
        """Retorna informações didáticas sobre uma classificação tributária."""
        if codigo in CLASSIFICACOES_DIDATICAS:
            return CLASSIFICACOES_DIDATICAS[codigo]
        
        # Tentar por prefixo
        prefixo = codigo[:3] if len(codigo) >= 3 else codigo
        if prefixo in CATEGORIA_PADRAO_POR_PREFIXO:
            info = CATEGORIA_PADRAO_POR_PREFIXO[prefixo]
            return {
                "categoria": info["categoria"],
                "descricao": f"Classificação {codigo}",
                "cor": info["cor"],
                "icone": info["icone"]
            }
        
        # Fallback
        return {
            "categoria": "Outros",
            "descricao": f"Classificação {codigo}",
            "cor": "#757575",
            "icone": "📋"
        }

    def highlight_text(
        self,
        text: str,
        query: str,
        highlight_color: str = "#FFEB3B",
        highlight_class: str = "search-highlight"
    ) -> str:
        """Destaca o termo de busca no texto com suporte a múltiplas ocorrências."""
        if not query or not text:
            return text

        normalized_query = self.normalize_text(query)
        normalized_text = self.normalize_text(text)

        # Encontrar todas as posições
        highlighted = text
        offset = 0
        
        # Buscar todas as ocorrências
        pos = normalized_text.find(normalized_query)
        while pos != -1:
            # Calcular posição ajustada no texto original
            actual_pos = pos + offset
            match_text = text[actual_pos:actual_pos + len(query)]
            
            # Criar HTML de highlight
            highlight_html = (
                f"<span class='{highlight_class}' style='background-color: {highlight_color}; "
                f"padding: 2px 4px; border-radius: 3px; font-weight: 600;'>"
                f"{match_text}</span>"
            )
            
            # Substituir no texto
            highlighted = (
                highlighted[:actual_pos] +
                highlight_html +
                highlighted[actual_pos + len(query):]
            )
            
            # Ajustar offset para próxima busca
            offset += len(highlight_html) - len(query)
            
            # Buscar próxima ocorrência
            pos = normalized_text.find(normalized_query, pos + 1)

        return highlighted

    def get_filter_counts(self, items: List[Dict]) -> Dict[str, Dict]:
        """Retorna contagem de itens para cada opção de filtro."""
        counts = {
            'tipos_tributacao': {},
            'grupos_lc116': {},
            'locais_incidencia': {},
            'ps_onerosa': {'S': 0, 'N': 0},
            'adq_exterior': {'S': 0, 'N': 0},
        }

        for item in items:
            # Contagem por grupo LC116
            item_code = item.get('item_lc116', '')
            if item_code:
                grupo = item_code.split('.')[0]
                counts['grupos_lc116'][grupo] = counts['grupos_lc116'].get(grupo, 0) + 1

            for nbs in item.get('nbs_entries', []):
                # Prestação onerosa
                ps = nbs.get('ps_onerosa', '')
                if ps in counts['ps_onerosa']:
                    counts['ps_onerosa'][ps] += 1

                # Aquisição exterior
                adq = nbs.get('adq_exterior', '')
                if adq in counts['adq_exterior']:
                    counts['adq_exterior'][adq] += 1

                # Local de incidência
                local = nbs.get('local_incidencia_ibs', '')
                if local:
                    counts['locais_incidencia'][local] = counts['locais_incidencia'].get(local, 0) + 1

                # Tipo de tributação
                for cc in nbs.get('cclasstrib', []):
                    codigo = cc.get('codigo', '')
                    info = self.get_classificacao_didatica(codigo)
                    categoria = info['categoria']
                    counts['tipos_tributacao'][categoria] = counts['tipos_tributacao'].get(categoria, 0) + 1

        return counts
