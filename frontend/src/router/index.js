import { createRouter, createWebHistory } from "vue-router";
import Sensors from "../views/Sensors.vue";
import Data from "../views/Data.vue";

const routes = [
  {
    path: "/",
    name: "Sensors",
    component: Sensors,
  },
  {
    path: "/sensors",
    name: "Sensors",
    component: Sensors,
  },
  {
    path: "/data",
    name: "Data",
    component: Data,
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.replace({ path: "*", redirect: "/" });

export default router;
