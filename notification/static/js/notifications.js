// static/js/notifications.js

// Check if browser supports Push notifications
if ('Notification' in window && 'serviceWorker' in navigator) {
    // Request notification permission if not granted
    Notification.requestPermission().then(function(permission) {
        if (permission === 'granted') {
            registerServiceWorker();
        }
    });
}

async function registerServiceWorker() {
    const swRegistration = await navigator.serviceWorker.register('/static/js/service-worker.js');
    const subscription = await swRegistration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: '<Your VAPID Public Key>'
    });

    // Send the subscription details to the backend
    await fetch('/webpush/subscribe/', {
        method: 'POST',
        body: JSON.stringify({
            subscription_info: JSON.stringify(subscription),
            csrfmiddlewaretoken: '{{ csrf_token }}'
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
}

// Add the following line in your HTML base template
// <script src="{% static 'js/notifications.js' %}"></script>
