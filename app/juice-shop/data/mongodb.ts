/*
 * Copyright (c) 2014-2026 Bjoern Kimminich & the OWASP Juice Shop contributors.
 * SPDX-License-Identifier: MIT
 */

import Datastore from '@seald-io/nedb'

type Document = Record<string, any>

function validateQuery (value: unknown): void {
  if (typeof value === 'function') throw new Error('Executable queries are disabled')
  if (value !== null && typeof value === 'object') {
    for (const [key, child] of Object.entries(value)) {
      if (key === '$where' || key === '$function' || key === '__proto__' || key === 'constructor' || key === 'prototype') {
        throw new Error('Executable queries are disabled')
      }
      validateQuery(child)
    }
  }
}

class Collection {
  private readonly store = new Datastore<Document>({ inMemoryOnly: true })
  private readonly insertionOrder = new Map<string, number>()

  async insert (document: Document) {
    const inserted = await this.store.insertAsync(document)
    this.insertionOrder.set(inserted._id, this.insertionOrder.size)
    return inserted
  }

  async find (query: Document = {}): Promise<any[]> {
    validateQuery(query)
    const documents = await this.store.findAsync(query)
    return documents.sort((a, b) => (this.insertionOrder.get(a._id) ?? 0) - (this.insertionOrder.get(b._id) ?? 0))
  }

  async findOne (query: Document): Promise<any> {
    validateQuery(query)
    return (await this.find(query))[0]
  }

  async count (query: Document = {}): Promise<number> {
    validateQuery(query)
    return await this.store.countAsync(query)
  }

  async update (query: Document, changes: Document, options: { multi?: boolean } = {}): Promise<{ modified: number, original: any[], updated: any[] }> {
    validateQuery(query)
    validateQuery(changes)
    const matches = await this.find(query)
    const original = options.multi ? matches : matches.slice(0, 1)
    const result = await this.store.updateAsync(query, changes, { multi: options.multi ?? false, returnUpdatedDocs: true })
    const updated = result.affectedDocuments === null ? [] : Array.isArray(result.affectedDocuments) ? result.affectedDocuments : [result.affectedDocuments]
    return { modified: result.numAffected, original, updated }
  }
}

export const reviewsCollection = new Collection()
export const ordersCollection = new Collection()
