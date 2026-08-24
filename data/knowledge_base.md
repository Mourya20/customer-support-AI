# Customer Support Knowledge Base

## Billing

### Duplicate Charge Resolution
If a customer reports being charged twice for the same subscription period, first verify the invoice timestamps and transaction IDs. If duplicate charges are confirmed, issue a refund for the duplicate transaction within 5 to 7 business days.

### Refund Timeline
Refunds are typically reflected in the original payment method in 5 to 10 business days depending on the bank. Advise customers to keep the refund reference ID for follow-up.

### Failed Payment and Grace Period
If a recurring payment fails, the account enters a 3-day grace period. During this period, customers can update payment details in the billing portal without immediate service interruption.

## Technical

### HTTP 500 Errors
A 500 error usually indicates a server-side issue. Ask the customer to share timestamp, endpoint, and request ID. Recommend checking service status, restarting the application worker, and reviewing server logs around the failure time.

### Slow Application Performance
For performance issues, capture browser version, device, network type, and the specific feature affected. Suggest clearing cache and retrying in an incognito window before deeper backend investigation.

### Login Page Not Loading
If the login page does not load, confirm whether CDN or DNS incidents are active. Ask users to try another network and disable browser extensions that block scripts.

## Account Access

### Password Reset
If customers cannot log in, direct them to the password reset flow. Password reset emails should arrive within a few minutes; customers should check spam folders if not received.

### Locked Account
After multiple failed login attempts, accounts are locked for 15 minutes. If lockout persists after 15 minutes, escalate to account security support.

### Two-Factor Authentication (2FA)
If users lose access to their authenticator app, verify identity and issue a one-time recovery link. Recommend re-enabling 2FA immediately after account access is restored.
