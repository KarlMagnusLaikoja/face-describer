import { createApp } from 'vue';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import {createRouter} from 'vue-router';
import {createWebHistory} from 'vue-router';

import 'primevue/resources/themes/arya-orange/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';

import TabMenu from 'primevue/tabmenu';
import Menu from 'primevue/menu';
import Avatar from 'primevue/avatar';

import './assets/app.css';

import HomePage from './/components/HomePage.vue'
import FaceDescriber from './/components/FaceDescriber.vue'
import Contact from './/components/Contact.vue'
import Gallery from './/components/Gallery.vue'
const routes = [
  { path: '/', component: HomePage },
  { path: '/face-describer', component: FaceDescriber },
  { path: '/contact', component: Contact },
  { path: '/gallery', component: Gallery }
]
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

const app = createApp(App);
app.use(PrimeVue);
app.use(router);
app.component('TabMenu', TabMenu);
app.component('Menu', Menu);
app.component('Avatar', Avatar);
app.mount('#app');
