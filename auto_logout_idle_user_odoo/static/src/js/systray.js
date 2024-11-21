/** @odoo-module **/
import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service";
import { registry } from "@web/core/registry";

class TimerSystrayItem extends Component {
    static template = "auto_logout_idle_user_odoo.TimerSystray";

    setup() {
        this.state = useState({ timerText: "", minutes: 0 });
        this.idleInterval = null;

        onMounted(async () => {
            await this.getIdleTime();
            this.startIdleTimer();
            this.registerActivityListeners();
        });

        onWillUnmount(() => {
            if (this.idleInterval) {
                clearInterval(this.idleInterval);
            }
            this.unregisterActivityListeners();
        });
    }

    async getIdleTime() {
        try {
            const data = await jsonrpc("/get_idle_time/timer", { method: "call" });
            if (data) {
                this.state.minutes = data;
            }
        } catch (error) {
            console.error("Error fetching idle time:", error);
        }
    }

    startIdleTimer() {
        const updateTimestamp = () => {
            const now = new Date().getTime();
            const futureDate = new Date(now);
            futureDate.setMinutes(futureDate.getMinutes() + this.state.minutes);
            return futureDate.getTime();
        };

        let updatedTimestamp = updateTimestamp();

        const updateTimerDisplay = () => {
            const now = new Date().getTime();
            const distance = updatedTimestamp - now;

            if (distance < 0) {
                clearInterval(this.idleInterval);
                this.state.timerText = "EXPIRED";
                window.location.replace("/web/session/logout");
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            this.state.timerText = days > 0
                ? `${days}d ${hours}h ${minutes}m ${seconds}s`
                : hours > 0
                    ? `${hours}h ${minutes}m ${seconds}s`
                    : `${minutes}m ${seconds}s`;
        };

        this.idleInterval = setInterval(updateTimerDisplay, 1000);
        updateTimerDisplay();
    }

    registerActivityListeners() {
        const resetTimestamp = () => {
            const now = new Date().getTime();
            const futureDate = new Date(now);
            futureDate.setMinutes(futureDate.getMinutes() + this.state.minutes);
            this.updatedTimestamp = futureDate.getTime();
        };

        ["mousemove", "keypress", "click", "touchstart", "mousedown"].forEach((event) =>
            document.addEventListener(event, resetTimestamp)
        );
    }

    unregisterActivityListeners() {
        ["mousemove", "keypress", "click", "touchstart", "mousedown"].forEach((event) =>
            document.removeEventListener(event, () => {})
        );
    }
}

// Register the component in the systray menu
export const systrayItem = {
    Component: TimerSystrayItem,
};
registry.category("systray").add("auto_logout_idle_user_odoo.TimerSystray", systrayItem, { sequence: 25 });
