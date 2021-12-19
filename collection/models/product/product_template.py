# coding: utf-8
# encoding: utf-8
from odoo import models, fields, api


class CollectionProduct(models.Model):
    _inherit = 'product.template'

    author_id = fields.Many2one('res.partner', string=u"Author")
    editor_id = fields.Many2one('res.partner', string=u"Editor")
    collection_id = fields.Many2one('collection.collection', string=u"Collection")
    ebook_file = fields.Binary(string=u"EBook File", attachment=True)
    summary = fields.Text(string=u"Summary")
    release_date = fields.Date(string=u"Release Date")
    is_book = fields.Boolean(string=u"Est un livre / Ebook",
                             compute="_compute_is_book", store=True)

    _sql_constraints = [('barcode_uniq', 'unique (barcode)',
                         u"ISBN must be unique.")]

    # region compute
    @api.multi
    @api.depends('categ_id')
    def _compute_is_book(self):
        for rec in self:
            rec.is_book = bool(rec.categ_id in (self.env.ref('collection.product_category_book'),
                                                self.env.ref('collection.product_category_ebook')))
