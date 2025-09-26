from odoo import api, fields, models


class ResUsers(models.Model):
    """
    Model to handle hiding specific menu items for certain user roles.
    """
    _inherit = 'res.users.role'

    def write(self, vals):
        # Store old hide_menu_ids per record
        old_hide_menu_map = {record.id: record.hide_menu_ids for record in self}
        res = super().write(vals)
        for record in self:
            old_hide_menu_ids = old_hide_menu_map.get(record.id,
                                                      self.env['ir.ui.menu'])
            # Add new restrictions
            for menu in record.hide_menu_ids:
                menu.sudo().write({'restrict_role_ids': [(4, record.id)]})
            # Remove old ones that are no longer selected
            removed_menus = old_hide_menu_ids - record.hide_menu_ids
            for menu in removed_menus:
                menu.sudo().write({'restrict_role_ids': [(3, record.id)]})
        return res

    def _get_is_admin(self):
        """
        Compute method to check if the user is an admin.
        The Hide specific menu tab will be hidden for the Admin user form.
        """
        for rec in self:
            rec.is_admin = False
            if rec.id == self.env.ref('base.user_admin').id:
                rec.is_admin = True

    
    hide_menu_ids = fields.Many2many(
        'ir.ui.menu', string="Hidden Menu",
        store=True, help='Select menu items that need to '
                         'be hidden to this role.')
    
    is_admin = fields.Boolean(compute='_get_is_admin', string="Is Admin",
                              help='Check if the user is an admin.')
    
    # is_show_specific_menu_role = fields.Boolean(string='Is Show Specific Menu Role', compute='_compute_is_show_specific_menu_role',
    #                                        help='Field determine to show the hide specific menu by role')

    # @api.depends('groups_id')
    # def _compute_is_show_specific_menu_role(self):
    #     """ compute function of the field is show specific menu """
    #     group_id = self.env.ref('base.group_user')
    #     for rec in self:
    #         if group_id.name in rec.user_ids.groups_id.mapped('name'):
    #             rec.is_show_specific_menu_role = False
    #         else:
    #             for menu in rec.hide_menu_ids:
    #                 menu.restrict_user_ids = [fields.Command.unlink(rec.id)]
    #             rec.hide_menu_ids = [fields.Command.clear()]
    #             rec.is_show_specific_menu_role = True


class IrUiMenu(models.Model):
    """
    Model to restrict the menu for specific user roles.
    """
    _inherit = 'ir.ui.menu'

    restrict_role_ids = fields.Many2many(
        'res.users.role', string="Restricted Roles",
        help='Roles restricted from accessing this menu.')

    @api.returns('self')
    def _filter_visible_menus(self):
        """
        Override to filter out menus restricted for current user.
        Applies only to the current user context.
        """
        menus = super()._filter_visible_menus()

        # Allow system admin to see everything
        if self.env.user.has_group('base.group_system'):
            return menus


        return menus.filtered(
            lambda m: self.env.user not in m.restrict_role_ids.user_ids)
