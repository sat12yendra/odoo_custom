/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { FormController } from '@web/views/form/form_controller';
import { jsonrpc } from '@web/core/network/rpc_service';

patch(FormController.prototype, {
    async setup() {
        await super.setup();

        // Fetch user's page configurations
        const pageConfigurations = await this._getUserPageConfigurations();

        // Apply a delay to ensure the DOM is fully rendered
        setTimeout(() => {
            pageConfigurations.forEach((pageName) => this._hidePage(pageName));
        }, 500); // Adjust delay if necessary
    },

    async _getUserPageConfigurations() {
        try {
            // Call the server-side endpoint to get the page configurations
            const result = await jsonrpc('/get_user_page_configurations', {});
            console.log('Fetch result:', result); // Debugging line
            return result || [];
        } catch (error) {
            console.error('Error fetching user page configurations:', error);
            return [];
        }
    },

    _hidePage(pageName) {
        // Use a selector to find the page with the specified name
        const $pageElement = document.querySelector(`[name="${pageName}"]`);
        if ($pageElement) {
            $pageElement.style.display = 'none';
            console.log(`Hiding page with name: ${pageName}`);
        } else {
            console.warn(`Page element not found for name: ${pageName}`);
        }
    }
});
