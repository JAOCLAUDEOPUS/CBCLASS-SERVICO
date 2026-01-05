# -*- coding: utf-8 -*-
import json

with open('data/anexoVIII_correlacao_categorizado.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data.get('itens', [])
print(f'Total items: {len(items)}')
print()

# Contar por categoria
cats = {}
for item in items:
    cat = item.get('filtro_principal', '')
    cats[cat] = cats.get(cat, 0) + 1

print('Categorias e contagens:')
for c in sorted(cats.keys()):
    print(f'  {c}: {cats[c]} itens')

# Verificar subcategorias
print('\nSubcategorias por categoria:')
for cat in sorted(cats.keys()):
    print(f'\n{cat}:')
    subcats = {}
    for item in items:
        if item.get('filtro_principal') == cat:
            sub = item.get('subcategoria', '')
            subcats[sub] = subcats.get(sub, 0) + 1
    
    for sub in sorted(subcats.keys()):
        print(f'  - {sub}: {subcats[sub]} itens')
