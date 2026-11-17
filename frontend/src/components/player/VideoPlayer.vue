<template>
  <div class="player" @mousemove="showControls" @mouseleave="hideControlsTimer">
    <video
      ref="videoRef"
      class="video"
      :poster="poster"
      @timeupdate="onTimeUpdate"
      @loadedmetadata="onLoaded"
      @waiting="loading = true"
      @playing="loading = false"
      @error="onError"
      @ended="playing = false"
      playsinline
    >
      <source v-if="src" :src="src" type="video/mp4" />
      <track v-if="subtitle" kind="subtitles" :src="subtitle" srclang="en" label="English" default />
    </video>

    <div v-if="loading" class="player-loading">
      <div class="spinner"></div>
      <span>Loading video…</span>
    </div>
    <div v-if="error" class="player-error">
      <p>{{ error }}</p>
      <button class="btn btn-primary" @click="retry">Retry</button>
    </div>

    <div class="controls" :class="{ visible: controlsVisible }">
      <div class="progress" @click="seek">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
      </div>
      <div class="control-row">
        <button class="ctrl-btn" @click="togglePlay" :aria-label="playing ? 'Pause' : 'Play'">
          <svg v-if="!playing" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>
        </button>
        <button class="ctrl-btn" @click="toggleMute" :aria-label="muted ? 'Unmute' : 'Mute'">
          <svg v-if="!muted" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 5L6 9H2v6h4l5 4V5zM19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 5L6 9H2v6h4l5 4V5zM23 9l-6 6M17 9l6 6"/></svg>
        </button>
        <input type="range" min="0" max="1" step="0.01" v-model.number="volume" @input="applyVolume" class="volume" />
        <span class="time">{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</span>
        <div class="spacer"></div>
        <button class="ctrl-btn" @click="toggleFullscreen" aria-label="Fullscreen">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from "vue";

const props = defineProps({
  src: { type: String, default: "" },
  poster: { type: String, default: "" },
  subtitle: { type: String, default: "" },
});
defineEmits(["error"]);

const videoRef = ref(null);
const playing = ref(false);
const muted = ref(false);
const volume = ref(1);
const currentTime = ref(0);
const duration = ref(0);
const progress = ref(0);
const loading = ref(false);
const error = ref("");
const controlsVisible = ref(true);

let hideTimer = null;

function togglePlay() {
  const v = videoRef.value;
  if (!v) return;
  if (v.paused) {
    v.play().catch(() => {});
    playing.value = true;
  } else {
    v.pause();
    playing.value = false;
  }
}
function toggleMute() {
  const v = videoRef.value;
  if (!v) return;
  v.muted = !v.muted;
  muted.value = v.muted;
}
function applyVolume() {
  const v = videoRef.value;
  if (v) v.volume = volume.value;
}
function seek(e) {
  const v = videoRef.value;
  if (!v || !duration.value) return;
  const rect = e.currentTarget.getBoundingClientRect();
  const ratio = (e.clientX - rect.left) / rect.width;
  v.currentTime = ratio * duration.value;
}
function onTimeUpdate() {
  const v = videoRef.value;
  if (!v) return;
  currentTime.value = v.currentTime;
  duration.value = v.duration || 0;
  progress.value = duration.value ? (currentTime.value / duration.value) * 100 : 0;
}
function onLoaded() {
  const v = videoRef.value;
  if (v) duration.value = v.duration || 0;
  loading.value = false;
}
function onError() {
  loading.value = false;
  error.value = "Unable to load this video. The source may be unavailable.";
}
function retry() {
  error.value = "";
  const v = videoRef.value;
  if (v) {
    v.load();
    v.play().catch(() => {});
  }
}
function formatTime(t) {
  if (!t || isNaN(t)) return "0:00";
  const m = Math.floor(t / 60);
  const s = Math.floor(t % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}
function toggleFullscreen() {
  const el = videoRef.value?.parentElement;
  if (!el) return;
  if (document.fullscreenElement) document.exitFullscreen();
  else el.requestFullscreen?.();
}
function showControls() {
  controlsVisible.value = true;
  clearTimeout(hideTimer);
  hideTimer = setTimeout(() => {
    if (playing.value) controlsVisible.value = false;
  }, 3000);
}
function hideControlsTimer() {
  hideTimer = setTimeout(() => {
    if (playing.value) controlsVisible.value = false;
  }, 1500);
}

onMounted(() => {
  showControls();
});
onBeforeUnmount(() => {
  clearTimeout(hideTimer);
});
</script>

<style scoped>
.player {
  position: relative;
  width: 100%;
  background: #000;
  border-radius: var(--radius-lg);
  overflow: hidden;
  aspect-ratio: 16 / 9;
}
.video {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #000;
}
.player-loading,
.player-error {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  background: rgba(0,0,0,0.6);
  color: var(--color-white);
  z-index: 5;
}
.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid rgba(255,255,255,0.2);
  border-top-color: var(--color-primary-purple);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.controls {
  position: absolute;
  left: 0; right: 0; bottom: 0;
  padding: var(--space-3) var(--space-4);
  background: linear-gradient(to top, rgba(0,0,0,0.85), transparent);
  opacity: 0;
  transition: opacity var(--transition-base);
  z-index: 6;
}
.controls.visible { opacity: 1; }
.progress {
  height: 4px;
  background: rgba(255,255,255,0.2);
  border-radius: 2px;
  cursor: pointer;
  margin-bottom: var(--space-3);
}
.progress-bar {
  height: 100%;
  background: var(--color-primary-purple);
  border-radius: 2px;
}
.control-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}
.ctrl-btn {
  background: none;
  border: none;
  color: #fff;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
}
.volume {
  width: 80px;
}
.time {
  font-size: var(--text-xs);
  color: var(--color-secondary-text);
}
.spacer { flex: 1; }
</style>
