# coding: utf-8
# encoding: utf-8
from odoo import models, fields, api


class CollectionProduct(models.Model):
    _inherit = 'product.product'

    author_id = fields.Many2one('res.partner', string=u"Author")
    editor_id = fields.Many2one('res.partner', string=u"Editor")
    ebook_file = fields.Binary(string=u"EBook File", attachment=True)
    summary = fields.Text(string=u"Summary")
