import '../public/assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import Markdown from 'vue3-markdown-it';
import router from './routes/index.js'


const app = createApp(App)
app.use(router)
app.use(Markdown)
// app.config.globalProperties.loginPwd = '123456'
// app.config.globalProperties.hasLogin = true
app.config.globalProperties.AIBody = {
    model: 'gpt-3.5-turbo',
    Temperatures: 0.8,
    Top_p: 1
}
app.mount('#app')

