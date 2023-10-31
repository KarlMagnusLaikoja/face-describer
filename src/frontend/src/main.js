import { createApp } from 'vue';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import {createRouter} from 'vue-router';
import {createWebHistory} from 'vue-router';
import Vuex from 'vuex';


import 'primevue/resources/themes/arya-orange/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';

import TabMenu from 'primevue/tabmenu';
import Menu from 'primevue/menu';
import Avatar from 'primevue/avatar';
import FileUpload from 'primevue/fileupload';
import Message from 'primevue/message';
import Image from 'primevue/image';
import Panel from 'primevue/panel';
import Divider from 'primevue/divider';
import Tree from 'primevue/tree';

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

const store = new Vuex.Store({
    state: {
        languageCode: 'EN',
    },
    mutations: {
        setLanguageCode: (state, languageCode) => state.languageCode = languageCode
    },
    actions: {
        updateLanguageCode(context, languageCode) { context.commit('setLanguageCode', languageCode) }
    }
});

const app = createApp(App);
app.use(PrimeVue);
app.use(router);
app.use(Vuex);
app.use(store);
app.component('TabMenu', TabMenu);
app.component('Menu', Menu);
app.component('Avatar', Avatar);
app.component('FileUpload', FileUpload);
app.component('Message', Message);
app.component('Image', Image);
app.component('Panel', Panel);
app.component('Divider', Divider);
app.component('Tree', Tree);

app.mount('#app');
