import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const app = createApp(App)

// 1) Fetch the JSON from public/.
const res = await fetch('/data.json')
const data = await res.json()  // combined: { items: string[], products: Product[] }

// 2) Provide it to the app
app.provide('data', data)

app.use(createPinia())

app.mount('#app')
