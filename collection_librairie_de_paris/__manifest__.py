# coding: utf8
# encoding: utf-8
#
# Copyright (C) 2021 Iziwas.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

{
    'name': 'Collection Librairie de Paris',
    'version': '0.1',
    'author': 'Iziwas',
    'maintainer': 'Iziwas',
    'category': 'Uncategorized',
    'depends': ['collection'],
    'description': """
Module to manage books information with 'Librairie de Paris'
============================================================
""",
    'data': [
        'views/wizard.xml',
    ],
    'external_dependencies': {
        'python': ['dateparser', 'fake_useragent'],
        'bin': [],
    },
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'application': False,
}
