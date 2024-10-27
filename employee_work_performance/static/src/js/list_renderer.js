/** @odoo-module **/

import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import { Pager } from "@web/core/pager/pager";
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class O2MListRenderer extends ListRenderer {
    get hasSelectors() {
        if (this.props.activeActions.delete) {
            this.props.allowSelectors = true;
        }
        let list = this.props.list;
        list.selection = list.records.filter((rec) => rec.selected);
        list.selectDomain = (value) => {
            list.isDomainSelected = value;
            list.model.notify();
        };
        return this.props.allowSelectors && !this.env.isSmall;
    }

    toggleSelection() {
        const list = this.props.list;
        if (!this.canSelectRecord) {
            return;
        }
        if (list.selection.length === list.records.length) {
            list.records.forEach((record) => {
                record.toggleSelection(false);
                list.selectDomain(false);
            });
        } else {
            list.records.forEach((record) => {
                record.toggleSelection(true);
            });
        }
    }

    get selectAll() {
        const list = this.props.list;
        return list.isDomainSelected;
    }
}

export class TestX2ManyField extends X2ManyField {
    setup() {
        super.setup();
        X2ManyField.components = { Pager, KanbanRenderer, ListRenderer: O2MListRenderer };
        this.dialog = useService("dialog");
        this.rpc = useService("rpc");  // Initialize rpc service
        this.orm = useService("orm");
    }

    get hasSelected() {
        return this.list.records.filter((rec) => rec.selected).length > 0;
    }

async sendTaskMail() {
    const selected = this.list.records.filter((rec) => rec.selected);
    try {
        const response = await this.orm.call("employee.work.performance", "action_send_task_mail", [this.props.record.resId], {
            selected_ids: selected.map((r) => r.resId),
        });

        // Check if response contains the 'params' object with 'title' and 'message'
        if (response && response.params) {
            this.dialog.add(AlertDialog, {
                title: _t(response.params.title || "Notice"), // Default to "Notice" if title is missing
                body: _t(response.params.message || "No message provided."), // Default message if empty
            });
        } else {
            this.dialog.add(AlertDialog, {
                title: _t("Error"),
                body: _t("Unexpected response structure from server."),
            });
        }
    } catch (error) {
        console.error("Error sending mail:", error);
        this.dialog.add(AlertDialog, {
            title: _t("Error"),
            body: _t("Failed to send emails. Please try again later."),
        });
    }
}

}

TestX2ManyField.template = "One2manyTaskSelection";
export const oo = {
    ...x2ManyField,
    component: TestX2ManyField,
};
registry.category("fields").add("one2many_task_selection", oo);
