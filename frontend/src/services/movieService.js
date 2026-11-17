const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

async function tryBackend(path) {
  try {
    const res = await fetch(`${API_BASE}${path}`);
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

export const movieService = {
  async getFeatured() {
    const data = await tryBackend("/api/v1/movies");
    return (data && data.items && data.items.length) ? data.items[0] : null;
  },
  async getTrending() {
    const data = await tryBackend("/api/v1/movies");
    return (data && data.items && data.items.length) ? data.items.slice(0, 8) : [];
  },
  async getPopular() {
    const data = await tryBackend("/api/v1/movies");
    if (data && data.items && data.items.length) {
      return [...data.items].sort((a, b) => (b.rating || 0) - (a.rating || 0)).slice(0, 8);
    }
    return [];
  },
  async getRecentlyAdded() {
    const data = await tryBackend("/api/v1/movies");
    return (data && data.items && data.items.length) ? data.items.slice(-6) : [];
  },
  async getAfricanCinema() {
    return [];
  },
  async getRwandanCinema() {
    return [];
  },
  async getRecommended() {
    const data = await tryBackend("/api/v1/movies");
    return (data && data.items && data.items.length) ? data.items.slice(2, 10) : [];
  },
  async getAllMovies() {
    const data = await tryBackend("/api/v1/movies");
    return (data && data.items) ? data.items : [];
  },
  async getMovieById(id) {
    const data = await tryBackend(`/api/v1/movies/${id}`);
    return (data && data.id) ? data : null;
  },
  async getGenres() {
    const data = await tryBackend("/api/v1/tmdb/genres");
    if (data && data.genres) {
      return data.genres.map((g) => ({ id: g.id, name: g.name }));
    }
    return [];
  },
};

export const seriesService = {
  async getAllSeries() {
    return [];
  },
  async getSeriesById() {
    return null;
  },
};

export const searchService = {
  async search(query) {
    const q = (query || "").trim();
    if (!q) return [];
    const data = await tryBackend(`/api/v1/search?q=${encodeURIComponent(q)}`);
    if (data && data.results) return data.results;
    const all = await movieService.getAllMovies();
    const ql = q.toLowerCase();
    return all.filter((m) =>
      (m.title || "").toLowerCase().includes(ql) ||
      (m.overview || "").toLowerCase().includes(ql)
    );
  },
  async suggestions(query) {
    const q = (query || "").trim();
    if (q.length < 2) return [];
    const data = await tryBackend(`/api/v1/search?q=${encodeURIComponent(q)}&limit=6`);
    if (data && data.results) return data.results.map((m) => m.title);
    return [];
  },
};

export default { movieService, seriesService, searchService };
