# -*- coding: utf-8 -*-
# from odoo import http


# class SambaFileUploadIntegration(http.Controller):
#     @http.route('/samba_file_upload_integration/samba_file_upload_integration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/samba_file_upload_integration/samba_file_upload_integration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('samba_file_upload_integration.listing', {
#             'root': '/samba_file_upload_integration/samba_file_upload_integration',
#             'objects': http.request.env['samba_file_upload_integration.samba_file_upload_integration'].search([]),
#         })

#     @http.route('/samba_file_upload_integration/samba_file_upload_integration/objects/<model("samba_file_upload_integration.samba_file_upload_integration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('samba_file_upload_integration.object', {
#             'object': obj
#         })

