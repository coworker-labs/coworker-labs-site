// Cloudflare Pages worker placeholder
export default {
  async fetch(request, env) {
    return env.ASSETS.fetch(request);
  }
};
