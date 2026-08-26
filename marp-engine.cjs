const { Marp } = require("@marp-team/marp-core");
const kroki = require("@kazumatu981/markdown-it-kroki");

// Em desenvolvimento local (fora de container) usa a instância pública.
// Dentro do compose, KROKI_ENTRYPOINT aponta para o serviço "kroki" na rede interna.
const KROKI_ENTRYPOINT = process.env.KROKI_ENTRYPOINT || "https://kroki.io";

module.exports = class CustomEngine extends Marp {
  constructor(opts) {
    super({ ...opts, html: true });

    this.use(kroki, {
      entrypoint: KROKI_ENTRYPOINT,
      containerClass: "kroki-diagram",
      useImg: true,
    });
  }
};
