# coding: utf-8
# encoding: utf-8
from odoo import models, fields


class CollectionCollection(models.Model):
    _name = 'collection.collection'
    _description = 'Model to store collection of editors'

    name = fields.Char(string=u"Name")
    editor_id = fields.Many2one('res.partner', string=u"Editor")