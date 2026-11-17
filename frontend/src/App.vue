<template>
  <div class="app-shell">
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
import { useUIStore } from "@/stores/ui";
import NavBar from "@/components/navigation/NavBar.vue";
import Footer from "@/components/navigation/Footer.vue";
import MobileMenu from "@/components/navigation/MobileMenu.vue";

const ui = useUIStore();
</script>

<style>
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
