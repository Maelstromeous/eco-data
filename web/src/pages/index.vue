<template>
  <v-container fluid>
    <h1>Eco Farming Calculator</h1>
    <p>Below, choose the level of products you wish to offer, and the current levels. You will then be informed how many crops you need to gather.</p>
    <p>Note: This is heavily WIP!</p>
    <v-row class="mt-2">
      <v-col cols="12" md="9">
        <h2>Product List</h2>
        <p>Choose the products you wish to offer.</p>
        <ProductList :data="data"></ProductList>
      </v-col>
      <v-col cols="12" md="3">
        <h2>Crop Summary</h2>
        <p>Below, you can see the crops you need to gather.</p>
      </v-col>
    </v-row>
  <CropSummary :data></CropSummary>
  </v-container>
</template>

<script setup lang="ts">

import { inject } from 'vue'
import type {Data} from "@/interfaces/data.ts";

const data = inject<Data>('data')
if (!data) throw new Error('data not provided')
</script>
