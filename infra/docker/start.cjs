'use strict'
const fs = require('node:fs')
const path = require('node:path')

// Seed only declared ephemeral writable directories. Application code stays read-only.
for (const name of ['data', 'ftp', 'i18n', 'uploads', 'frontend/dist', '.well-known']) {
  const destination = path.join('/juice-shop', name)
  const marker = path.join(destination, '.pipelinefortress-seeded')
  if (!fs.existsSync(marker)) {
    fs.cpSync(path.join('/opt/juice-shop-seed', name), destination, {
      recursive: true, force: false, errorOnExist: false
    })
    fs.writeFileSync(marker, 'seeded\n', { flag: 'wx' })
  }
}
require('/juice-shop/build/app.js')
