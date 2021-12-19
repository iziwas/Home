# coding: utf-8
# encoding: utf-8
from . import librairie_de_paris
from odoo import models, fields, tools
from odoo.exceptions import ValidationError
import base64
from odoo.modules.module import get_module_resource


class CollectionWizardLibrairieDeParis(models.TransientModel):
    _name = 'collection.wizard.librairie.de.paris'
    _description = "Wizard to add books with 'Librairie de Paris' information"
    _soup = False

    isbn = fields.Char(string=u"ISBN", size=13, required=True)
    is_ebook = fields.Boolean(string="Est un Ebook ?", default=False, required=True)

    def add_book(self):
        my_ldp = librairie_de_paris.LibrairieDeParis()
        ldp_book = my_ldp.search_book(self.isbn)

        if not ldp_book:
            raise ValidationError('No result with BeautifoulSoup')

        # search if the ISBN exists in the database
        book = self.env['product.product'].search([('barcode', '=', self.isbn)])
        if book:
            raise ValidationError('This book already exists.')

        # Get Auhtor
        author = self.env['res.partner'].search([('name', 'ilike', ldp_book['author_name'])])
        if not author:
            image_name = 'author.png'
            image_path = get_module_resource('collection', 'static/src/img', image_name)
            image = tools.image_resize_image_big(base64.b64encode(
                open(image_path, 'rb').read()))

            author = self.env['res.partner'].create({
                'name': ldp_book['author_name'],
                'partner_category_id': 
                    self.env.ref('collection.partner_category_author').id,
                'image': image,
            })
        ldp_book['author_id'] = author.id

        # Get Editor
        editor = self.env['res.partner'].search([('name', 'ilike', ldp_book['editor_name'])])
        if not editor:
            image_name = 'publisher.png'
            image_path = get_module_resource('collection', 'static/src/img',
                                             image_name)
            image = tools.image_resize_image_big(base64.b64encode(
                open(image_path, 'rb').read()))

            editor = self.env['res.partner'].create({
                'name': ldp_book['editor_name'],
                'partner_category_id':
                    self.env.ref('collection.partner_category_editor').id,
                'image': image,
            })
        ldp_book['editor_id'] = editor.id

        # Get Collection
        collection = self.env['collection.collection'].search([('name', 'ilike', ldp_book['collection_name'])])
        if not collection:
            collection = self.env['collection.collection'].create({
                'name': ldp_book['collection_name'],
            })
        ldp_book['collection_id'] = collection.id

        # Create book
        ldp_book['categ_id'] = self.env.ref('collection.product_category_ebook').id if self.is_ebook else \
            self.env.ref('collection.product_category_ebook').id

        self.env['product.product'].create({
            'barcode': ldp_book['barcode'],
            'name': ldp_book['name'],
            'summary': ldp_book['summary'],
            'author_id': ldp_book['author_id'],
            'editor_id': ldp_book['editor_id'],
            'collection_id': ldp_book['collection_id'],
            'categ_id': ldp_book['categ_id'],
            'release_date': ldp_book['release_date'],
            'image': ldp_book['image']
        })

        return {'type': 'ir.actions.client', 'tag': 'reload'}


