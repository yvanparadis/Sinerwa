<template>
  <div class="card" style="max-width:400px;margin:40px auto">
    <h2 style="margin-bottom:16px">Admin Sign In</h2>
    <form @submit.prevent="submit">
      <label>Username</label>
      <input v-model="username" required />
      <label style="margin-top:12px;display:block">Password</label>
      <input v-model="password" type="password" required />
      <p v-if="error" style="color:#E50914;margin-top:8px;font-size:14px">{{ error }}</p>
      <button class="btn" type="submit" style="margin-top:16px;width:100%" :disabled="loading">{{ loading ? 'Signing in…' : 'Sign In' }}</button>
    </form>
    <p style="margin-top:12px;font-size:12px;color:#888">Owner account only. No public registration.</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
const emit = defineEmits(["login"]);
const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);
const API = import.meta.env.VITE_API_BASE || "";

async function submit() {
  error.value = ""; loading.value = true;
  try {
    const form = new URLSearchParams();
    form.append("username", username.value);
    form.append("password", password.value);
    const res = await fetch(`${API}/api/v1/auth/login`, { method: "POST", body: form });
    if (!res.ok) { const d = await res.json(); throw new Error(d.detail || "Login failed"); }
    const data = await res.json();
    // verify admin
    const me = await fetch(`${API}/api/v1/auth/me`, { headers: { Authorization: `Bearer ${data.access_token}` } });
    const userData = await me.json();
    if (!userData.is_admin) throw new Error("Not an admin account");
    emit("login", data.access_token);
  } catch (e) { error.value = e.message; }
  finally { loading.value = false; }
}
</script>
