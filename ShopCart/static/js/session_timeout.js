(() => {
    const config = document.getElementById("session-timeout-config");

    // Anonymous visitors don't need a logout timer.
    if (!config) return;

    const TIMEOUT = 15 * 60 * 1000;
    const CHECK_INTERVAL = 30 * 1000;

    const activityUrl = config.dataset.activityUrl;
    const logoutUrl = config.dataset.logoutUrl;
    const loginUrl = config.dataset.loginUrl;

    const csrfToken = config.querySelector(
        'input[name="csrfmiddlewaretoken"]'
    ).value;

    let lastActivity = Date.now();
    let activitySincePing = false;
    let loggingOut = false;
    let requestInProgress = false;

    function markActivity() {
        // If the tab was suspended, don't treat returning to it
        // as permission to revive an expired session.
        if (Date.now() - lastActivity >= TIMEOUT) {
            logout();
            return;
        }

        lastActivity = Date.now();
        activitySincePing = true;
    }

    async function logout() {
        if (loggingOut) return;
        loggingOut = true;

        try {
            await fetch(logoutUrl, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": csrfToken,
                },
            });
        } finally {
            window.location.replace(loginUrl);
        }
    }

    async function checkSession() {
        if (loggingOut) return;

        if (Date.now() - lastActivity >= TIMEOUT) {
            await logout();
            return;
        }

        // Send a heartbeat only if there was actual activity.
        // Polling an idle tab must not keep its session alive.
        if (
            document.hidden ||
            !activitySincePing ||
            requestInProgress
        ) {
            return;
        }

        activitySincePing = false;
        requestInProgress = true;

        try {
            const response = await fetch(activityUrl, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": csrfToken,
                },
            });

            if (response.status === 401) {
                window.location.replace(loginUrl);
            } else if (response.status === 403) {
                // The session/CSRF token may have changed in another tab.
                window.location.reload();
            } else if (!response.ok) {
                activitySincePing = true;
            }
        } catch (error) {
            // Retry when connectivity returns.
            // The server still enforces session expiry.
            activitySincePing = true;
        } finally {
            requestInProgress = false;
        }
    }

    ["pointerdown", "pointermove", "keydown", "scroll", "touchstart"]
        .forEach((eventName) => {
            window.addEventListener(eventName, markActivity, {
                passive: true,
            });
        });

    window.setInterval(checkSession, CHECK_INTERVAL);

    document.addEventListener("visibilitychange", () => {
        if (!document.hidden) {
            checkSession();
        }
    });

    window.addEventListener("pageshow", checkSession);
})();