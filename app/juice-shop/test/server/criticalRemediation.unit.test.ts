/*
 * Copyright (c) 2014-2026 Bjoern Kimminich & the OWASP Juice Shop contributors.
 * SPDX-License-Identifier: MIT
 */

import { describe, it } from 'node:test'
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import { createServer } from 'node:http'
import { once } from 'node:events'
import { mkdtempSync, readFileSync, existsSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { type AddressInfo } from 'node:net'
import { reviewsCollection } from '../../data/mongodb'
import * as security from '../../lib/insecurity'
import { downloadToFile } from '../../lib/utils'

void describe('critical dependency remediation', () => {
  void it('accepts a signed application token and rejects missing, malformed and unsigned tokens', () => {
    assert.equal(security.verify(security.authorize({ data: { id: 1 } })), true)
    assert.equal(security.verify(''), false)
    assert.equal(security.verify('not-a-token'), false)
    const header = Buffer.from(JSON.stringify({ alg: 'none', typ: 'JWT' })).toString('base64url')
    const payload = Buffer.from(JSON.stringify({ data: { id: 1 }, exp: 9999999999 })).toString('base64url')
    assert.equal(security.verify(`${header}.${payload}.`), false)
  })

  void it('rejects a token signed with the public key as an HMAC secret', () => {
    const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url')
    const payload = Buffer.from(JSON.stringify({ data: { id: 1 }, exp: 9999999999 })).toString('base64url')
    const body = `${header}.${payload}`
    const signature = crypto.createHmac('sha256', security.publicKey).update(body).digest('base64url')
    assert.equal(security.verify(`${body}.${signature}`), false)
    assert.equal(crypto.createPublicKey(security.publicKey).asymmetricKeyDetails?.modulusLength, 2048)
  })

  void it('preserves insertion, reads, counts and update result shapes', async () => {
    const inserted = await reviewsCollection.insert({ product: 91001, author: 'fixture', message: 'before', likesCount: 0, likedBy: [] })
    assert.equal(await reviewsCollection.count({ _id: inserted._id }), 1)
    const result = await reviewsCollection.update({ _id: inserted._id }, { $set: { message: 'after' }, $inc: { likesCount: 1 } })
    assert.equal(result.modified, 1)
    assert.equal(result.original[0].message, 'before')
    assert.equal(result.updated[0].message, 'after')
    assert.equal((await reviewsCollection.findOne({ _id: inserted._id })).likesCount, 1)
    assert.equal((await reviewsCollection.find({ product: 91001 })).length, 1)
  })

  void it('rejects executable selectors at every query entry point, including nested selectors', async () => {
    const query = { $where: 'globalThis.__criticalQueryExecuted = true; return true' }
    await assert.rejects(reviewsCollection.find(query), /Executable queries are disabled/)
    await assert.rejects(reviewsCollection.findOne(query), /Executable queries are disabled/)
    await assert.rejects(reviewsCollection.count(query), /Executable queries are disabled/)
    await assert.rejects(reviewsCollection.update(query, { $set: { message: 'unsafe' } }), /Executable queries are disabled/)
    await assert.rejects(reviewsCollection.find({ $or: [{ product: 91001 }, query] }), /Executable queries are disabled/)
    await assert.rejects(reviewsCollection.find({ $where: () => true }), /Executable queries are disabled/)
    assert.equal(Object.prototype.hasOwnProperty.call(globalThis, '__criticalQueryExecuted'), false)
  })

  void it('downloads bytes without archive extraction and refuses HTTP errors', async (t) => {
    const directory = mkdtempSync(join(tmpdir(), 'critical-download-'))
    const originalNoProxy = process.env.NO_PROXY
    process.env.NO_PROXY = '127.0.0.1'
    const bytes = Buffer.from([0x50, 0x4b, 0x03, 0x04, 0xff])
    const server = createServer((req, res) => {
      if (req.url === '/large') {
        res.end(Buffer.alloc(20 * 1024 * 1024 + 1))
        return
      }
      res.statusCode = req.url === '/ok' ? 200 : 404
      res.end(req.url === '/ok' ? bytes : 'not found')
    })
    t.after(() => {
      server.closeAllConnections()
      server.close()
      rmSync(directory, { recursive: true, force: true })
      if (originalNoProxy === undefined) delete process.env.NO_PROXY
      else process.env.NO_PROXY = originalNoProxy
    })
    server.listen(0, '127.0.0.1')
    await once(server, 'listening')
    const url = `http://127.0.0.1:${(server.address() as AddressInfo).port}`
    assert.equal(await downloadToFile(url + '/ok', join(directory, 'download.bin')), true)
    assert.deepEqual(readFileSync(join(directory, 'download.bin')), bytes)
    assert.equal(await downloadToFile(url + '/missing', join(directory, 'missing.bin')), false)
    assert.equal(existsSync(join(directory, 'missing.bin')), false)
    assert.equal(await downloadToFile(url + '/large', join(directory, 'large.bin')), false)
    assert.equal(existsSync(join(directory, 'large.bin')), false)
  })
})
