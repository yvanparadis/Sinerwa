<template>
  <div>
    <h2 style="margin-bottom:16px">Overview</h2>
    <div class="card" v-if="overview">
      <div>Total movies: {{ overview.total_movies }}</div>
      <div>Total genres: {{ overview.total_genres }}</div>
      <div>Missing description: {{ overview.movies_missing_description }}</div>
      <div>Missing poster: {{ overview.movies_missing_poster }}</div>
      <div>Without trailer: {{ overview.movies_without_trailer }}</div>
    </div>
    <h3 style="margin:16px 0 8px">Recent movies</h3>
    <div class="card">
      <table>
        <thead><tr><th>Title</th><th>Created</th></tr></thead>
        <tbody>
          <tr v-for="m in (overview?.recent_movies || [])" :key="m.id">
            <td>{{ m.title }}</td>
            <td>{{ m.createdAt }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <h3 style="margin:16px 0 8px">Movie management</h3>
    <div class="card">
      <input v-model="q" placeholder="Search movies..." @input="loadMovies" />
      <table style="margin-top:12px">
        <thead><tr><th>Title</th><th>Genres</th><th>Playback</th><th>Actions</th></tr></thead>
        <tbody>
          <tr v-for="m in movies" :key="m.id">
            <td>{{ m.title }}</td>
            <td>{{ (m.genres||[]).join(', ') }}</td>
            <td>{{ m.playbackType }}</td>
            <td><button class="btn" style="padding:4px 8px;font-size:12px" @click="del(m.id)">Delete</button></td>
          </tr>
        </tbody>
      </table>
      <p style="margin-top:8px;font-size:12px;color:#888">Total: {{ total }}</p>
    </div>
    <h3 style="margin:16px 0 8px">Audit log</h3>
    <div class="card">
      <table>
        <thead><tr><th>Action</th><th>Details</th><th>When</th></tr></thead>
        <tbody>
          <tr v-for="a in audit" :key="a.id">
            <td>{{ a.action }}</td>
            <td>{{ a.details }}</td>
            <td>{{ a.created_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
const props = defineProps({ token: String });
const API = import.meta.env.VITE_API_BASE || "";
const overview = ref(null);
const movies = ref([]);
const total = ref(0);
const audit = ref([]);
const q = ref("");

async function authFetch(path, opts = {}) {
  return fetch(`${API}${path}`, { ...opts, headers: { ...(opts.headers||{}), Authorization: `Bearer ${props.token}` } });
}

async function load() {
  const r = await authFetch("/api/v1/admin/overview");
  if (r.ok) overview.value = await r.json();
  const a = await authFetch("/api/v1/admin/audit-log");
  if (a.ok) { const d = await a.json(); audit.value = d.items || []; }
  await loadMovies();
}
async function loadMovies() {
  const r = await authFetch(`/api/v1/admin/movies?q=${encodeURIComponent(q.value)}&limit=50`);
  if (r.ok) { const d = await r.json(); movies.value = d.items || []; total.value = d.total || 0; }
}
async function del(id) {
  if (!confirm("Delete this movie?")) return;
  await authFetch(`/api/v1/admin/movies/${id}`, { method: "DELETE" });
  await loadMovies();
}
onMounted(load);
</script>
