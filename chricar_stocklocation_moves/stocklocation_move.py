# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2007 TINY SPRL. (http://tiny.be) All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
from mx import DateTime
from mx.DateTime import now
import time

import netsvc
from osv import fields, osv

import wizard
import pooler
from tools import config
from tools.sql import drop_view_if_exists

class chricar_report_location_moves(osv.osv):
        _name = "chricar.report.location.moves"
        _description = "Location Moves"
        _auto = False
        _columns = {
                'name'       : fields.char ('Name',size=16, readonly=True),
                'picking_id'  : fields.many2one('stock.picking','Stock Picking', readonly=True),
                'product_id'  : fields.many2one('product.product', 'Product', readonly=True),
                'location_id' : fields.many2one('stock.location', 'Location', readonly=True),
                'partner_id'  : fields.many2one('res.partner', 'Partner', readonly=True),
                'period_id'   : fields.many2one('account.period', 'Period', readonly=True),
                'prodlot_id'  : fields.many2one('stock.production.lot', 'Production Lot', readonly=True),
                'date': fields.date    ('Date',readonly=True),
                'product_qty' : fields.float('Quantity', readonly=True),
                'move_value_cost' : fields.float('Cost Value', readonly=True),
                'move_value_sale' : fields.float('Sale Value', readonly=True),
                'cost_price' : fields.float('Cost Price', readonly=True),
                'sale_price' : fields.float('Sale Price', readonly=True),
                'usage'      : fields.related('location_id','usage',type="char", relation="stock.location", string="Usage", readonly=True),
                'variants'   : fields.related('product_id','variants',type="char", relation="product.product", string="Variants", readonly=True),
                'categ_id'   : fields.related('product_id','categ_id',type="many2one", relation="product.category", string="Category", readonly=True),
                'state'      : fields.selection([('draft', 'Draft'), ('waiting', 'Waiting'), ('confirmed', 'Confirmed'), ('assigned', 'Available'), ('done', 'Done'), ('cancel', 'Canceled')], 'Status', readonly=True, select=True),

        }
        _order = 'product_id'
        def init(self, cr) :
	        drop_view_if_exists(cr, "chricar_report_location_moves_sum")
	        drop_view_if_exists(cr, "chricar_report_location_moves")
                cr.execute("""
		create or replace view chricar_report_location_moves
                as (
                select id*2 as id,name,
                     picking_id,product_id, 
                     location_dest_id as location_id,
                     partner_id,period_id,prodlot_id,
                     date,
                     product_qty,move_value_cost,move_value_sale,
                     case when product_qty != 0 then  move_value_cost/product_qty  else 0 end as cost_price,
                     case when product_qty != 0 then  move_value_sale/product_qty  else 0 end as sale_price,
                     state
                from stock_move
                    
                union all
                select id*2-1 as id,name,
                     picking_id,product_id, 
                     location_id,
                     partner_id,period_id,prodlot_id,
                     date,
                     -product_qty,-move_value_cost,-move_value_sale,
                     case when product_qty != 0 then  move_value_cost/product_qty  else 0 end as cost_price,
                     case when product_qty != 0 then  move_value_sale/product_qty  else 0 end as sale_price,
                     state
                from stock_move
                    
                   )
                """)
chricar_report_location_moves()


class chricar_report_location_moves_sum(osv.osv):
        _name = "chricar.report.location.moves.sum"
        _description = "Location Product Sum"
        _auto = False
        _columns = {
                'product_id'  : fields.many2one('product.product', 'Product', readonly=True),
                'location_id' : fields.many2one('stock.location', 'Location', readonly=True),
                'product_qty' : fields.float('Quantity', readonly=True),
                'move_value_cost' : fields.float('Cost Value', readonly=True),
                'move_value_sale' : fields.float('Sale Value', readonly=True),
                'cost_price' : fields.float('Cost Price', readonly=True),
                'sale_price' : fields.float('SAle Price', readonly=True),
                'usage'      : fields.related('location_id','usage',type="char", relation="stock.location", string="Usage", readonly=True),
                'categ_id'   : fields.related('product_id','categ_id',type="many2one", relation="product.category", string="Category", readonly=True),
        }
        _order = 'product_id'	
        def init(self, cr):
	        drop_view_if_exists(cr, "chricar_report_location_moves_sum")
                cr.execute("""
                create or replace view chricar_report_location_moves_sum
                as ( 
                select min(id) as id, 
                 product_id,location_id, 
                 sum(product_qty) as product_qty,
                 sum(move_value_cost) as move_value_cost,
                 sum(move_value_sale) as move_value_sale, 
                 case when sum(product_qty) != 0 then  sum(move_value_cost)/sum(product_qty)  else 0 end as cost_price,
                 case when sum(product_qty) != 0 then  sum(move_value_sale)/sum(product_qty)  else 0 end as sale_price
                from chricar_report_location_moves
                where state ='done'
                group by product_id,location_id
                   )
                """)
chricar_report_location_moves_sum()
