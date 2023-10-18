import { createApp } from 'vue';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import {createRouter} from 'vue-router';

import 'primevue/resources/themes/arya-orange/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';

import TabMenu from 'primevue/tabmenu';
import Menu from 'primevue/menu';
import Avatar from 'primevue/avatar';

import './assets/app.css';

import HomePage from './/components/HomePage.vue'
const routes = [
  { path: '/', component: HomePage }
]
const router = createRouter({
  routes
})

const app = createApp(App);
app.use(PrimeVue);
app.use(router);
app.component('TabMenu', TabMenu);
app.component('Menu', Menu);
app.component('Avatar', Avatar);
app.mount('#app');
