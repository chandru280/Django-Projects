// static/js/service-worker.js

self.addEventListener('push', function(event) {
    const data = event.data.json();  // Parse the notification data

    const options = {
        body: data.body,
        icon: data.icon,
        badge: data.badge || '/static/icons/badge.png',
        data: {
            url: data.url
        }
    };

    event.waitUntil(
        self.registration.showNotification(data.head, options)
    );
});

// Handle click on the notification
self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(
        clients.openWindow(event.notification.data.url)  // Open the provided URL
    );
});
