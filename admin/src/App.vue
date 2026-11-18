<template>
  <div class="admin-shell">
    <header class="admin-header">
      <span class="brand">CineRwa Admin</span>
      <button v-if="token" class="btn" @click="logout">Sign out</button>
    </header>
    <main class="admin-main">
      <Login v-if="!token" @login="onLogin" />
      <Dashboard v-else :token="token" />
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Login from "./Login.vue";
import Dashboard from "./Dashboard.vue";
const token = ref(localStorage.getItem("admin_token") || "");
function onLogin(t) { token.value = t; localStorage.setItem("admin_token", t); }
function logout() { token.value = ""; localStorage.removeItem("admin_token"); }
</script>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, sans-serif; background: #0a0a0a; color: #fff; }
.admin-shell { min-height: 100vh; }
.admin-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 24px; background: #111; border-bottom: 1px solid #222; }
.brand { font-weight: 700; font-size: 18px; color: #E50914; }
.btn { background: #E50914; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; }
.admin-main { padding: 24px; max-width: 1200px; margin: 0 auto; }
.card { background: #161616; border: 1px solid #222; border-radius: 8px; padding: 16px; margin-bottom: 16px; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 8px; border-bottom: 1px solid #222; text-align: left; font-size: 14px; }
input { background: #222; border: 1px solid #333; color: #fff; padding: 8px; border-radius: 4px; width: 100%; }
</style>
