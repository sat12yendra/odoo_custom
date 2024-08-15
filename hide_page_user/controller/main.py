from odoo import http
from odoo.http import request


class UserPageConfiguration(http.Controller):
    @http.route('/get_user_page_configurations', auth='user', type='json')
    def get_user_page_configurations(self):
        user = request.env.user
        # Assuming 'get_user_page_configurations' is a method defined in 'res.users'
        page_configurations = user.get_user_page_configurations()
        return page_configurations