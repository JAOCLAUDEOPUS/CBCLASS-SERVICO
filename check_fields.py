# -*- coding: utf-8 -*-
import json

with open('data/anexoVIII_correlacao_categorizado.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

item = data['itens'][0]
nbs = item['nbs_entries'][0]

print('Campos disponíveis no NBS:')
print('=' * 60)
for key in sorted(nbs.keys()):
    value = nbs[key]
    if isinstance(value, list) and value:
        print(f'{key}: [lista com {len(value)} itens]')
        if key == 'cclasstrib' and value:
            print(f'  Exemplo: {value[0]}')
    else:
        print(f'{key}: {value}')
