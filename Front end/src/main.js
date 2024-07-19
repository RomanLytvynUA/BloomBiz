import 'bootstrap/dist/css/bootstrap.css';

import $ from 'jquery';
window.$ = window.jQuery = $;

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';

import router from './router';

import { createI18n } from 'vue-i18n'
import eng from './locales/eng.json'
import ukr from './locales/ukr.json'

const i18n = createI18n({
    locale: 'eng',
    legacy: false,
    messages: {
        ukr: ukr,
        eng: eng,
    },
})

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(i18n);

app.mount('#app');
