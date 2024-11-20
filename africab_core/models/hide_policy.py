from odoo import models, fields, api

from odoo.exceptions import ValidationError


class HidePolicy(models.Model):
    _name = 'hide.policy'
    _description = 'Configuration for hide multiple menu items for multiple user'

    name = fields.Char(string='Name', required=True)
    hide_menu_ids = fields.Many2many(
        'ir.ui.menu', string="Hidden Menu",
        store=True, help='Select menu items that need to '
                         'be hidden to this user.')
    restrict_user_ids = fields.Many2many(
        'res.users', string="Restricted Users",
        help='Users restricted from accessing this menu.')
    page_configuration_ids = fields.Many2many(
        'page.configuration',
        string='Page Configurations'
    )

    @api.constrains('restrict_user_ids', 'hide_menu_ids', 'page_configuration_ids')
    def _check_existing_mappings(self):
        """
        Constraint to check if any user in restrict_user_ids is already mapped
        to any menu in hide_menu_ids.
        """
        for record in self:
            for user in record.restrict_user_ids:
                # Search for any menus in hide_menu_ids that already include the user
                already_mapped_menus = self.env['ir.ui.menu'].search([
                    ('id', 'in', record.hide_menu_ids.ids),
                    ('restrict_user_ids', 'in', user.id)
                ])

                already_mapped_pages = self.env['page.configuration'].search([
                    ('id', 'in', record.page_configuration_ids.ids),
                    ('restrict_user_ids', 'in', user.id)
                ])

                if already_mapped_menus:
                    # Collect menu names for a more descriptive error message
                    menu_names = ', '.join(already_mapped_menus.mapped('display_name'))
                    raise ValidationError(
                        f"User '{user.name}' is already mapped to the following menu(s): {menu_names}. "
                        "Please remove these from the selection to avoid duplicate mappings."
                    )

                if already_mapped_pages:
                    # Collect page names for a more descriptive error message
                    page_names = ', '.join(already_mapped_pages.mapped('display_name'))
                    raise ValidationError(
                        f"User '{user.name}' is already mapped to the following page(s): {page_names}. "
                        "Please remove these from the selection to avoid duplicate mappings."
                    )

    def write(self, vals):
        """
        Overriding write method to handle menu hiding logic when records are updated.
        """
        # Before update, remove any outdated restrictions
        for record in self:
            for menu in record.hide_menu_ids:
                menu.write({
                    'restrict_user_ids': [fields.Command.unlink(user.id) for user in record.restrict_user_ids]
                })

            for page in record.page_configuration_ids:
                page.write({
                    'restrict_user_ids': [fields.Command.unlink(user.id) for user in record.restrict_user_ids]
                })

        # Proceed with the standard write operation
        res = super(HidePolicy, self).write(vals)
        # Apply the constraint check before actually updating the record
        self._check_existing_mappings()

        # After update, add new restrictions
        for record in self:
            for menu in record.hide_menu_ids:
                menu.write({
                    'restrict_user_ids': [fields.Command.link(user.id) for user in record.restrict_user_ids]
                })

            for page in record.page_configuration_ids:
                page.write({
                    'restrict_user_ids': [fields.Command.link(user.id) for user in record.restrict_user_ids]
                })

        return res

    def create(self, vals):
        """
        Overriding create method to handle menu hiding logic when new records are created.
        """
        record = super(HidePolicy, self).create(vals)

        # Apply restrictions for the newly created record
        for menu in record.hide_menu_ids:
            menu.write({
                'restrict_user_ids': [fields.Command.link(user.id) for user in record.restrict_user_ids]
            })

        for page in record.page_configuration_ids:
            page.write({
                'restrict_user_ids': [fields.Command.link(user.id) for user in record.restrict_user_ids]
            })

        return record

    def unlink(self):
        """
        Overriding unlink method to clean up restrictions when records are deleted.
        """
        for record in self:
            for menu in record.hide_menu_ids:
                menu.write({
                    'restrict_user_ids': [fields.Command.unlink(user.id) for user in record.restrict_user_ids]
                })

            for page in record.page_configuration_ids:
                page.write({
                    'restrict_user_ids': [fields.Command.unlink(user.id) for user in record.restrict_user_ids]
                })

        return super(HidePolicy, self).unlink()
