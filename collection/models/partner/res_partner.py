# coding: utf-8
# encoding: utf-8
from odoo import models, fields, api, tools


class CollectionPartnerCategory(models.Model):
    _name = 'collection.partner.category'
    _description = 'Class to define Partner Category'

    name = fields.Char(string=u"Category", required=True)
    is_author = fields.Boolean(string=u"Is Author ?")
    is_editor = fields.Boolean(string=u"Is Editor ?")


class CollectionPartner(models.Model):
    _inherit = 'res.partner'

    partner_category_id = fields.Many2one('collection.partner.category',
                                          string=u"Contact type")
    is_author = fields.Boolean(string=u"Is Author ?",
                               related="partner_category_id.is_author")
    is_editor = fields.Boolean(string=u"Is Editor ?",
                               related="partner_category_id.is_editor")
    book_author_ids = fields.One2many('product.product', 'author_id',
                                      string=u"Author Books")
    book_editor_ids = fields.One2many('product.product', 'editor_id',
                                      string=u"Editor Books")
    nb_books_author = fields.Integer(string="Number of books (Author)",
                                     compute="_compute_nb_books")
    nb_books_editor = fields.Integer(string="Number of books (Editor)",
                                     compute="_compute_nb_books")
    collection_ids = fields.One2many('collection.collection', 'editor_id',
                                     string=u"Collection")

    @api.multi
    def _compute_nb_books(self):
        for rec in self:
            rec.nb_books_author = len(rec.book_author_ids)
            rec.nb_books_editor = len(rec.book_editor_ids)
