<template>
  <v-container fluid>
    <!-- Loop over each table group -->
    <v-expansion-panels accordion>
      <v-expansion-panel
        v-for="([table, products]) in sortedTables"
        :key="table"
      >
        <v-expansion-panel-title>
          {{ table }}
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-row>
            <!-- Each product: name + number input -->
            <v-col
              v-for="prod in products"
              :key="prod.name"
              cols="12" sm="6" md="4"
            >
              <v-card class="pa-3">
                  <div class="mb-2">
                    <div class="d-flex align-center">
                      <div class="placeholder-square mr-2"></div>
                      <span class="font-weight-medium">{{ prod.name }}</span>
                    </div>
                  </div>
                <div class="mb-2">
                  <p>Products per run: <b>{{ prod.amount }}</b></p>
                </div>
                <div class="d-flex align-center">
                    <!-- number input bound to target level -->
                    <v-text-field
                      class="mr-2 float-left"
                      v-model.number="targets[prod.name]"
                      type="number"
                      label="Target"
                      min="0"
                      dense
                      hide-details
                      style="max-width: 120px"
                    />
                     <!-- number input bound to current level -->
                    <v-text-field
                      v-model.number="current[prod.name]"
                      type="number"
                      label="Current"
                      min="0"
                      dense
                      hide-details
                      style="max-width: 120px"
                    />
                  </div>
                <div class="mt-4">
                  <div class="font-weight-medium mb-2">Ingredients</div>
                  <v-row dense>
                    <v-col
                      v-for="ing in prod.recipe"
                      :key="ing.id"
                      cols="12" sm="6" md="4"
                    >
                      <div class="d-flex align-center">
                        <div class="placeholder-square mr-2"></div>
                        <div>{{ ing.id }} x {{ ing.amount }}</div>
                      </div>
                    </v-col>
                  </v-row>
                </div>
              </v-card>
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type {Data, Product} from '@/interfaces/data'

const props = defineProps<{
  data: Data,
  current: Record<string, number>
  targets: Record<string, number>
}>()

// Group products by their crafting table
const groupedProducts = computed(() => {
  return props.data.products.reduce<Record<string, Product[]>>((acc, prod) => {
    if (!acc[prod.table]) acc[prod.table] = []
    acc[prod.table].push(prod)
    return acc
  }, {})
})

// Create a sorted array of [table, products] entries by table name
// and sort each products list alphabetically
const sortedTables = computed<[string, Product[]][]>(() => {
  return Object.entries(groupedProducts.value)
    // sort products within each table
    .map(([table, prods]) => [
      table,
      prods.slice().sort((p1, p2) => p1.name.localeCompare(p2.name))
    ] as [string, Product[]])
    // then sort tables by table name
    .sort(([a], [b]) => a.localeCompare(b))
})


</script>

<style scoped>
/* Optional: tweak card styling */
.v-card {
  border: 1px solid #e0e0e0;
}
.placeholder-square {
  width: 40px;
  height: 40px;
  background-color: #e0e0e0;
  flex-shrink: 0;
}
</style>
