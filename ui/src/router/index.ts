import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/",
      name: "home",
      component: () => import("../views/HomeView.vue"),
    },
    {
      path: "/apache",
      name: "apache",
      component: () => import("../views/ApacheView.vue"),
    },
  ],
});

export default router;

router.beforeEach(async (to: any) => {
  const publicPages = ["login"];
  const authRequired = !publicPages.includes(to.name);
  const auth: any = useAuthStore();

  if (authRequired && !auth.isAuthenticated()) {
    return "/login";
  }
});
