# coding: utf-8
# encoding: utf-8
from odoo import models, fields, api


class CollectionProduct(models.Model):
    _inherit = 'product.product'

    author_id = fields.Many2one('res.partner', string=u"Author")
    editor_id = fields.Many2one('res.partner', string=u"Editor")
    collection_id = fields.Many2one('collection.collection', string=u"Collection")
    ebook_file = fields.Binary(string=u"EBook File", attachment=True)
    summary = fields.Text(string=u"Summary")
    release_date = fields.Date(string=u"Release Date")

    _sql_constraints = [('barcode_uniq', 'unique (barcode)',
                         u"ISBN must be unique.")]
