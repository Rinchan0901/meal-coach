/* ========================================
   Storage Layer (localStorage wrapper)
   Future: replace with API calls
   ======================================== */

const Storage = {
    PREFIX: 'mealcoach_',

    // ========== Generic Operations ==========
    get(key) {
        try {
            const data = localStorage.getItem(this.PREFIX + key);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.error('Storage.get error:', e);
            return null;
        }
    },

    set(key, value) {
        try {
            localStorage.setItem(this.PREFIX + key, JSON.stringify(value));
        } catch (e) {
            console.error('Storage.set error:', e);
        }
    },

    remove(key) {
        localStorage.removeItem(this.PREFIX + key);
    },

    // ========== Client Identity ==========
    getClientId() {
        let clientId = this.get('my_client_id');
        if (!clientId) {
            clientId = 'client-' + Date.now();
            this.set('my_client_id', clientId);
        }
        return clientId;
    },

    getClientName() {
        return this.get('my_client_name') || null;
    },

    setClientName(name) {
        this.set('my_client_name', name);
        // Register with chat system
        ChatStorage.registerClient(this.getClientId(), name);
    },

    isRegistered() {
        return !!this.get('my_client_name');
    },

    // ========== Meals ==========
    getMeals(clientId) {
        clientId = clientId || this.getClientId();
        const meals = this.get('meals') || [];
        return meals.filter(m => m.clientId === clientId);
    },

    getMealsByDate(dateStr, clientId) {
        clientId = clientId || this.getClientId();
        return this.getMeals(clientId).filter(m => m.date === dateStr);
    },

    getMealsForWeek(weekOffset = 0, clientId) {
        clientId = clientId || this.getClientId();
        const dates = getWeekDates(weekOffset);
        const dateKeys = dates.map(d => d.date);
        return this.getMeals(clientId).filter(m => dateKeys.includes(m.date));
    },

    addMeal(meal) {
        const meals = this.get('meals') || [];
        meals.push(meal);
        this.set('meals', meals);
        this.addNotification({
            type: 'meal_upload',
            clientId: meal.clientId,
            message: `${this.getClientName() || 'クライアント'}が${MEAL_TYPES[meal.type].label}をアップロードしました`,
            timestamp: new Date().toISOString(),
            read: false
        });
    },

    // ========== Health Data ==========
    getHealthData(clientId) {
        clientId = clientId || this.getClientId();
        const data = this.get('healthData') || [];
        return data.filter(h => h.clientId === clientId);
    },

    getHealthDataByDate(dateStr, clientId) {
        clientId = clientId || this.getClientId();
        const data = this.getHealthData(clientId);
        return data.find(h => h.date === dateStr) || null;
    },

    getHealthDataForWeek(weekOffset = 0, clientId) {
        clientId = clientId || this.getClientId();
        const dates = getWeekDates(weekOffset);
        const dateKeys = dates.map(d => d.date);
        return this.getHealthData(clientId).filter(h => dateKeys.includes(h.date));
    },

    saveHealthData(data) {
        const allData = this.get('healthData') || [];
        const existingIndex = allData.findIndex(h => h.date === data.date && h.clientId === data.clientId);
        if (existingIndex >= 0) {
            allData[existingIndex] = data;
        } else {
            allData.push(data);
        }
        this.set('healthData', allData);
    },

    // ========== Feedback ==========
    getFeedbacks(clientId) {
        clientId = clientId || this.getClientId();
        const feedbacks = this.get('feedbacks') || [];
        return feedbacks.filter(f => f.clientId === clientId).sort((a, b) => b.date.localeCompare(a.date));
    },

    addFeedback(feedback) {
        const feedbacks = this.get('feedbacks') || [];
        feedbacks.push(feedback);
        this.set('feedbacks', feedbacks);
    },

    // ========== Notifications (Coach) ==========
    getNotifications() {
        return this.get('notifications') || [];
    },

    addNotification(notification) {
        const notifications = this.get('notifications') || [];
        notifications.unshift({ ...notification, id: 'notif-' + Date.now() });
        this.set('notifications', notifications.slice(0, 50));
    },

    getUnreadCount() {
        return this.getNotifications().filter(n => !n.read).length;
    },

    markAllRead() {
        const notifications = this.getNotifications().map(n => ({ ...n, read: true }));
        this.set('notifications', notifications);
    }
};
