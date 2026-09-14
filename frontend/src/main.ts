import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import Vue3Toastify from "vue3-toastify";
import "vue3-toastify/dist/index.css";

import App from "./App.vue";
import router from "./router";
import GoogleLogin from "vue3-google-login";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(GoogleLogin, { clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID });
app.use(Vue3Toastify, { autoClose: 3000 });

app.mount("#app");
