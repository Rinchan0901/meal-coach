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

    // ========== Meals ==========
    getMeals(clientId = 'client-1') {
        const meals = this.get('meals') || [];
        return meals.filter(m => m.clientId === clientId);
    },

    getMealsByDate(dateStr, clientId = 'client-1') {
        return this.getMeals(clientId).filter(m => m.date === dateStr);
    },

    getMealsForWeek(weekOffset = 0, clientId = 'client-1') {
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
            mealId: meal.id,
            message: `${SAMPLE_CLIENTS.find(c => c.id === meal.clientId)?.name || 'クライアント'}が${MEAL_TYPES[meal.type].label}をアップロードしました`,
            timestamp: new Date().toISOString(),
            read: false
        });
    },

    // ========== Health Data ==========
    getHealthData(clientId = 'client-1') {
        const data = this.get('healthData') || [];
        return data.filter(h => h.clientId === clientId);
    },

    getHealthDataByDate(dateStr, clientId = 'client-1') {
        const data = this.getHealthData(clientId);
        return data.find(h => h.date === dateStr) || null;
    },

    getHealthDataForWeek(weekOffset = 0, clientId = 'client-1') {
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
    getFeedbacks(clientId = 'client-1') {
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
        this.set('notifications', notifications.slice(0, 50)); // keep latest 50
    },

    getUnreadCount() {
        return this.getNotifications().filter(n => !n.read).length;
    },

    markAllRead() {
        const notifications = this.getNotifications().map(n => ({ ...n, read: true }));
        this.set('notifications', notifications);
    },

    // ========== Initialize with sample data ==========
    initSampleData() {
        if (this.get('initialized')) return;

        const { meals, healthData } = generateSampleWeekData();
        this.set('meals', meals);
        this.set('healthData', healthData);
        this.set('feedbacks', SAMPLE_FEEDBACKS);
        this.set('notifications', [
            {
                id: 'notif-1',
                type: 'meal_upload',
                clientId: 'client-1',
                message: '田中 美咲さんが昼食をアップロードしました',
                timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
                read: false
            },
            {
                id: 'notif-2',
                type: 'meal_upload',
                clientId: 'client-1',
                message: '田中 美咲さんが朝食をアップロードしました',
                timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
                read: false
            },
            {
                id: 'notif-3',
                type: 'meal_upload',
                clientId: 'client-2',
                message: '佐藤 花子さんが夕食をアップロードしました',
                timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
                read: true
            }
        ]);
        this.set('initialized', true);
    }
};
