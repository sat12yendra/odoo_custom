/* @odoo-module */
import { Component, useState } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service";
import { registry } from "@web/core/registry";

const { onMounted } = owl;

class TimerSystrayItem extends Component {
    static template = "auto_logout_idle_user_odoo.TimerSystray";

    setup() {
        super.setup();
        this.state = useState({
            minutes: 0, // Initial idle time
        });
        this.get_idle_time();
    }

    /**
     * Fetch the idle time from the server
     */
    get_idle_time() {
        jsonrpc("/get_idle_time/timer", { method: "call" })
            .then((data) => {
                if (data) {
                    this.state.minutes = data;
                    this.idle_timer();
                }
            })
            .catch((error) => {
                console.error("Error fetching idle time:", error);
            });
    }

    /**
     * Helper function to calculate the new timestamp
     */
    calculate_new_timestamp() {
        const now = new Date().getTime();
        const date = new Date(now);
        date.setMinutes(date.getMinutes() + this.state.minutes);
        return date.getTime();
    }

    /**
     * Start the idle timer
     */
    idle_timer() {
        let updatedTimestamp = this.calculate_new_timestamp();

        /** Countdown timer using setInterval */
        const idle = setInterval(() => {
            const now = new Date().getTime();
            const distance = updatedTimestamp - now;

            if (distance < 0) {
                clearInterval(idle);
                const timerElement = document.querySelector("#idle_timer");
                if (timerElement) timerElement.innerHTML = "EXPIRED";
                location.replace("/web/session/logout");
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            const timerText =
                days > 0
                    ? `${days}d ${hours}h ${minutes}m ${seconds}s`
                    : hours > 0
                    ? `${hours}h ${minutes}m ${seconds}s`
                    : `${minutes}m ${seconds}s`;

            const timerElement = document.querySelector("#idle_timer");
            if (timerElement) timerElement.innerHTML = timerText;
        }, 1000);

        /** Reset idle timer on user activity */
        const reset_on_activity = () => {
            updatedTimestamp = this.calculate_new_timestamp();
        };

        ["mousemove", "keypress", "click", "touchstart", "mousedown"].forEach((event) => {
            document.addEventListener(event, reset_on_activity);
        });
    }
}

export const systrayItem = {
    Component: TimerSystrayItem,
};

registry.category("systray").add("auto_logout_idle_user_odoo.TimerSystray", systrayItem, { sequence: 25 });
