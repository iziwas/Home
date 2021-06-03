# coding: utf8
# encoding: utf8
from odoo import models, fields


class CollectionISBN(models.Model):
    _name = 'collection.isbn'
    _description = 'Class to manage ISBN'

    isbn = fields.Char(string=u"ISBN")
    data_found = fields.Boolean(string=u"Données récupérées", default=False)
