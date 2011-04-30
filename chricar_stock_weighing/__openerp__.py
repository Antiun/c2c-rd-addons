# -*- coding: utf-8 -*-
{
     "name"         : "Stock Weighing",
     "version"      : "1.0",
     "author"       : "ChriCar Beteiligungs- und Beratungs- GmbH",
     "website"      : "http://www.chricar.at",
     "description"  : """Stock Weighing
Extension to carrier
* allows to records weights of the vehicle etc
Extension to Production
* allows simplified data entry for harvest
* quality attributes for stock_moves
""",
     "category"     : "Client Modules/Farm",
     "depends"      : ["base","stock","mrp","delivery","c2c_sale_multi_partner"],
     "init_xml"     : [],
     "demo_xml"     : [],
     "update_xml"   : ["stock_weighing_view.xml","mrp_view.xml","mrp_workflow.xml","stock_report.xml"],
     "active"       : False,
     "installable"  : True
}
