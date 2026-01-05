# -*- coding: utf-8 -*-
import json

with open('data/anexoVIII_correlacao_categorizado.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data.get('itens', [])

# Listar categorias únicas
unique_cats = set(item.get('filtro_principal', '') for item in items if item.get('filtro_principal'))
print('Categorias únicas no JSON:')
print('=' * 80)
for cat in sorted(unique_cats):
    count = sum(1 for item in items if item.get('filtro_principal') == cat)
    nbs_count = sum(len(item.get('nbs_entries', [])) for item in items if item.get('filtro_principal') == cat)
    print(f'{cat}: {count} serviços LC116, {nbs_count} entradas NBS')

# Verificar um item completo
print('\n' + '=' * 80)
print('Exemplo de item completo:')
print('=' * 80)
if items:
    item = items[0]
    print(f"item_lc116: {item.get('item_lc116')}")
    print(f"descricao_item: {item.get('descricao_item')[:50]}...")
    print(f"filtro_principal: {item.get('filtro_principal')}")
    print(f"subcategoria: {item.get('subcategoria')}")
    
    if item.get('nbs_entries'):
        nbs = item['nbs_entries'][0]
        print(f"\nPrimeira entrada NBS:")
        print(f"  nbs_code: {nbs.get('nbs_code')}")
        print(f"  descricao_nbs: {nbs.get('descricao_nbs')[:50]}...")
        print(f"  prest_onerosa: {nbs.get('prest_onerosa')}")
        print(f"  aquis_ext: {nbs.get('aquis_ext')}")
        
        if nbs.get('cclasstrib'):
            cc = nbs['cclasstrib'][0]
            print(f"\n  Primeira classificação:")
            print(f"    codigo: {cc.get('codigo')}")
            print(f"    descricao: {cc.get('descricao')}")
