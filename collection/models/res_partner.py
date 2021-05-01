# coding: utf-8
# encoding: utf-8
from odoo import models, fields


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
