from odoo import models, fields, api

class EmployeeMassUpdateWizard(models.TransientModel):
    _name = "employee.mass.update.wizard"
    _description = "Bulk Update Employee Wizard"

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    department_id = fields.Many2one('hr.department', string="Department", domain="[('company_id', '=', company_id)]")
    parent_id = fields.Many2one('hr.employee', string="Manager", domain="[('company_id', '=', company_id)]")

    def action_apply_mass_update(self):
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            return

        employees = self.env['hr.employee'].browse(active_ids)

        values = {}
        if self.department_id:
            values['department_id'] = self.department_id.id
        if self.parent_id:
            values['parent_id'] = self.parent_id.id
        if self.company_id:
            values['company_id'] = self.company_id.id

        if values:
            employees.write(values)

        return {'type': 'ir.actions.act_window_close'}
