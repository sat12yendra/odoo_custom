# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Odoo Database Backup",
  "summary"              :  """Module provide feature to admin to take backups of his instance's database and later download them.""",  
  "category"             :  "Extra Tools",
  "version"              :  "1.0.4",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://webkul.com/blog/odoo-data-backup-how-to-create-and-restore-data-in-odoo/",  
  "description"          :  """Module provide feature to admin to take backups of his instance's database and later download them.""",
  "live_test_url"        :  "http://odoodemo.webkul.com/demo_feedback?module=wk_backup_restore",  
  "depends"              :  [
                             'base',
                             'mail'
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'wizards/backup_custom_message_wizard_view.xml',
                             'wizards/backup_deletion_confirmation_view.xml',
                             'views/backup_remote_server.xml',
                             'data/backup_process_sequence.xml',
                             'views/backup_process.xml',
                             'data/backup_ignite_crone.xml',
                             'views/menuitems.xml',
                            ],
  "images"               :  ['static/description/Banner.gif'],
  "application"          :  True,
  "installable"          :  True,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
  "external_dependencies":  {'python': ['python-crontab', 'paramiko']},
}
