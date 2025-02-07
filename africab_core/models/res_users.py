# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"


    def action_create_employee(self):
        self.ensure_one()

        # Search for existing employee based on login email
        existing_employee = self.env['hr.employee'].search([('work_email', '=', self.login)], limit=1)

        if existing_employee:
            existing_employee.write(dict(
                name=self.name,
                company_id=self.company_id.id if self.company_id else self.env.company.id,
                **self.env['hr.employee']._sync_user(self)
            ))
        else:
            # Create a new employee if no existing employee found
            new_employee = self.env['hr.employee'].create(dict(
                name=self.name,
                company_id=self.company_id.id if self.company_id else self.env.company.id,
                **self.env['hr.employee']._sync_user(self)
            ))
            _logger.info(f"Created new employee {new_employee.name} for user {self.login}.")

    @api.model
    def create(self, vals):
        # vals['active'] = False

        # If policy is not updated, show a warning
        # if not self.policy_updated:
        #     raise UserError(_("You cannot create a user without updating the policy!"))

        vals['groups_id'] = [(5, 0, 0)]

        return super(ResUsers, self).create(vals)
