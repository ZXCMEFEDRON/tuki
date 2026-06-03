import { createApp } from 'vue'
import { createPinia } from 'pinia'
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap/dist/js/bootstrap"
import * as bootstrap from 'bootstrap'

import App from './App.vue'
import router from './router'

window.bootstrap = bootstrap

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')