// Content provider adapter interface and registry.
// Each provider implements this contract. Do not hardcode provider logic in components.

export const PROVIDER_STATUS = {
  AVAILABLE: "available",
  UNAVAILABLE: "unavailable",
  MAINTENANCE: "maintenance",
  PENDING_AUTHORIZATION: "pending_authorization",
};

export class ContentProviderAdapter {
  constructor(meta) {
    this.id = meta.id;
    this.name = meta.name;
    this.description = meta.description || "";
    this.status = meta.status || PROVIDER_STATUS.UNAVAILABLE;
    this.supports = meta.supports || [];
  }

  async getMetadata(contentId) {
    throw new Error(`${this.name}: getMetadata not implemented`);
  }

  async getWatchLink(contentId) {
    throw new Error(`${this.name}: getWatchLink not implemented`);
  }

  async getAvailability(contentId) {
    throw new Error(`${this.name}: getAvailability not implemented`);
  }

  getStatus() {
    return this.status;
  }
}

const providers = new Map();

export const providerRegistry = {
  register(provider) {
    providers.set(provider.id, provider);
  },
  get(id) {
    return providers.get(id) || null;
  },
  list() {
    return Array.from(providers.values());
  },
  async getWatchLink(providerId, contentId) {
    const p = providers.get(providerId);
    if (!p) throw new Error(`Unknown provider: ${providerId}`);
    return p.getWatchLink(contentId);
  },
};

export default providerRegistry;
