#!/usr/bin/env python3
"""
Generate outputs from Recipes.json:
 - crops.csv: list of raw resources (recipes requiring gathering skills)
 - products.csv: list of end products (not used as ingredients elsewhere), with table and flat target amount=0; oils always included; exclude butcher items
 - product_ingredients.csv: mapping of each selected recipe to its ingredients with correctly spelled 'amount'

Excludes recipes with tables or names containing 'Laboratory', 'PlaceHolderTable', 'Research Paper', 'Skill', or 'Book'.
"""

import json
import csv
import sys
from pathlib import Path

# File paths
IN_JSON      = Path('Recipes.json')
CROPS_CSV    = Path('crops.csv')
PROD_CSV     = Path('products.csv')
PROD_ING_CSV = Path('product_ingredients.csv')

# Skill groups
gather_skills = {'Gathering', 'Farming', 'Milling'}
cook_skills   = {
    'Campfire Cooking',
    'Baking',
    'Advanced Baking',
    'Cooking',
    'Advanced Cooking',
    'Butchery',
    'Milling'
}

# Exclusion keywords
exclude_tables  = {'laboratory', 'placeholdertable'}
exclude_phrases = {'research paper', 'skill', 'book'}

# Load JSON data
try:
    with open(IN_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error loading {IN_JSON}: {e}", file=sys.stderr)
    sys.exit(1)

# Iterate recipes and first variant
def iterate_variants(recipes):
    for recipe in recipes:
        variant = recipe.get('Variants', [{}])[0]
        yield recipe, variant

# Helper to check exclusions
def should_exclude(table_name: str, item_name: str) -> bool:
    t = table_name.lower()
    n = item_name.lower()
    if any(ex in t for ex in exclude_tables):
        return True
    for phrase in exclude_phrases:
        if phrase in t or phrase in n:
            return True
    return False

# 1. Generate crops.csv
crop_rows = []
seen = set()
for recipe, variant in iterate_variants(data.get('Recipes', [])):
    table = recipe.get('CraftingTable', '')
    name  = variant.get('Name', '')
    if should_exclude(table, name):
        continue
    skills = {sn.get('Skill') for sn in recipe.get('SkillNeeds', [])}
    if skills.intersection(gather_skills) and name not in seen:
        crop_rows.append({'crop_name': name})
        seen.add(name)

crop_rows.sort(key=lambda x: x['crop_name'].lower())
with open(CROPS_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['crop_name'])
    writer.writeheader()
    writer.writerows(crop_rows)
print(f"Wrote crops CSV → {CROPS_CSV}")

# 2. Generate product_ingredients.csv and provisional prod_rows
pi_rows = []
prod_rows = []
for recipe, variant in iterate_variants(data.get('Recipes', [])):
    table = recipe.get('CraftingTable', '')
    name  = variant.get('Name', '')
    if should_exclude(table, name):
        continue
    skills = {sn.get('Skill') for sn in recipe.get('SkillNeeds', [])}
    has_oil = any((ing.get('Tag') or '').lower() == 'oil' for ing in variant.get('Ingredients', []))
    if skills.intersection(cook_skills) or has_oil:
        prod_rows.append({'product_name': name, 'table': table, 'amount': 0})
        for ing in variant.get('Ingredients', []):
            iid = ing.get('Name') or ing.get('Tag')
            amt = ing.get('Ammount', 0)
            pi_rows.append({
                'product_name':      name,
                'ingredient_id':     iid,
                'ingredient_amount': amt
            })

# Write product_ingredients.csv
pi_rows.sort(key=lambda x: (x['product_name'].lower(), (x['ingredient_id'] or '').lower()))
with open(PROD_ING_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['product_name', 'ingredient_id', 'ingredient_amount'])
    writer.writeheader()
    writer.writerows(pi_rows)
print(f"Wrote product ingredients CSV → {PROD_ING_CSV}")

# 3. Filter prod_rows to end products (not used as ingredients), except oils; exclude butcher products
ingredient_set = {row['ingredient_id'] for row in pi_rows}
final_products = []
for row in prod_rows:
    name_lower = row['product_name'].lower()
    is_oil = 'oil' in name_lower
    is_butcher = 'butcher' in name_lower
    if (is_oil or row['product_name'] not in ingredient_set) and not is_butcher:
        final_products.append(row)

final_products.sort(key=lambda x: x['product_name'].lower())
with open(PROD_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['product_name', 'table', 'amount'])
    writer.writeheader()
    writer.writerows(final_products)
print(f"Wrote products CSV → {PROD_CSV}")
