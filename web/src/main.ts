/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Styles
import 'unfonts.css'

const app = createApp(App)

registerPlugins(app)

// 1) Fetch the JSON from public/.
const res = await fetch('/data.json')
const data = await res.json()  // combined: { items: string[], products: Product[] }

// 2) Provide it to the app
app.provide('data', data)

app.mount('#app')
