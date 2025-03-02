import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { clickOutside } from './directives/clickOutside'

const app = createApp(App)

app.use(createPinia())
app.directive('click-outside', clickOutside)

app.mount('#app')
