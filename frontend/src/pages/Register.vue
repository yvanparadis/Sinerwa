<template>
  <div class="page">
    <div class="container auth-wrap">
      <div class="auth-card">
        <h1>Create Account</h1>
        <p class="sub">Join CineRwa.</p>
        <form @submit.prevent="submit">
          <label>Email</label>
          <input v-model="email" type="email" class="input" required />
          <label>Username</label>
          <input v-model="username" class="input" required />
          <label>Password</label>
          <input v-model="password" type="password" class="input" required />
          <p v-if="error" class="err">{{ error }}</p>
          <button class="btn btn-primary block" type="submit" :disabled="loading">{{ loading ? 'Creating…' : 'Create Account' }}</button>
        </form>
        <p class="switch">Already have an account? <router-link to="/login">Sign in</router-link></p>
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
const email = ref("");
const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    await auth.register(email.value, username.value, password.value);
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
