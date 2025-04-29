<template>
    <v-table>
      <thead>
        <tr>
          <th class="text-left">Crop</th>
          <th class="text-left">Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="_, crop in amounts" :key="crop">
          <td>{{ crop }}</td>
          <td :class="{ 'text-red': amounts[crop] > 0 }">
            <b>{{ amounts[crop] }}</b>
          </td>
        </tr>
      </tbody>
    </v-table>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type {Data} from "@/interfaces/data.ts";

// Props: list of crop names
const props = defineProps<{
  data: Data,
  current: Record<string, number>
  targets: Record<string, number>
}>()


// Computed map of crop name -> required amount
const amounts = computed(() => {
  const result: Record<string, number> = {}
  // initialize all to zero
  for (const crop of props.data.crops) {
    result[crop] = 0
  }
  // calculate required amounts based on product diffs
  for (const product of props.data.products) {
    const targetAmount = props.targets[product.name] ?? 0
    const currentAmount = props.current[product.name] ?? 0
    const diff = targetAmount - currentAmount
    if (diff > 0) {
      for (const ingredient of product.recipe) {
        result[ingredient.id] = (result[ingredient.id] || 0) + ingredient.amount * diff
      }
    }
  }
  return result
})
</script>

<style scoped>
/* Optional styling */
</style>
