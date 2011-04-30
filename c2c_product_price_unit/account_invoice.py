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

from osv import osv, fields
import decimal_precision as dp

import math
#from _common import rounding
import re  
from tools.translate import _
        
import sys


#----------------------------------------------------------
#  Account Invoice Line INHERIT
#----------------------------------------------------------
class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"
    _columns = {
        'price_unit_id'    : fields.many2one('c2c_product.price_unit','Price Unit' ),
        'price_unit_pu'    : fields.float(string='Unit Price',digits_compute=dp.get_precision('Sale Price'),  \
                            help='Price using "Price Units"') ,
        'price_unit'       : fields.float(string='Unit Price internal',  digits=(16, 8), \
                            help="""Product's cost for accounting stock valuation."""),
    }

    def init(self, cr):
      cr.execute("""
          update account_invoice_line set price_unit_pu = price_unit  where price_unit_pu is null;
      """)
      cr.execute("""
          update account_invoice_line set price_unit_id = (select min(id) from c2c_product_price_unit where coefficient=1) where price_unit_id is null;
      """)
      
    def product_id_change_c2c_pu(self, cr, uid, ids, product, uom, qty=0, name='',
           type=False, partner_id=False, fposition_id=False, price_unit_pu=False, address_invoice_id=False, currency_id=False, context=None,price_unit_id=None):
       res = {}
       print >>sys.stderr,'invocie ',price_unit_id, price_unit_pu

       if product:
           prod = self.pool.get('product.product').browse(cr, uid, product)
           if type in ['out_invoice','out_refund']:
               price_unit_id = prod.list_price_unit_id.id
               
           else:
               price_unit_id = prod.price_unit_id.id
        
           coeff = self.pool.get('c2c_product.price_unit').get_coeff(cr, uid, price_unit_id)
           price_unit = price_unit_pu * coeff 

           res['value'] = super(account_invoice_line, self).product_id_change( cr, uid, ids, product, uom, qty, name,
               type, partner_id, fposition_id, price_unit, address_invoice_id, currency_id, context)['value']
           print  >>sys.stderr, 'invoice res ', res['value']

           res['value']['price_unit_id'] = price_unit_id
           res['value']['price_unit_pu'] = res['value']['price_unit'] * coeff

       return res

    def onchange_price_unit(self, cr, uid, ids, field_name,price_pu, price_unit_id):
        if  price_pu and  price_unit_id:
           coeff = self.pool.get('c2c_product.price_unit').get_coeff(cr, uid, price_unit_id)
           price = price_pu / coeff
           return {'value': {field_name : price}}
        return False

account_invoice_line()


