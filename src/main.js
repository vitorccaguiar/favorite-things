import Vue from 'vue'
import Vuetify from 'vuetify'
import App from '@/App.vue'

import router from '@/router'

import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.use(Vuetify, {
  iconfont: 'md'
})

Vue.config.productionTip = false

const vue = new Vue({
  router,
  render: h => h(App)
})

vue.$mount('#app')
