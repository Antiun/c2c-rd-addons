# -*- coding: utf-8 -*-
{
     "name"         : "Product Partner Moves",
     "version"      : "1.0",
     "author"       : "ChriCar Beteiligungs- und Beratungs- GmbH",
     "website"      : "http://www.chricar.at/ChriCar",
     "description"  : """Shows stock move quantites for each partner and period
It's not a sale statistic, this has to be done from invoices.
Adds partner, transaction type and period to stock move.
""",
     "category"     : "Stock Management",
     "depends"      : ["stock","sale","purchase","chricar_view_id","c2c_stock_accounting"],
     "init_xml"     : [],
     "demo_xml"     : [],
     "update_xml"   : ["partner_product_view.xml"],
     "active"       : False,
     "installable"  : True
}
