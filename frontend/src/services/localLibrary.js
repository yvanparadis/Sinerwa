const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export const localLibraryService = {
  async list() {
    const res = await fetch(`${API_BASE}/api/v1/local/library`);
    if (!res.ok) throw new Error("Failed to load local library");
    const data = await res.json();
    return data.items || [];
  },
  streamUrl(item) {
    return `${API_BASE}${item.url}`;
  },
  subtitleUrl(item) {
    return item.subtitleUrl ? `${API_BASE}${item.subtitleUrl}` : null;
  },
};

export default localLibraryService;
