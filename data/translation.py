#!/usr/bin/env python3
import json
from pathlib import Path
import re

# Paths
IN_JSON  = Path('Recipes.json')
OUT_JSON = Path('data.json')

# Skill definitions
gather_skills = {'Gathering', 'Farming', 'Milling'}
cook_skills   = {
    'Campfire Cooking', 'Baking', 'Advanced Baking',
    'Cooking', 'Advanced Cooking', 'Butchery', 'Milling'
}

# Exclusions
exclude_tables  = {'laboratory', 'placeholdertable'}
exclude_phrases = {'research paper', 'skill', 'book'}
butcher_substr  = 'butcher'

def should_exclude(table_name: str, item_name: str) -> bool:
    t = table_name.lower()
    n = item_name.lower()
    if any(ex in t for ex in exclude_tables):
        return True
    if any(ph in t or ph in n for ph in exclude_phrases):
        return True
    return False

# Load recipes
with open(IN_JSON, 'r', encoding='utf-8') as f:
    recipes = json.load(f).get('Recipes', [])

# Collect all recipe products and ingredients
prod_rows = []  # holds all potential products
pi_rows   = []  # holds all product-ingredient pairs
for recipe in recipes:
    table = recipe.get('CraftingTable', '')
    variant = recipe.get('Variants', [{}])[0]
    name = variant.get('Name', '')
    if should_exclude(table, name):
        continue
    skills = {sn.get('Skill') for sn in recipe.get('SkillNeeds', [])}
    has_oil = any((ing.get('Tag') or '').lower() == 'oil' for ing in variant.get('Ingredients', []))
    if not (skills & cook_skills or has_oil):
        continue
    # record product row
    products = variant.get('Products', [])
    prod_amount = products[0].get('Ammount', 1) if products else 1
    prod_rows.append({
        'product_name': name,
        'table':        table,
        'product_amount': prod_amount
    })
    # record ingredients
    for ing in variant.get('Ingredients', []):
        iid = ing.get('Name') or ing.get('Tag')
        amt = ing.get('Ammount', 0)
        pi_rows.append({
            'product_name':      name,
            'ingredient_id':     iid,
            'ingredient_amount': amt
        })

# Determine end products: not used as ingredient (unless oil), exclude butcher outputs
used_as_ingredient = {pi['ingredient_id'] for pi in pi_rows}
end_products = []
for p in prod_rows:
    nl = p['product_name'].lower()
    is_oil = 'oil' in nl
    is_butch = butcher_substr in nl
    if (is_oil or p['product_name'] not in used_as_ingredient) and not is_butch:
        end_products.append(p)

# Build crops list: recipes whose name starts with "Grow "
crop_set = set()
for recipe in recipes:
    table = recipe.get('CraftingTable', '')
    variant = recipe.get('Variants', [{}])[0]
    name = variant.get('Name', '')
    if should_exclude(table, name):
        continue
    # Use the "Grow X" pattern to identify crops
    if name.startswith("Grow "):
        raw_name = name[len("Grow "):]
        # Insert a space before each internal capital letter
        formatted = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', raw_name)
        crop_set.add(formatted)
crops = sorted(crop_set)

# Build items list: all ingredients + end products + crops
items_set = set()
items_set.update(used_as_ingredient)
items_set.update(p['product_name'] for p in end_products)
items_set.update(crops)
items = sorted(items_set)

# Assemble products with nested recipes
products = []
for p in end_products:
    recipe_list = [
        {'id':    pi['ingredient_id'],
         'amount': pi['ingredient_amount']}
        for pi in pi_rows
        if pi['product_name'] == p['product_name']
    ]
    products.append({
        'name':           p['product_name'],
        'table':          p['table'],
        'product_amount': p['product_amount'],
        'recipe':         recipe_list
    })

# Final combined data
combined = {
    'items':    items,
    'products': products,
    'crops':    crops
}

# Write to data.json
with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(combined, f, indent=2)
print(f"Wrote combined data → {OUT_JSON}")