# coding: utf-8
# encoding: utf-8
from . import librairie_de_paris
from odoo import models, fields, tools
import base64
import logging
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)


class librairie_de_paris_import_ibsn(models.TransientModel):
    _name = 'collection.librairie.de.paris.import.file'
    _description = 'Transient model to import ISBN file'

    isbn_file = fields.Binary(string="ISBN file", attachment=True, required=True)

    def add_books(self):
        datas = base64.b64decode(self.isbn_file)
        for line in datas.split():
            isbn = line.decode('utf-8')
            ldp_book = False
            my_ldp = librairie_de_paris.LibrairieDeParis()

            # Search if ISBN doesn't exist
            book = self.env['product.product'].search([('barcode', '=', isbn)])

            if book:
                continue

            ldp_book = my_ldp.search_book(isbn)

            if not ldp_book:
                continue

            # Get Auhtor
            ldp_book['author_id'] = False
            if ldp_book['author_name']:
                author = self.env['res.partner'].search([('name', '=', ldp_book['author_name'])])
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
            ldp_book['editor_id'] = False
            if ldp_book['editor_name']:
                editor = self.env['res.partner'].search([('name', '=', ldp_book['editor_name'])])
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
            ldp_book['collection_id'] = False
            if ldp_book['collection_name']:
                collection = self.env['collection.collection'].search([
                    ('name', '=', ldp_book['collection_name'])
                ])
                if not collection:
                    collection = self.env['collection.collection'].create({
                        'name': ldp_book['collection_name'],
                    })
                ldp_book['collection_id'] = collection.id

            # Create book
            ldp_book['categ_id'] = self.env.ref('collection.product_category_book').id

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
            _logger.info('Book %s created.' % ldp_book['barcode'])

        return {'type': 'ir.actions.client', 'tag': 'reload'}

