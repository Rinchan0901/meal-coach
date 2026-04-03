/* ========================================
   Chat System
   ======================================== */

const ChatStorage = {
    PREFIX: 'mealcoach_',

    getMessages(clientId) {
        try {
            const data = localStorage.getItem(this.PREFIX + 'chat_' + clientId);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            return [];
        }
    },

    addMessage(clientId, message) {
        const messages = this.getMessages(clientId);
        messages.push({
            id: 'msg-' + Date.now(),
            sender: message.sender, // 'client' or 'coach'
            senderName: message.senderName,
            body: message.body,
            timestamp: new Date().toISOString(),
            read: false
        });
        localStorage.setItem(this.PREFIX + 'chat_' + clientId, JSON.stringify(messages));
    },

    getUnreadCount(clientId, forRole) {
        const messages = this.getMessages(clientId);
        return messages.filter(m => !m.read && m.sender !== forRole).length;
    },

    markAsRead(clientId, forRole) {
        const messages = this.getMessages(clientId);
        messages.forEach(m => {
            if (m.sender !== forRole) m.read = true;
        });
        localStorage.setItem(this.PREFIX + 'chat_' + clientId, JSON.stringify(messages));
    },

    getTotalUnreadForCoach() {
        // Check all known clients
        const clients = JSON.parse(localStorage.getItem(this.PREFIX + 'known_clients') || '[]');
        let total = 0;
        clients.forEach(c => {
            total += this.getUnreadCount(c.id, 'coach');
        });
        return total;
    },

    // Register client so coach can see them
    registerClient(clientId, clientName) {
        const clients = JSON.parse(localStorage.getItem(this.PREFIX + 'known_clients') || '[]');
        const existing = clients.find(c => c.id === clientId);
        if (!existing) {
            clients.push({ id: clientId, name: clientName, registeredAt: new Date().toISOString() });
            localStorage.setItem(this.PREFIX + 'known_clients', JSON.stringify(clients));
        } else if (existing.name !== clientName) {
            existing.name = clientName;
            localStorage.setItem(this.PREFIX + 'known_clients', JSON.stringify(clients));
        }
    },

    getKnownClients() {
        return JSON.parse(localStorage.getItem(this.PREFIX + 'known_clients') || '[]');
    }
};
