<template>
  <v-container>
    <v-simple-table>
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
            <v-text-field
              v-model.number="amounts[crop]"
              type="number"
              min="0"
              dense
              hide-details
              style="max-width: 80px"
            />
          </td>
        </tr>
      </tbody>
    </v-simple-table>
  </v-container>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'

// Props: list of crop names
const props = defineProps<{ crops: string[] }>()

// Reactive map of crop name -> amount
const amounts = reactive<Record<string, number>>({})
// Initialize all amounts to zero
props.crops.forEach(crop => {
  amounts[crop] = 0
})

// Sorted list of crops
const sortedCrops = computed(() => {
  return [...props.crops].sort((a, b) => a.localeCompare(b))
})
</script>

<style scoped>
/* Optional styling */
</style>
