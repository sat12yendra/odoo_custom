/** @odoo-module */

//
import { patch } from "@web/core/utils/patch";
import { SwitchCompanyMenu } from "@web/webclient/switch_company_menu/switch_company_menu";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";


patch(SwitchCompanyMenu.prototype, {
    setup() {
        super.setup();
        var companyId = this.companyService.activeCompanyIds
        this.rpc = useService('rpc')
        const orm = useService("orm");
        orm.call(
            'ks_custom_report.ks_report',
            'ks_get_company_wise_data',
            [companyId],
        );
    }
});
