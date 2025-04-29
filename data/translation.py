#!/usr/bin/env python3
import json
from pathlib import Path

# Paths
IN_JSON  = Path('Recipes.json')
OUT_JSON = Path('combined.json')

# Skills and exclusions
COOK_SKILLS    = {
    'Campfire Cooking', 'Baking', 'Advanced Baking',
    'Cooking', 'Advanced Cooking', 'Butchery', 'Milling'
}
EXCLUDE_TABLES  = {'laboratory', 'placeholdertable'}
EXCLUDE_PHRASES = {'research paper', 'skill', 'book'}
BUTCHER_SUBSTR  = 'butcher'

def should_exclude(table: str, name: str) -> bool:
    """Return True if table or recipe name contains any exclusion."""
    t = table.lower()
    n = name.lower()
    if any(ex in t for ex in EXCLUDE_TABLES):
        return True
    if any(ph in t or ph in n for ph in EXCLUDE_PHRASES):
        return True
    return False

# Load all recipes
with open(IN_JSON, 'r', encoding='utf-8') as f:
    data = json.load(f).get('Recipes', [])

# Step 1: collect all product recipes and their ingredients
prod_rows = []
pi_rows   = []

for recipe in data:
    table   = recipe.get('CraftingTable', '')
    variant = recipe.get('Variants', [{}])[0]
    name    = variant.get('Name', '')
    if should_exclude(table, name):
        continue

    # Include if cooking skill applies, or if any ingredient has Tag "Oil"
    skills = {sn.get('Skill') for sn in recipe.get('SkillNeeds', [])}
    has_oil = any((ing.get('Tag') or '').lower() == 'oil'
                  for ing in variant.get('Ingredients', []))
    if not (skills & COOK_SKILLS or has_oil):
        continue

    # Record the product itself
    products = variant.get('Products', [])
    amount   = products[0].get('Ammount', 1) if products else 1
    prod_rows.append({
        'product_name':   name,
        'table':          table,
        'amount': amount
    })

    # Record each ingredient for that product
    for ing in variant.get('Ingredients', []):
        iid = ing.get('Name') or ing.get('Tag')
        amt = ing.get('Ammount', 0)
        pi_rows.append({
            'product_name':      name,
            'ingredient_id':     iid,
            'ingredient_amount': amt
        })

# Step 2: determine which products are end-products
used_as_ingredient = {pi['ingredient_id'] for pi in pi_rows}
end_products = []
for p in prod_rows:
    nl        = p['product_name'].lower()
    is_oil    = 'oil' in nl
    is_butch  = BUTCHER_SUBSTR in nl
    # keep if not used as ingredient (or is oil) and not a butcher output
    if (is_oil or p['product_name'] not in used_as_ingredient) and not is_butch:
        end_products.append(p)

# Step 3: build items list
items = sorted({
    *used_as_ingredient,
    *(p['product_name'] for p in end_products)
})

# Step 4: assemble products with their recipes
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
        'amount': p['amount'],
        'recipe':         recipe_list
    })

# Step 5: write combined.json
combined = {'items': items, 'products': products}
with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(combined, f, indent=2)
print(f"Wrote combined JSON → {OUT_JSON}")