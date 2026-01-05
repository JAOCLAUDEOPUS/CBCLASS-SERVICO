# Sistema de Consulta Tributária - IBS/CBS

Sistema profissional para consulta e pesquisa de dados tributários baseado na correlação entre Item LC116, NBS e Classificação Tributária.

## 📋 Funcionalidades

- **Pesquisa Avançada**: Busca por descrição, código LC116, código NBS
- **Múltiplos Tipos de Busca**: 
  - Contém (padrão)
  - Busca Aproximada (Fuzzy)
  - Busca Exata
  - Expressões Regulares (Regex)
- **Filtros Principais**: Categorias de serviços
- **Filtros Secundários**: 
  - Subcategoria
  - Prestação Onerosa
  - Aquisição Exterior
  - Local de Incidência IBS
  - Classificação Tributária
- **Interface Responsiva**: Layout adaptável
- **Paginação**: Navegação eficiente por grandes volumes de dados

## 🚀 Instalação

1. **Clone ou copie o projeto**

2. **Crie um ambiente virtual**:
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**:
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

## 💻 Execução

```bash
streamlit run app.py
```

O aplicativo estará disponível em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
pesquisa_tributaria/
├── app.py                  # Aplicação principal
├── requirements.txt        # Dependências Python
├── README.md              # Este arquivo
├── config/
│   ├── __init__.py
│   └── settings.py        # Configurações globais
├── services/
│   ├── __init__.py
│   ├── data_service.py    # Serviço de dados
│   └── search_service.py  # Serviço de busca
├── components/
│   ├── __init__.py
│   └── ui_components.py   # Componentes de UI
└── data/
    └── anexoVIII_correlacao_categorizado.json  # Dados
```

## 📊 Estrutura dos Dados

O sistema utiliza um arquivo JSON com a seguinte estrutura:

- **item_lc116**: Código do item na LC116
- **descricao_item**: Descrição do serviço
- **filtro_principal**: Categoria principal
- **subcategoria**: Subcategoria do serviço
- **nbs_entries**: Lista de entradas NBS contendo:
  - nbs_code: Código NBS
  - descricao_nbs: Descrição NBS
  - ps_onerosa: Prestação onerosa (S/N)
  - adq_exterior: Aquisição exterior (S/N)
  - indop: Indicador de operação
  - local_incidencia_ibs: Local de incidência
  - cclasstrib: Classificações tributárias

## 🔧 Configuração

As configurações podem ser ajustadas em `config/settings.py`:

- Parâmetros de busca (threshold fuzzy, limite de resultados)
- Cores e ícones por categoria
- Caminho do arquivo de dados

## 📝 Licença

Uso interno.
