import { defineStore } from "pinia";
import { ref } from "vue";

export const useUIStore = defineStore("ui", () => {
  const searchQuery = ref("");
  const mobileMenuOpen = ref(false);
  const isLoading = ref(false);

  function openMobileMenu() {
    mobileMenuOpen.value = true;
  }
  function closeMobileMenu() {
    mobileMenuOpen.value = false;
  }
  function toggleMobileMenu() {
    mobileMenuOpen.value = !mobileMenuOpen.value;
  }

  return { searchQuery, mobileMenuOpen, isLoading, openMobileMenu, closeMobileMenu, toggleMobileMenu };
});
