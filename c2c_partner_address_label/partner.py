# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010-2010 Camptocamp Austria (<http://www.camptocamp.at>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields,osv
import tools
import pooler
from tools.translate import _

#----------------------------------------------------------
#  Country
#----------------------------------------------------------

class Country(osv.osv):
    _inherit = 'res.country'
    _columns = {
        'zip_position' : fields.selection([('before','Before'),('after','After'),('below','Below')], string="Zip Position", help="Zip position relative to city name"),
    }

    _defaults = {
        'zip_position': lambda *a: 'before',
    }

    def init(self, cr):
        # set reasonable values 
        cr.execute("""update res_country
                         set zip_position = 'after'
                       where code in ('US')
                         and zip_position is null""")
        cr.execute("""update res_country
                         set zip_position = 'below'
                       where code in ('GB')
                         and zip_position is null""")
Country()

#----------------------------------------------------------
#  Company
#----------------------------------------------------------

class res_company(osv.osv):
    _inherit = 'res.company'
    _columns = {
        'address_label_position' : fields.selection([('left','Left'),('rigth','Right')], string="Address Window Position", help="Position of address window on standard company enevlops. Many reports do not use this yet"),
    }
    _defaults = {
        'address_label_position': lambda *a: 'right',
    }

res_company()

#----------------------------------------------------------
#  Address
#----------------------------------------------------------
class res_partner_address(osv.osv):
    _inherit = 'res.partner.address'
 
    def _address_label(self, cr, uid, ids, name, arg, context=None):
        res = {}
        lf ='\x0A'
#        lf ='\x0D\x0A'
        for a in self.browse(cr, uid, ids, context=context):
             l = a.partner_id.name or ''
             if a.partner_id.title:
                  l = l + ' ' + a.partner_id.title.name
             t = ''
             if a.title:
                  t = a.title.name + ' ' or ''
             if a.name:
                  t = t + a.name
             if t:
                  l = l + lf + t
             if a.street:
                  l = l + lf + a.street
             if a.street2:
                  l = l + lf + a.street2
             z = ''
             if a.city:
                  z = a.city
             if a.zip:
                  zip_position='before'
                  if a.country_id.zip_position:
                      zip_position = a.country_id.zip_position
                  if zip_position == 'before':
                      z = a.zip + ' ' + z
                  if zip_position == 'after':
                      if a.state_id.code:
                          z = z + ', ' + a.state_id.code +', '+ a.zip
                      else:
                          z = z + ', ' + a.zip
                  if zip_position == 'below':
                      z = z + lf + a.zip
             if z:
                  l = l +lf + z
             if a.state_id:
                  l = l + lf + a.state_id.name
             if a.country_id:
                  l = l + lf + a.country_id.name
             res[a.id] = l
        return res


    _columns = {
        'address_label': fields.function(_address_label, type='text', method = True, string="Address Label"),
    }
    
res_partner_address()