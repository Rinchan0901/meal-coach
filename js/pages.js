/* ========================================
   Page Renderers
   ======================================== */

const Pages = {

    // =============================================
    // CLIENT PAGES
    // =============================================

    // ========== Client Dashboard ==========
    clientDashboard() {
        const today = getToday();
        const todayMeals = Storage.getMealsByDate(today);
        const todayHealth = Storage.getHealthDataByDate(today);
        const feedbacks = Storage.getFeedbacks();
        const latestFeedback = feedbacks[0];

        // Stats
        const totalMealsToday = todayMeals.length;
        const totalCalories = todayMeals.reduce((sum, m) => sum + (m.calories || 0), 0);
        const waterGlasses = todayHealth ? todayHealth.waterGlasses : 0;
        const streakDays = this._getStreakDays();

        return `
      <div class="animate-fade">
        <h1 class="page-title">こんにちは 👋</h1>
        <p class="page-subtitle">${formatDateDisplay(today)} の食事記録</p>

        <!-- Stats -->
        <div class="dashboard-stats">
          ${Components.statCard('🍽️', totalMealsToday, '今日の食事', 'var(--accent-green)')}
          ${Components.statCard('🔥', totalCalories, 'カロリー', 'var(--accent-orange)')}
          ${Components.statCard('💧', waterGlasses + '杯', '水分摂取', 'var(--accent-blue)')}
          ${Components.statCard('📅', streakDays + '日', '連続記録', 'var(--accent-purple)')}
        </div>

        <!-- Today's Meals -->
        <div class="section-header">
          <h2 class="section-title">今日の食事</h2>
          <button class="btn btn-sm btn-primary" onclick="navigateTo('upload')">
            ＋ 追加
          </button>
        </div>

        <div class="today-meals">
          ${todayMeals.length > 0
                ? todayMeals.map((m, i) => Components.mealCard(m, { stagger: `stagger-${i + 1}` })).join('')
                : Components.emptyState('📷', 'まだ食事がありません', '写真をアップロードして記録を始めましょう')
            }
        </div>

        <!-- Latest Feedback -->
        ${latestFeedback ? `
          <div style="margin-top:var(--space-2xl);">
            <div class="section-header">
              <h2 class="section-title">最新フィードバック</h2>
            </div>
            ${Components.feedbackCard(latestFeedback)}
          </div>
        ` : ''}
      </div>
    `;
    },

    _getStreakDays() {
        let streak = 0;
        const now = new Date();
        for (let i = 0; i < 30; i++) {
            const d = new Date(now);
            d.setDate(d.getDate() - i);
            const meals = Storage.getMealsByDate(formatDateKey(d));
            if (meals.length > 0) streak++;
            else break;
        }
        return streak;
    },

    // ========== Meal Upload ==========
    mealUpload() {
        return `
      <div class="animate-fade">
        <h1 class="page-title">食事を記録 📸</h1>
        <p class="page-subtitle">写真をアップロードしてメニューを記録</p>

        <!-- Photo Upload -->
        <div id="upload-container">
          <div class="upload-area" id="upload-area" onclick="document.getElementById('photo-input').click()">
            <div class="upload-icon">📷</div>
            <div class="upload-text">写真をタップして選択</div>
            <div class="upload-hint">撮影またはライブラリから選択</div>
          </div>
          <input type="file" id="photo-input" accept="image/*" capture="environment"
                 style="display:none" onchange="handlePhotoUpload(event)">
        </div>

        <!-- Meal Type Selector -->
        <div style="margin-top:var(--space-xl);">
          <label class="form-label">食事タイプ</label>
          <div class="meal-type-selector" id="meal-type-selector">
            ${Object.entries(MEAL_TYPES).map(([key, val]) => `
              <button class="meal-type-btn ${key === 'lunch' ? 'active' : ''}"
                      data-type="${key}" onclick="selectMealType('${key}')">
                <span class="meal-type-icon">${val.icon}</span>
                <span>${val.label}</span>
              </button>
            `).join('')}
          </div>
        </div>

        <!-- AI Prediction Area (hidden until photo uploaded) -->
        <div id="ai-section" class="hidden" style="margin-top:var(--space-xl);">
          <!-- Will be filled by AI analysis -->
        </div>

        <!-- Manual Input (visible after AI or skip) -->
        <div id="manual-input" class="hidden" style="margin-top:var(--space-xl);">
          <div class="form-group" style="margin-bottom:var(--space-lg);">
            <label class="form-label">メニュー名</label>
            <input type="text" id="menu-name" placeholder="例: 鮭の塩焼き定食">
          </div>

          <div class="form-group" style="margin-bottom:var(--space-lg);">
            <label class="form-label">食材・材料</label>
            <div id="ingredients-chips" style="display:flex;flex-wrap:wrap;gap:var(--space-sm);margin-bottom:var(--space-sm);"></div>
            <div style="display:flex;gap:var(--space-sm);">
              <input type="text" id="ingredient-input" placeholder="食材を入力..."
                     onkeydown="if(event.key==='Enter'){addIngredient();event.preventDefault()}"
                     oninput="showIngredientSuggestions(this.value)">
              <button class="btn btn-secondary btn-sm" onclick="addIngredient()">追加</button>
            </div>
            <div id="ingredient-suggestions" class="hidden"
                 style="margin-top:var(--space-xs);display:flex;flex-wrap:wrap;gap:var(--space-xs);"></div>
          </div>

          <div class="form-group" style="margin-bottom:var(--space-xl);">
            <label class="form-label">推定カロリー (kcal)</label>
            <input type="number" id="calories-input" placeholder="例: 500">
          </div>

          <button class="btn btn-primary btn-block btn-lg" onclick="saveMeal()">
            ✓ 食事を保存
          </button>
        </div>

        <!-- Skip AI button -->
        <div id="skip-ai" style="margin-top:var(--space-xl);text-align:center;">
          <button class="btn btn-ghost" onclick="showManualInput()">
            📝 手動で入力する
          </button>
        </div>
      </div>
    `;
    },

    // ========== Health Tracker ==========
    healthTracker() {
        const today = getToday();
        const data = Storage.getHealthDataByDate(today) || {
            date: today,
            waterGlasses: 0,
            bowelMovement: false,
            bowelQuality: 'normal',
            menstruation: false,
            weight: '',
            note: '',
            clientId: 'client-1'
        };

        const glassesHtml = Array.from({ length: 10 }, (_, i) => {
            const filled = i < data.waterGlasses;
            return `<div class="water-glass ${filled ? 'filled' : ''}" onclick="setWaterGlasses(${i + 1})"></div>`;
        }).join('');

        return `
      <div class="animate-fade">
        <h1 class="page-title">健康トラッカー 🏃‍♀️</h1>
        <p class="page-subtitle">${formatDateDisplay(today)} のコンディション</p>

        <!-- Water Intake -->
        <div class="health-section">
          <div class="health-section-title">💧 水分摂取量</div>
          <div class="water-tracker">
            <div>
              <div class="water-glasses" id="water-glasses">
                ${glassesHtml}
              </div>
              <div style="margin-top:var(--space-sm);font-size:var(--font-sm);color:var(--text-secondary);">
                <span id="water-count">${data.waterGlasses}</span> / 10杯 (約${data.waterGlasses * 200}mL)
              </div>
            </div>
            <div style="text-align:center;">
              <div style="font-size:var(--font-3xl);font-weight:800;color:var(--accent-blue);" id="water-big-count">
                ${data.waterGlasses}
              </div>
              <div style="font-size:var(--font-xs);color:var(--text-tertiary);">杯</div>
            </div>
          </div>
        </div>

        <!-- Bowel Movement -->
        <div class="health-section">
          <div class="health-section-title">🟢 排便</div>
          <div class="toggle-card" style="margin-bottom:var(--space-md);">
            <div class="toggle-card-left">
              <div class="toggle-card-icon">💚</div>
              <div>
                <div class="toggle-card-label">排便の有無</div>
                <div class="toggle-card-sub">今日の排便を記録</div>
              </div>
            </div>
            <div class="toggle-switch ${data.bowelMovement ? 'active' : ''}"
                 id="bowel-toggle" onclick="toggleBowel()"></div>
          </div>
          <div id="bowel-quality" class="${data.bowelMovement ? '' : 'hidden'}">
            <div class="toggle-group">
              <button class="toggle-option ${data.bowelQuality === 'good' ? 'active' : ''}"
                      onclick="setBowelQuality('good')">🟢 良好</button>
              <button class="toggle-option ${data.bowelQuality === 'normal' ? 'active' : ''}"
                      onclick="setBowelQuality('normal')">🟡 普通</button>
              <button class="toggle-option ${data.bowelQuality === 'poor' ? 'active' : ''}"
                      onclick="setBowelQuality('poor')">🔴 不調</button>
            </div>
          </div>
        </div>

        <!-- Menstruation -->
        <div class="health-section">
          <div class="health-section-title">🌸 生理</div>
          <div class="toggle-card">
            <div class="toggle-card-left">
              <div class="toggle-card-icon">🌺</div>
              <div>
                <div class="toggle-card-label">生理期間中</div>
                <div class="toggle-card-sub">ダイエットへの影響を考慮</div>
              </div>
            </div>
            <div class="toggle-switch ${data.menstruation ? 'active-pink' : ''}"
                 id="mens-toggle" onclick="toggleMenstruation()"></div>
          </div>
        </div>

        <!-- Weight -->
        <div class="health-section">
          <div class="health-section-title">⚖️ 体重</div>
          <div class="form-group">
            <div style="display:flex;align-items:center;gap:var(--space-md);">
              <input type="number" id="weight-input" step="0.1" placeholder="55.0"
                     value="${data.weight}" onchange="saveHealthData()" style="max-width:150px;">
              <span style="color:var(--text-secondary);font-weight:600;">kg</span>
            </div>
          </div>
        </div>

        <!-- Note -->
        <div class="health-section">
          <div class="health-section-title">📝 メモ</div>
          <div class="form-group">
            <textarea id="health-note" placeholder="体調や気になったことをメモ..."
                      onchange="saveHealthData()">${data.note || ''}</textarea>
          </div>
        </div>

        <button class="btn btn-primary btn-block btn-lg" onclick="saveHealthData();showToast('保存しました ✓');">
          💾 保存する
        </button>
      </div>
    `;
    },

    // ========== Client History ==========
    clientHistory() {
        const weekDates = getWeekDates(0);
        const feedbacks = Storage.getFeedbacks();

        return `
      <div class="animate-fade">
        <h1 class="page-title">記録一覧 📊</h1>
        <p class="page-subtitle">1週間分の食事と健康データ</p>

        <!-- Weekly Calendar -->
        <div style="margin-bottom:var(--space-2xl);">
          <div class="section-header">
            <h2 class="section-title">今週のカレンダー</h2>
          </div>
          ${Components.weeklyCalendar(0)}
        </div>

        <!-- Health Overview -->
        <div style="margin-bottom:var(--space-2xl);">
          <div class="section-header">
            <h2 class="section-title">健康サマリー</h2>
          </div>
          ${Components.healthStatusRow(0)}
        </div>

        <!-- Water Chart -->
        <div style="margin-bottom:var(--space-2xl);">
          <div class="section-header">
            <h2 class="section-title">💧 水分摂取量</h2>
          </div>
          <div class="card">
            ${Components.waterChart(0)}
          </div>
        </div>

        <!-- Feedback History -->
        <div>
          <div class="section-header">
            <h2 class="section-title">フィードバック履歴</h2>
          </div>
          ${feedbacks.length > 0
                ? feedbacks.map(fb => Components.feedbackCard(fb)).join('<div style="margin-top:var(--space-lg);"></div>')
                : Components.emptyState('💬', 'まだフィードバックがありません', 'コーチからの週次レビューがここに表示されます')
            }
        </div>
      </div>
    `;
    },


    // =============================================
    // COACH PAGES
    // =============================================

    // ========== Coach Dashboard ==========
    coachDashboard() {
        const notifications = Storage.getNotifications();
        const unreadCount = Storage.getUnreadCount();

        return `
      <div class="animate-fade">
        <div class="coach-header">
          <div class="coach-avatar">🩺</div>
          <div>
            <h1 class="page-title" style="margin-bottom:0;">コーチ管理</h1>
            <p class="page-subtitle" style="margin-bottom:0;">クライアントの食事を管理</p>
          </div>
        </div>

        <!-- Notification Summary -->
        ${unreadCount > 0 ? `
          <div class="card card-gradient" style="margin-bottom:var(--space-2xl);cursor:pointer;" onclick="navigateTo('notifications')">
            <div style="display:flex;align-items:center;justify-content:space-between;">
              <div style="display:flex;align-items:center;gap:var(--space-md);">
                <span style="font-size:1.5rem;">🔔</span>
                <div>
                  <div style="font-weight:700;">新着通知</div>
                  <div style="font-size:var(--font-sm);color:var(--text-secondary);">${unreadCount}件の未読</div>
                </div>
              </div>
              <span class="badge badge-green">${unreadCount}</span>
            </div>
          </div>
        ` : ''}

        <!-- Client List -->
        <div class="section-header">
          <h2 class="section-title">クライアント一覧</h2>
          <span class="section-subtitle">${SAMPLE_CLIENTS.length}名</span>
        </div>

        <div class="client-list">
          ${SAMPLE_CLIENTS.map((c, i) => Components.clientCard(c)).join('')}
        </div>
      </div>
    `;
    },

    // ========== Coach Weekly Review ==========
    coachWeeklyReview(clientId = 'client-1') {
        const client = SAMPLE_CLIENTS.find(c => c.id === clientId) || SAMPLE_CLIENTS[0];
        const weekDates = getWeekDates(0);
        const weekMeals = Storage.getMealsForWeek(0, clientId);

        // Group meals by day
        const mealsByDay = {};
        weekDates.forEach(d => {
            mealsByDay[d.date] = weekMeals.filter(m => m.date === d.date);
        });

        return `
      <div class="animate-fade">
        <!-- Back button -->
        <button class="btn btn-ghost" onclick="navigateTo('coach-dashboard')" style="margin-bottom:var(--space-lg);">
          ← 戻る
        </button>

        <div style="display:flex;align-items:center;gap:var(--space-md);margin-bottom:var(--space-xl);">
          <div class="client-avatar" style="background:${client.gradient}">${client.initial}</div>
          <div>
            <h1 class="page-title" style="margin-bottom:0;">${client.name}</h1>
            <p class="page-subtitle" style="margin-bottom:0;">週次レビュー</p>
          </div>
        </div>

        <!-- Weekly Calendar -->
        <div style="margin-bottom:var(--space-2xl);">
          ${Components.weeklyCalendar(0, clientId)}
        </div>

        <!-- Health Summary -->
        <div style="margin-bottom:var(--space-2xl);">
          <div class="section-header">
            <h2 class="section-title">健康データ</h2>
          </div>
          ${Components.healthStatusRow(0, clientId)}
          <div style="margin-top:var(--space-lg);">
            <div class="card">
              <div style="font-size:var(--font-sm);font-weight:600;color:var(--text-secondary);margin-bottom:var(--space-sm);">水分摂取量</div>
              ${Components.waterChart(0, clientId)}
            </div>
          </div>
        </div>

        <!-- Daily Meals -->
        <div style="margin-bottom:var(--space-2xl);">
          <div class="section-header">
            <h2 class="section-title">食事記録</h2>
          </div>

          ${weekDates.map(d => {
            const dayMeals = mealsByDay[d.date] || [];
            if (dayMeals.length === 0) return '';
            return `
              <div class="day-meals-section">
                <div class="day-meals-header">
                  <span>${formatDateDisplay(d.date)}</span>
                  <span class="badge badge-green">${dayMeals.length}食</span>
                </div>
                <div class="day-meals-list">
                  ${dayMeals.map(m => Components.miniMealCard(m)).join('')}
                </div>
              </div>
            `;
        }).join('')}
        </div>

        <!-- Feedback Form -->
        <div class="feedback-form">
          <div class="section-header">
            <h2 class="section-title">📝 フィードバック</h2>
          </div>
          <textarea id="feedback-textarea"
                    placeholder="今週の食事に対するフィードバックを入力...&#10;&#10;例:&#10;・全体的な評価&#10;・改善ポイント&#10;・来週の目標"
                    style="min-height:150px;"></textarea>
          <button class="btn btn-primary btn-block btn-lg" onclick="submitFeedback('${clientId}')">
            📤 フィードバックを送信
          </button>
        </div>
      </div>
    `;
    },

    // ========== Coach Notifications ==========
    coachNotifications() {
        const notifications = Storage.getNotifications();

        return `
      <div class="animate-fade">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:var(--space-xl);">
          <h1 class="page-title" style="margin-bottom:0;">通知 🔔</h1>
          <button class="btn btn-ghost btn-sm" onclick="Storage.markAllRead();navigateTo('notifications');">
            すべて既読
          </button>
        </div>

        <div class="notification-list">
          ${notifications.length > 0
                ? notifications.map(n => Components.notificationItem(n)).join('')
                : Components.emptyState('🔔', '通知はありません', 'クライアントの新着アップロードがここに表示されます')
            }
        </div>
      </div>
    `;
    }
};
