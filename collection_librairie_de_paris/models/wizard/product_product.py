# coding: utf-8
# encoding: utf-8
from odoo import models, fields


class CollectionWizardLibrairieDeParis(models.TransientModel):
    _name = 'collection.wizard.product.librairie.de.paris'
    _description = "Wizard to add books with 'Librairie de Paris' information"

    isbn = fields.Char(string=u"ISBN", size=13)

    def add_book(self):
        pass
