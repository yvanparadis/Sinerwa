import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", name: "Home", component: () => import("@/pages/Home.vue"), meta: { title: "Home" } },
  { path: "/movies", name: "Movies", component: () => import("@/pages/Movies.vue"), meta: { title: "Movies" } },
  { path: "/series", name: "Series", component: () => import("@/pages/Series.vue"), meta: { title: "Series" } },
  { path: "/series/:id", name: "SeriesDetails", component: () => import("@/pages/SeriesDetails.vue"), meta: { title: "Series Details" } },
  { path: "/movie/:id", name: "MovieDetails", component: () => import("@/pages/MovieDetails.vue"), meta: { title: "Movie Details" } },
  { path: "/watch/:id", name: "Watch", component: () => import("@/pages/Watch.vue"), meta: { title: "Watch" } },
  { path: "/my-list", name: "MyList", component: () => import("@/pages/MyList.vue"), meta: { title: "My List" } },
  { path: "/search", name: "Search", component: () => import("@/pages/Search.vue"), meta: { title: "Search" } },
  { path: "/about", name: "About", component: () => import("@/pages/About.vue"), meta: { title: "About" } },
  { path: "/login", name: "Login", component: () => import("@/pages/Login.vue"), meta: { title: "Sign In" } },
  { path: "/register", name: "Register", component: () => import("@/pages/Register.vue"), meta: { title: "Create Account" } },
  { path: "/providers", name: "Providers", component: () => import("@/pages/Providers.vue"), meta: { title: "Providers" } },
  { path: "/storage", name: "Storage", component: () => import("@/pages/StorageDashboard.vue"), meta: { title: "Storage" } },
  { path: "/:pathMatch(.*)*", name: "NotFound", component: () => import("@/pages/NotFound.vue"), meta: { title: "Not Found" } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

router.afterEach((to) => {
  if (to.meta?.title) {
    document.title = `CineRwa — ${to.meta.title}`;
  }
});

export default router;
