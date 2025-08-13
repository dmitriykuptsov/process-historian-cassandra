import { createApp } from "vue";
import App from "./App.vue";
import "bootstrap/dist/css/bootstrap.min.css";
import "@/assets/css/main.css";
import router from "./router";

const app = createApp(App);
app.config.globalProperties["$BASE_URL"] = "https://process-historian.strangebit.io";
//app.config.globalProperties["$BASE_URL"] = "http://192.168.1.244:5006";
app.use(router);
app.mount("#app");
