<template>
  <v-container>
    <v-table>
      <thead>
        <tr>
          <th class="text-left">Crop</th>
          <th class="text-left">Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="crop in sortedCrops" :key="crop">
          <td>{{ crop }}</td>
          <td>
            <b>{{ amounts[crop] }}</b>
          </td>
        </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import type {Data} from "@/interfaces/data.ts";

// Props: list of crop names
const props = defineProps<{
  data: Data,
  current: Record<string, number>
  targets: Record<string, number>
}>()

// Reactive map of crop name -> amount
const amounts = reactive<Record<string, number>>({})
// Initialize all amounts to zero
props.data.crops.forEach(crop => {
  amounts[crop] = 0
})

// Sorted list of crops
const sortedCrops = computed(() => {
  return [...props.data.crops].sort((a, b) => a.localeCompare(b))
})
</script>

<style scoped>
/* Optional styling */
</style>
