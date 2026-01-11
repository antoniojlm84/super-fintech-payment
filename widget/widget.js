(function () {
    // Capture the script element immediately while it's executing
    const script = document.currentScript;

    function initSuperPayment() {
        if (!script) {
            console.error("SuperPayment: Could not find script element.");
            return;
        }
        const apiKey = script.getAttribute('data-api-key');
        const orderId = script.getAttribute('data-order-id');
        const amount = script.getAttribute('data-amount');

        const container = document.createElement('div');
        container.id = 'superpayment-container';
        container.style.position = 'fixed';
        container.style.top = '0';
        container.style.left = '0';
        container.style.width = '100%';
        container.style.height = '100%';
        container.style.backgroundColor = 'rgba(0,0,0,0.5)';
        container.style.zIndex = '9999';
        container.style.display = 'flex';
        container.style.justifyContent = 'center';
        container.style.alignItems = 'center';

        // Iframe
        const iframe = document.createElement('iframe');
        iframe.src = `http://localhost:8080/iframe.html?apiKey=${apiKey}&orderId=${orderId}&amount=${amount}`;
        iframe.style.width = '400px';
        iframe.style.height = '500px';
        iframe.style.border = 'none';
        iframe.style.borderRadius = '8px';
        iframe.style.backgroundColor = 'white';

        container.appendChild(iframe);

        // Close on click outside
        container.addEventListener('click', (e) => {
            if (e.target === container) {
                document.body.removeChild(container);
            }
        });

        // Create Trigger Button (if not auto-opened, but user requirement says "Shopper selects to pay...")
        // Requirement: "Shopper selects to pay... A widget is shown"
        // So we trigger it on click of a "Pay with SuperPayment" button usually.
        // For this demo, let's auto-inject a button where the script is, or append to body.

        const btn = document.createElement('button');
        btn.innerText = 'Pay with SuperPayment';
        btn.style.padding = '10px 20px';
        btn.style.fontSize = '16px';
        btn.style.cursor = 'pointer';
        btn.style.backgroundColor = '#007bff';
        btn.style.color = 'white';
        btn.style.border = 'none';
        btn.style.borderRadius = '4px';

        btn.onclick = () => {
            document.body.appendChild(container);
        };

        script.parentNode.insertBefore(btn, script);

        // Listen for success
        window.addEventListener('message', (event) => {
            if (event.data.type === 'SUPERPAYMENT_SUCCESS') {
                setTimeout(() => {
                    document.body.removeChild(container);
                    alert('Order Paid! ' + event.data.payload.purchase_id);
                }, 1500);
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSuperPayment);
    } else {
        initSuperPayment();
    }
})();
