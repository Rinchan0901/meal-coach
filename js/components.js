/* ========================================
   Reusable Component Renderers
   ======================================== */

const Components = {
    // ========== Meal Card ==========
    mealCard(meal, options = {}) {
        const mealType = MEAL_TYPES[meal.type];
        const photoStyle = meal.photo
            ? `background-image: url(${meal.photo});background-size:cover;background-position:center;`
            : `background: ${meal.photoGradient || 'var(--bg-tertiary)'};display:flex;align-items:center;justify-content:center;font-size:1.5rem;`;
        const photoContent = meal.photo ? '' : mealType.icon;
        const timeStr = meal.timestamp ? formatTime(meal.timestamp) : '';

        return `
      <div class="meal-card animate-fade ${options.stagger || ''}" onclick="${options.onClick || ''}">
        <div class="meal-photo" style="${photoStyle}">${photoContent}</div>
        <div class="meal-info">
          <div class="meal-name">${meal.menu}</div>
          <div class="meal-ingredients">${meal.ingredients.join(', ')}</div>
          <div style="display:flex;align-items:center;gap:var(--space-sm);">
            <span class="badge ${mealType.badge}">${mealType.icon} ${mealType.label}</span>
            ${timeStr ? `<span class="meal-time">${timeStr}</span>` : ''}
            ${meal.calories ? `<span class="meal-time">${meal.calories}kcal</span>` : ''}
          </div>
        </div>
      </div>
    `;
    },

    // ========== Mini Meal Card ==========
    miniMealCard(meal) {
        const mealType = MEAL_TYPES[meal.type];
        const photoStyle = meal.photo
            ? `background-image: url(${meal.photo});background-size:cover;background-position:center;`
            : `background: ${meal.photoGradient || 'var(--bg-tertiary)'};display:flex;align-items:center;justify-content:center;font-size:1rem;`;
        const photoContent = meal.photo ? '' : mealType.icon;

        return `
      <div class="mini-meal-card">
        <div class="mini-photo" style="${photoStyle}">${photoContent}</div>
        <div class="mini-info">
          <div class="mini-name">${meal.menu}</div>
          <span class="badge ${mealType.badge} mini-badge">${mealType.label}</span>
        </div>
      </div>
    `;
    },

    // ========== Stat Card ==========
    statCard(icon, value, label, color = '') {
        return `
      <div class="stat-card animate-scale">
        <div class="stat-icon">${icon}</div>
        <div class="stat-value" ${color ? `style="color:${color}"` : ''}>${value}</div>
        <div class="stat-label">${label}</div>
      </div>
    `;
    },

    // ========== Weekly Calendar ==========
    weeklyCalendar(weekOffset = 0, clientId = 'client-1') {
        const dates = getWeekDates(weekOffset);
        const meals = Storage.getMealsForWeek(weekOffset, clientId);

        const daysHtml = dates.map(d => {
            const dayMeals = meals.filter(m => m.date === d.date);
            const dotsHtml = dayMeals.map(m =>
                `<div class="meal-dot meal-dot-${m.type}"></div>`
            ).join('');

            return `
        <div class="calendar-day ${d.isToday ? 'today' : ''}" onclick="showDayDetail('${d.date}')">
          <div class="calendar-day-label">${d.dayLabel}</div>
          <div class="calendar-day-date">${d.dayNum}</div>
          <div class="meal-dots">${dotsHtml}</div>
          <div style="font-size:10px;color:var(--text-tertiary);">${dayMeals.length}食</div>
        </div>
      `;
        }).join('');

        return `<div class="weekly-calendar">${daysHtml}</div>`;
    },

    // ========== Health Chart (CSS bars) ==========
    waterChart(weekOffset = 0, clientId = 'client-1') {
        const dates = getWeekDates(weekOffset);
        const healthData = Storage.getHealthDataForWeek(weekOffset, clientId);

        const barsHtml = dates.map(d => {
            const data = healthData.find(h => h.date === d.date);
            const glasses = data ? data.waterGlasses : 0;
            const heightPct = Math.min((glasses / 10) * 100, 100);
            const color = glasses >= 8 ? 'var(--accent-green)' : glasses >= 5 ? 'var(--accent-blue)' : 'var(--accent-orange)';

            return `
        <div class="bar-chart-col">
          <div class="bar-chart-value">${glasses}</div>
          <div class="bar-chart-bar" style="height:${heightPct}%;background:${color};"></div>
          <div class="bar-chart-label">${d.dayLabel}</div>
        </div>
      `;
        }).join('');

        return `<div class="bar-chart">${barsHtml}</div>`;
    },

    // ========== Health Status Row ==========
    healthStatusRow(weekOffset = 0, clientId = 'client-1') {
        const healthData = Storage.getHealthDataForWeek(weekOffset, clientId);
        const bowelDays = healthData.filter(h => h.bowelMovement).length;
        const mensDays = healthData.filter(h => h.menstruation).length;
        const avgWater = healthData.length > 0
            ? (healthData.reduce((sum, h) => sum + h.waterGlasses, 0) / healthData.length).toFixed(1)
            : 0;

        return `
      <div class="health-status-row">
        <div class="health-status-item">
          <div class="health-status-icon">💧</div>
          <div class="health-status-value" style="color:var(--accent-blue)">${avgWater}杯/日</div>
          <div class="health-status-label">平均水分</div>
        </div>
        <div class="health-status-item">
          <div class="health-status-icon">🟢</div>
          <div class="health-status-value" style="color:var(--accent-green)">${bowelDays}/7日</div>
          <div class="health-status-label">排便</div>
        </div>
        <div class="health-status-item">
          <div class="health-status-icon">🌸</div>
          <div class="health-status-value" style="color:var(--accent-pink)">${mensDays > 0 ? mensDays + '日間' : 'なし'}</div>
          <div class="health-status-label">生理</div>
        </div>
      </div>
    `;
    },

    // ========== Feedback Card ==========
    feedbackCard(feedback) {
        return `
      <div class="feedback-card animate-fade">
        <div class="feedback-header">
          <div class="feedback-avatar">🩺</div>
          <div class="feedback-meta">
            <div class="feedback-name">${feedback.coachName}</div>
            <div class="feedback-date">${formatDateDisplay(feedback.date)}</div>
          </div>
        </div>
        <div class="feedback-body">${feedback.body.replace(/\n/g, '<br>')}</div>
      </div>
    `;
    },

    // ========== Client Card (Coach View) ==========
    clientCard(client) {
        return `
      <div class="client-card animate-fade" onclick="viewClientWeek('${client.id}')">
        <div class="client-avatar" style="background:${client.gradient}">${client.initial}</div>
        <div class="client-info">
          <div class="client-name">${client.name}</div>
          <div class="client-meta">
            <span>最終: ${client.lastUpload}</span>
            <span>${client.currentWeight}kg</span>
          </div>
        </div>
        ${client.newMeals > 0 ? `
          <div style="display:flex;align-items:center;gap:var(--space-sm);">
            <span class="badge badge-green">${client.newMeals}件</span>
            <div class="notification-dot"></div>
          </div>
        ` : ''}
      </div>
    `;
    },

    // ========== Empty State ==========
    emptyState(icon, title, desc) {
        return `
      <div class="empty-state">
        <div class="empty-state-icon">${icon}</div>
        <div class="empty-state-title">${title}</div>
        <div class="empty-state-desc">${desc}</div>
      </div>
    `;
    },

    // ========== Notification Item ==========
    notificationItem(notification) {
        const time = timeAgo(notification.timestamp);
        return `
      <div class="notification-item ${notification.read ? '' : 'unread'}">
        <div class="notification-icon">📸</div>
        <div class="notification-content">
          <div class="notification-text">${notification.message}</div>
          <div class="notification-time">${time}</div>
        </div>
      </div>
    `;
    }
};

// Helper: time ago
function timeAgo(isoString) {
    const now = new Date();
    const past = new Date(isoString);
    const diffMs = now - past;
    const diffMin = Math.floor(diffMs / 60000);
    const diffHr = Math.floor(diffMin / 60);
    const diffDay = Math.floor(diffHr / 24);

    if (diffMin < 1) return 'たった今';
    if (diffMin < 60) return `${diffMin}分前`;
    if (diffHr < 24) return `${diffHr}時間前`;
    return `${diffDay}日前`;
}
