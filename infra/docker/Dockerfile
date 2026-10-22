FROM node:24@sha256:14078204b6bb268c107ceff6d3c43f45a888105e5c2b18b14c32b3409d93a1b0 AS builder
WORKDIR /juice-shop
ENV CYPRESS_INSTALL_BINARY=0 NG_BUILD_MAX_WORKERS=2 NODE_OPTIONS=--max-old-space-size=4096
COPY app/ ./
# Both locks are supplied from the retained project locks in a clean context.
# Disable the upstream postinstall's unlocked frontend install and build explicitly.
RUN npm ci --ignore-scripts --no-audit --no-fund \
    && npm rebuild sqlite3 \
    && cd frontend && npm ci --ignore-scripts --no-audit --no-fund
RUN npm run build
RUN npm prune --omit=dev --ignore-scripts --no-audit --no-fund \
    && mkdir -p /runtime/frontend/src /seed/frontend \
    && cp -a build config encryptionkeys infrastructure lib models routes views \
        server.ts swagger.yml ctf.key package.json package-lock.json LICENSE /runtime/ \
    && cp -a frontend/src/app /runtime/frontend/src/ \
    && cp -a node_modules /runtime/ \
    && cp -a data ftp i18n uploads .well-known /seed/ \
    && cp -a frontend/dist /seed/frontend/ \
    && mkdir -p /runtime/data /runtime/ftp /runtime/i18n /runtime/uploads /runtime/logs /runtime/frontend/dist /runtime/.well-known \
    && chmod -R a+rX /runtime /seed

FROM gcr.io/distroless/nodejs24-debian13:nonroot@sha256:78f07ef1b5ea71ad7c055df15d0dd8997f2d288f9158623c4d4ae3d765b7d50d
LABEL org.opencontainers.image.title="PipelineFortress Juice Shop lab" \
    org.opencontainers.image.source="https://github.com/juice-shop/juice-shop" \
    org.opencontainers.image.revision="f189f521266f42c6bd05884468292000cee852ed" \
    org.opencontainers.image.licenses="MIT"
ENV NODE_ENV=production
WORKDIR /juice-shop
COPY --from=builder --chown=0:0 /runtime/ ./
COPY --from=builder --chown=0:0 /seed/ /opt/juice-shop-seed/
COPY --chown=0:0 start.cjs /opt/pipelinefortress/start.cjs
USER 65532:65532
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD ["/nodejs/bin/node", "-e", "fetch('http://127.0.0.1:3000/').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]
CMD ["/opt/pipelinefortress/start.cjs"]
