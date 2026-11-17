<template>
  <div class="app-shell">
    <div class="route-progress" :class="{ active: routeLoading }"></div>
    <NavBar />
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <Footer />
    <MobileMenu v-if="ui.mobileMenuOpen" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useUIStore } from "@/stores/ui";
import NavBar from "@/components/navigation/NavBar.vue";
import Footer from "@/components/navigation/Footer.vue";
import MobileMenu from "@/components/navigation/MobileMenu.vue";

const ui = useUIStore();
const router = useRouter();
const routeLoading = ref(false);

router.beforeEach(() => { routeLoading.value = true; });
router.afterEach(() => { setTimeout(() => { routeLoading.value = false; }, 200); });
</script>

<style>
.route-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  width: 0;
  background: var(--color-primary-purple);
  z-index: 9999;
  transition: width 0.2s ease;
  box-shadow: 0 0 8px var(--color-primary-purple);
}
.route-progress.active {
  width: 80%;
  transition: width 0.8s ease;
}
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.app-main {
  flex: 1;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
