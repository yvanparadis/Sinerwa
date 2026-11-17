export function setSeo({ title, description, canonical, ogTitle, ogDescription, ogImage, jsonLd }) {
  if (title) document.title = title;
  const setMeta = (name, content, attr = "name") => {
    if (!content) return;
    let el = document.querySelector(`meta[${attr}="${name}"]`);
    if (!el) {
      el = document.createElement("meta");
      el.setAttribute(attr, name);
      document.head.appendChild(el);
    }
    el.setAttribute("content", content);
  };
  setMeta("description", description);
  setMeta("og:title", ogTitle || title, "property");
  setMeta("og:description", ogDescription || description, "property");
  setMeta("og:image", ogImage, "property");
  setMeta("og:type", "video.movie", "property");
  // canonical
  if (canonical) {
    let link = document.querySelector('link[rel="canonical"]');
    if (!link) {
      link = document.createElement("link");
      link.setAttribute("rel", "canonical");
      document.head.appendChild(link);
    }
    link.setAttribute("href", canonical);
  }
  // JSON-LD
  const existing = document.querySelector('script[type="application/ld+json"]');
  if (existing) existing.remove();
  if (jsonLd) {
    const script = document.createElement("script");
    script.type = "application/ld+json";
    script.textContent = JSON.stringify(jsonLd);
    document.head.appendChild(script);
  }
}
