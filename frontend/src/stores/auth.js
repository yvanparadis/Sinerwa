import { defineStore } from "pinia";
import { ref, computed } from "vue";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
const TOKEN_KEY = "cinerwa_token";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || "");
  const user = ref(null);

  const isAuthenticated = computed(() => !!token.value);
  const isAdmin = computed(() => !!(user.value && user.value.is_admin));

  async function register(email, username, password) {
    const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, username, password }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Registration failed");
    }
    const data = await res.json();
    token.value = data.access_token;
    localStorage.setItem(TOKEN_KEY, token.value);
    await fetchMe();
  }

  async function login(username, password) {
    const form = new URLSearchParams();
    form.append("username", username);
    form.append("password", password);
    const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Login failed");
    }
    const data = await res.json();
    token.value = data.access_token;
    localStorage.setItem(TOKEN_KEY, token.value);
    await fetchMe();
  }

  async function fetchMe() {
    if (!token.value) { user.value = null; return; }
    try {
      const res = await fetch(`${API_BASE}/api/v1/auth/me`, {
        headers: { Authorization: `Bearer ${token.value}` },
      });
      if (!res.ok) throw new Error("unauth");
      user.value = await res.json();
    } catch {
      token.value = "";
      user.value = null;
      localStorage.removeItem(TOKEN_KEY);
    }
  }

  function logout() {
    token.value = "";
    user.value = null;
    localStorage.removeItem(TOKEN_KEY);
  }

  // init
  if (token.value) fetchMe();

  return { token, user, isAuthenticated, isAdmin, register, login, logout, fetchMe };
});
