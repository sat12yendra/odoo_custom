# -*- coding: utf-8 -*-
# from odoo import http


# class Hrms(http.Controller):
#     @http.route('/hrms/hrms', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hrms/hrms/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hrms.listing', {
#             'root': '/hrms/hrms',
#             'objects': http.request.env['hrms.hrms'].search([]),
#         })

#     @http.route('/hrms/hrms/objects/<model("hrms.hrms"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hrms.object', {
#             'object': obj
#         })

