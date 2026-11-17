<template>
  <div class="page">
    <div class="container auth-wrap">
      <div class="auth-card">
        <h1>Sign In</h1>
        <p class="sub">Welcome back to CineRwa.</p>
        <form @submit.prevent="submit">
          <label>Username</label>
          <input v-model="username" class="input" required />
          <label>Password</label>
          <input v-model="password" type="password" class="input" required />
          <p v-if="error" class="err">{{ error }}</p>
          <button class="btn btn-primary block" type="submit" :disabled="loading">{{ loading ? 'Signing in…' : 'Sign In' }}</button>
        </form>
        <p class="switch">No account? <router-link to="/register">Create one</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
const router = useRouter();
const auth = useAuthStore();
const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    await auth.login(username.value, password.value);
    router.push("/");
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.page { padding: var(--space-10) 0; }
.auth-wrap { display: flex; justify-content: center; }
.auth-card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-8); width: 100%; max-width: 420px; }
.auth-card h1 { margin: 0 0 var(--space-1); }
.sub { color: var(--color-secondary-text); margin: 0 0 var(--space-6); }
label { display: block; font-size: var(--text-sm); color: var(--color-secondary-text); margin: var(--space-3) 0 var(--space-1); }
.err { color: var(--color-danger); font-size: var(--text-sm); margin: var(--space-2) 0; }
.block { width: 100%; margin-top: var(--space-4); }
.switch { margin-top: var(--space-4); font-size: var(--text-sm); color: var(--color-secondary-text); text-align: center; }
.switch a { color: var(--color-lavender); }
</style>
