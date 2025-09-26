{
    'name': 'Hide Any Menu User by Role',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Hide Menu Role, Odoo18 Hide Menu Role, Hide Menu Odoo Role, Restrict Menu Items By Role, Odoo18 Menu Role, Odoo18, Odoo Apps',
    'description': 'Hide Any Menu Item User Role, Hide Menu Items by Role, Hide Menu by Role',
    'author': 'Cybrosys Techno Solutions, ABF OSIELL, Odoo Community Association (OCA), acevedoesteban999@gmail.com',
    'maintainer': 'acevedoesteban999@gmail.com',
    'website': "",
    'depends': ['base','hide_menu_user','base_user_role'],
    'data': [
        'views/res_users_role_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': True,
    'application': False,
}
