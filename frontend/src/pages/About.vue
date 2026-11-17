<template>
  <div class="page">
    <div class="container about">
      <header class="about-hero">
        <img src="/logo-primary.svg" alt="CineRwa" height="48" />
        <h1>About CineRwa</h1>
        <p class="tagline">Your World of Cinema.</p>
      </header>

      <section class="about-section">
        <h2>Our Story</h2>
        <p>
          CineRwa is a Rwanda-inspired cinema and entertainment platform designed for an international audience.
          Born from a love of storytelling and a belief that African voices deserve a global stage, CineRwa brings
          together Rwandan cinema, African stories, and world entertainment in one premium experience.
        </p>
      </section>

      <section class="about-section">
        <h2>Mission</h2>
        <p>
          To celebrate creativity, make entertainment accessible, and connect audiences worldwide with stories rooted in
          Rwanda and Africa while opening doors to international cinema.
        </p>
      </section>

      <section class="about-section">
        <h2>Brand Identity</h2>
        <p>
          Our logo combines a simplified film reel, a subtle play button, and a circular geometric structure —
          representing cinema, storytelling, and modern African entertainment. Purple is our primary brand accent,
          evoking creativity and cinematic quality.
        </p>
        <div class="logo-grid">
          <div class="logo-card"><img src="/logo-primary.svg" alt="Primary logo" /><span>Primary</span></div>
          <div class="logo-card"><img src="/logo-icon.svg" alt="Icon" /><span>Icon</span></div>
          <div class="logo-card"><img src="/logo-compact.svg" alt="Compact" /><span>Compact</span></div>
          <div class="logo-card dark"><img src="/logo-dark.svg" alt="Dark" /><span>Dark bg</span></div>
          <div class="logo-card light"><img src="/logo-light.svg" alt="Light" /><span>Light bg</span></div>
        </div>
      </section>

      <section class="about-section">
        <h2>Content & Ethics</h2>
        <p>
          CineRwa respects creators and rights holders. We only integrate content through official APIs, authorized
          embedding, legitimate links, and licensed sources. We do not scrape, download, redistribute, or embed
          copyrighted content without permission.
        </p>
      </section>

      <section class="about-section">
        <h2>Credits & Attribution</h2>
        <p>
          Movie metadata is provided by TMDB, subject to its licensing and attribution requirements.
          Images and artwork are provided by authorized metadata sources. This is Phase 02 of a larger project.
        </p>
      </section>

      <section class="about-section">
        <h2>Contact</h2>
        <p>Email: hello@cinerwa.com (placeholder)</p>
        <p>Location: Kigali, Rwanda</p>
      </section>
    </div>
  </div>
</template>

<style scoped>
.page { padding: var(--space-8) 0; }
.about { max-width: 900px; }
.about-hero { text-align: center; margin-bottom: var(--space-10); }
.about-hero h1 { font-size: var(--text-4xl); font-weight: var(--font-weight-extrabold); margin: var(--space-4) 0 var(--space-2); }
.tagline { color: var(--color-lavender); font-size: var(--text-lg); margin: 0; }
.about-section { margin-bottom: var(--space-8); }
.about-section h2 { font-size: var(--text-2xl); margin: 0 0 var(--space-3); color: var(--color-lavender); }
.about-section p { color: var(--color-secondary-text); line-height: 1.7; }
.logo-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: var(--space-4); margin-top: var(--space-4); }
.logo-card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-4); display: flex; flex-direction: column; align-items: center; gap: var(--space-2); }
.logo-card img { max-width: 100%; height: 40px; }
.logo-card span { font-size: var(--text-xs); color: var(--color-secondary-text); }
.logo-card.dark { background: var(--color-midnight); }
.logo-card.light { background: #f4f1fa; }
</style>
