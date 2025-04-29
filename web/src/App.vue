<template>
  <CropSummary></CropSummary>
  <ProductList></ProductList>
</template>

<script setup lang="ts">
import ProductList from "@/components/ProductList.vue";
import CropSummary from "@/components/CropSummary.vue";

import { inject } from 'vue'

interface Ingredient { id: string; amount: number }
interface Product {
  name: string
  table: string
  product_amount: number
  recipe: Ingredient[]
}

type Data = { items: string[]; products: Product[] }

const data = inject<Data>('data')
if (!data) throw new Error('data not provided')


</script>
