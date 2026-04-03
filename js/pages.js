/* ========================================
   Page Renderers
   ======================================== */

const Pages = {

  // =============================================
  // WELCOME / REGISTRATION
  // =============================================

  // ========== Welcome Screen (first-time client) ==========
  welcome() {
    return `
        <div class="page-container" style="min-height:80vh;display:flex;align-items:center;justify-content:center;">
          <div class="glass-card" style="text-align:center;max-width:400px;width:100%;padding:var(--space-3xl) var(--space-xl);">
            <div style="font-size:3rem;margin-bottom:var(--space-lg);">🥗</div>
            <h1 style="font-size:var(--font-2xl);font-weight:800;margin-bottom:var(--space-sm);">
              MealCoachへようこそ
            </h1>
            <p style="color:var(--text-secondary);margin-bottom:var(--space-2xl);font-size:var(--font-sm);">
              食事管理を始めましょう。<br>まずはあなたのお名前を教えてください。
            </p>
            <div class="form-group" style="margin-bottom:var(--space-xl);">
              <input type="text" id="client-name-input" class="form-input"
                placeholder="お名前（例：田中 美咲）"
                style="text-align:center;font-size:var(--font-lg);"
                onkeydown="if(event.key==='Enter')registerClient()">
            </div>
            <button class="btn btn-primary" style="width:100%;padding:var(--space-md) var(--space-xl);font-size:var(--font-md);"
              onclick="registerClient()">
              始める 🚀
            </button>
          </div>
        </div>`;
  },

  // ========== Admin Login ==========
  adminLogin() {
    return `
        <div class="page-container" style="min-height:80vh;display:flex;align-items:center;justify-content:center;">
          <div class="glass-card" style="text-align:center;max-width:400px;width:100%;padding:var(--space-3xl) var(--space-xl);">
            <div style="font-size:3rem;margin-bottom:var(--space-lg);">🔐</div>
            <h1 style="font-size:var(--font-2xl);font-weight:800;margin-bottom:var(--space-sm);">
              管理者ログイン
            </h1>
            <p style="color:var(--text-secondary);margin-bottom:var(--space-2xl);font-size:var(--font-sm);">
              パスワードを入力してください
            </p>
            <div class="form-group" style="margin-bottom:var(--space-md);">
              <input type="password" id="admin-password-input" class="form-input"
                placeholder="パスワード"
                style="text-align:center;font-size:var(--font-lg);"
                onkeydown="if(event.key==='Enter')attemptAdminLogin()">
            </div>
            <div id="login-error" style="color:#ef4444;font-size:var(--font-sm);margin-bottom:var(--space-md);display:none;">
              パスワードが正しくありません
            </div>
            <button class="btn btn-primary" style="width:100%;padding:var(--space-md) var(--space-xl);font-size:var(--font-md);margin-bottom:var(--space-md);"
              onclick="attemptAdminLogin()">
              ログイン
            </button>
            <button class="btn btn-secondary" style="width:100%;"
              onclick="navigateTo('dashboard')">
              ← 戻る
            </button>
          </div>
        </div>`;
  },

  // =============================================
  // CLIENT PAGES
  // =============================================

  // ========== Client Dashboard ==========
  clientDashboard() {
    const clientId = Storage.getClientId();
    const clientName = Storage.getClientName() || 'ゲスト';
    const today = getToday();
    const todayMeals = Storage.getMealsByDate(today, clientId);
    const todayHealth = Storage.getHealthDataByDate(today, clientId);
    const totalCalories = todayMeals.reduce((sum, m) => sum + (m.calories || 0), 0);
    const waterCount = todayHealth ? todayHealth.waterGlasses : 0;
    const streakDays = this._getStreakDays(clientId);
    const feedbacks = Storage.getFeedbacks(clientId);
    const chatUnread = ChatStorage.getUnreadCount(clientId, 'client');

    return `
        <div class="page-container">
          <div class="greeting">
            <h1>こんにちは、${clientName}さん 👋</h1>
            <p>${formatDateDisplay(today)} の食事記録</p>
          </div>

          <div class="stats-grid">
            ${Components.statCard('🍽', todayMeals.length, '今日の食事', 'stat-meals')}
            ${Components.statCard('🔥', totalCalories, 'カロリー', 'stat-calories')}
            ${Components.statCard('💧', waterCount + '杯', '水分摂取', 'stat-water')}
            ${Components.statCard('📅', streakDays + '日', '連続記録', 'stat-streak')}
          </div>

          <div class="section-header">
            <h2>今日の食事</h2>
            <button class="btn btn-sm btn-primary" onclick="navigateTo('upload')">＋ 追加</button>
          </div>

          ${todayMeals.length > 0 ?
        todayMeals.map(m => Components.mealCard(m)).join('') :
        Components.emptyState('🍽️', '今日の食事はまだありません', '「記録」タブから食事を追加しましょう')
      }

          ${feedbacks.length > 0 ? `
            <div class="section-header" style="margin-top:var(--space-xl);">
              <h2>コーチからのフィードバック</h2>
            </div>
            ${Components.feedbackCard(feedbacks[0])}
          ` : ''}
        </div>`;
  },

  _getStreakDays(clientId) {
    let streak = 0;
    const now = new Date();
    for (let i = 0; i < 30; i++) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      const dateStr = formatDateKey(d);
      const meals = Storage.getMealsByDate(dateStr, clientId);
      if (meals.length > 0) streak++;
      else break;
    }
    return streak;
  },

  // ========== Meal Upload ==========
  mealUpload() {
    return `
        <div class="page-container">
          <div class="greeting">
            <h1>食事を記録 📸</h1>
            <p>写真をアップロードしてメニューを記録</p>
          </div>

          <!-- Upload Area -->
          <div class="upload-area" id="upload-area" onclick="document.getElementById('photo-input').click()">
            <input type="file" id="photo-input" accept="image/*" capture="environment"
              style="display:none" onchange="handlePhotoUpload(event)">
            <div class="upload-icon">📷</div>
            <div class="upload-text">写真をタップして選択</div>
            <div class="upload-hint">撮影またはライブラリから選択</div>
          </div>

          <!-- Meal Type -->
          <div class="meal-type-section">
            <div class="section-title">食事タイプ</div>
            <div class="meal-type-grid">
              ${Object.entries(MEAL_TYPES).map(([key, val]) => `
                <button class="meal-type-btn ${key === AppState.currentMealType ? 'active' : ''}"
                  data-type="${key}" onclick="selectMealType('${key}')">
                  <span class="meal-type-icon">${val.icon}</span>
                  <span>${val.label}</span>
                </button>
              `).join('')}
            </div>
          </div>

          <!-- AI Analysis Section (hidden initially) -->
          <div id="ai-section" class="hidden"></div>

          <!-- Skip AI Button -->
          <div id="skip-ai" class="text-center" style="margin-top:var(--space-lg);">
            <button class="btn-link" onclick="showManualInput()">📝 手動で入力する</button>
          </div>

          <!-- Manual Input Section (hidden initially) -->
          <div id="manual-input" class="hidden">
            <div class="glass-card" style="margin-top:var(--space-xl);">
              <div class="section-title">メニュー情報</div>
              <div class="form-group">
                <label class="form-label">メニュー名</label>
                <input type="text" id="menu-name" class="form-input" placeholder="例：鮭の塩焼き定食">
              </div>

              <div class="form-group">
                <label class="form-label">食材</label>
                <div id="ingredients-chips" class="chips-container"></div>
                <div style="display:flex;gap:var(--space-sm);position:relative;">
                  <input type="text" id="ingredient-input" class="form-input" placeholder="食材を追加"
                    oninput="showIngredientSuggestions(this.value)"
                    onkeydown="if(event.key==='Enter'){event.preventDefault();addIngredient();}">
                  <button class="btn btn-sm btn-secondary" onclick="addIngredient()">追加</button>
                </div>
                <div id="ingredient-suggestions" class="suggestions-container hidden"></div>
              </div>

              <div class="form-group">
                <label class="form-label">推定カロリー (kcal)</label>
                <input type="number" id="calories-input" class="form-input" placeholder="例：500">
              </div>

              <button class="btn btn-primary" style="width:100%;margin-top:var(--space-lg);" onclick="saveMeal()">
                ✓ 食事を保存
              </button>
            </div>
          </div>
        </div>`;
  },

  // ========== Health Tracker ==========
  healthTracker() {
    const clientId = Storage.getClientId();
    const today = getToday();
    const health = Storage.getHealthDataByDate(today, clientId) || {
      waterGlasses: 0, bowelMovement: false, bowelQuality: 'normal',
      menstruation: false, weight: '', note: ''
    };

    const waterGlasses = Array.from({ length: 10 }, (_, i) => `
          <div class="water-glass ${i < health.waterGlasses ? 'filled' : ''}"
            onclick="setWaterGlasses(${i + 1})"></div>
        `).join('');

    return `
        <div class="page-container">
          <div class="greeting">
            <h1>健康トラッカー 🏃‍♀️</h1>
            <p>${formatDateDisplay(today)} のコンディション</p>
          </div>

          <!-- Water Intake -->
          <div class="health-section">
            <div class="section-title">💧 水分摂取量</div>
            <div class="glass-card">
              <div class="water-tracker">
                <div class="water-glasses-grid">
                  ${waterGlasses}
                </div>
                <div class="water-count">
                  <span id="water-big-count" class="water-big-number">${health.waterGlasses}</span>
                  <span class="water-unit">杯</span>
                </div>
              </div>
              <div class="water-info">
                <span id="water-count">${health.waterGlasses}</span> / 10杯 (約${health.waterGlasses * 200}mL)
              </div>
            </div>
          </div>

          <!-- Bowel Movement -->
          <div class="health-section">
            <div class="section-title">🟢 排便</div>
            <div class="glass-card">
              <div class="toggle-row">
                <div class="toggle-label">
                  <span class="toggle-icon">💚</span>
                  <div>
                    <div class="toggle-title">排便の有無</div>
                    <div class="toggle-subtitle">今日の排便を記録</div>
                  </div>
                </div>
                <button id="bowel-toggle" class="toggle-btn ${health.bowelMovement ? 'active' : ''}"
                  onclick="toggleBowel()">
                  <span class="toggle-knob"></span>
                </button>
              </div>
            </div>
            <div id="bowel-quality" class="toggle-options ${!health.bowelMovement ? 'hidden' : ''}" style="margin-top:var(--space-sm);">
              <button class="toggle-option ${health.bowelQuality === 'good' ? 'active' : ''}"
                onclick="setBowelQuality('good')">🟢 良好</button>
              <button class="toggle-option ${health.bowelQuality === 'normal' ? 'active' : ''}"
                onclick="setBowelQuality('normal')">🟡 普通</button>
              <button class="toggle-option ${health.bowelQuality === 'bad' ? 'active' : ''}"
                onclick="setBowelQuality('bad')">🔴 不調</button>
            </div>
          </div>

          <!-- Menstruation -->
          <div class="health-section">
            <div class="section-title">🌸 生理</div>
            <div class="glass-card">
              <div class="toggle-row">
                <div class="toggle-label">
                  <span class="toggle-icon">💗</span>
                  <div>
                    <div class="toggle-title">生理期間中</div>
                    <div class="toggle-subtitle">体調管理の参考に記録</div>
                  </div>
                </div>
                <button id="mens-toggle" class="toggle-btn ${health.menstruation ? 'active-pink' : ''}"
                  onclick="toggleMenstruation()">
                  <span class="toggle-knob"></span>
                </button>
              </div>
            </div>
          </div>

          <!-- Weight -->
          <div class="health-section">
            <div class="section-title">⚖️ 体重</div>
            <div class="glass-card">
              <div class="form-group" style="margin:0;">
                <div style="display:flex;align-items:center;gap:var(--space-sm);">
                  <input type="number" id="weight-input" class="form-input"
                    placeholder="例：55.5" step="0.1" value="${health.weight || ''}">
                  <span style="color:var(--text-secondary);">kg</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Note -->
          <div class="health-section">
            <div class="section-title">📝 メモ</div>
            <div class="glass-card">
              <textarea id="health-note" class="form-input" rows="3"
                placeholder="体調や気づいたことがあれば...">${health.note || ''}</textarea>
            </div>
          </div>

          <button class="btn btn-primary" style="width:100%;margin-top:var(--space-xl);padding:var(--space-md);"
            onclick="saveHealthData()">
            💾 保存する
          </button>
        </div>`;
  },

  // ========== Client History ==========
  clientHistory() {
    const clientId = Storage.getClientId();
    const weekDates = getWeekDates();
    const weekMeals = Storage.getMealsForWeek(0, clientId);
    const weekHealth = Storage.getHealthDataForWeek(0, clientId);
    const feedbacks = Storage.getFeedbacks(clientId);

    return `
        <div class="page-container">
          <div class="greeting">
            <h1>今週の記録 📊</h1>
          </div>

          <!-- Week Calendar -->
          <div class="week-calendar">
            ${weekDates.map(d => {
      const dayMeals = weekMeals.filter(m => m.date === d.date);
      return `
              <div class="calendar-day ${d.isToday ? 'today' : ''}" onclick="showDayDetail('${d.date}')">
                <div class="calendar-day-label">${d.dayLabel}</div>
                <div class="calendar-day-num">${d.dayNum}</div>
                <div class="calendar-day-dots">
                  ${dayMeals.map(m => `<span class="dot ${MEAL_TYPES[m.type]?.badge || ''}"></span>`).join('')}
                </div>
                <div class="calendar-day-count">${dayMeals.length > 0 ? dayMeals.length + '食' : ''}</div>
              </div>`;
    }).join('')}
          </div>

          <!-- Health Summary -->
          ${weekHealth.length > 0 ? `
          <div class="section-header" style="margin-top:var(--space-xl);">
            <h2>健康サマリー</h2>
          </div>
          <div class="health-status-row">
            <div class="health-status-item">
              <div class="health-status-icon">💧</div>
              <div class="health-status-value">${(weekHealth.reduce((s, h) => s + h.waterGlasses, 0) / weekHealth.length).toFixed(1)}杯/日</div>
              <div class="health-status-label">平均水分</div>
            </div>
            <div class="health-status-item">
              <div class="health-status-icon">🟢</div>
              <div class="health-status-value">${weekHealth.filter(h => h.bowelMovement).length}/7日</div>
              <div class="health-status-label">排便</div>
            </div>
            <div class="health-status-item">
              <div class="health-status-icon">🌸</div>
              <div class="health-status-value">${weekHealth.filter(h => h.menstruation).length}日間</div>
              <div class="health-status-label">生理</div>
            </div>
          </div>

          <!-- Water Chart -->
          <div class="glass-card" style="margin-top:var(--space-xl);">
            <div class="section-title">水分摂取量</div>
            <div class="water-chart">
              ${weekDates.map(d => {
      const h = weekHealth.find(h => h.date === d.date);
      const glasses = h ? h.waterGlasses : 0;
      const height = Math.max(glasses * 10, 2);
      const color = glasses < 4 ? '#fb923c' : glasses < 7 ? '#3b82f6' : '#22c55e';
      return `
                <div class="chart-bar-container">
                  <span class="chart-bar-value">${glasses}</span>
                  <div class="chart-bar" style="height:${height}%;background:${color};"></div>
                  <span class="chart-bar-label">${d.dayLabel}</span>
                </div>`;
    }).join('')}
            </div>
          </div>
          ` : Components.emptyState('📊', 'まだデータがありません', '健康データを記録すると、ここに表示されます')}

          <!-- Feedback History -->
          ${feedbacks.length > 0 ? `
            <div class="section-header" style="margin-top:var(--space-xl);">
              <h2>フィードバック履歴</h2>
            </div>
            ${feedbacks.map(fb => Components.feedbackCard(fb)).join('')}
          ` : ''}
        </div>`;
  },

  // ========== Client Chat ==========
  clientChat() {
    const clientId = Storage.getClientId();
    const clientName = Storage.getClientName() || 'ゲスト';
    const messages = ChatStorage.getMessages(clientId);
    ChatStorage.markAsRead(clientId, 'client');

    return `
        <div class="page-container chat-page">
          <div class="greeting">
            <h1>💬 コーチとのチャット</h1>
          </div>

          <div class="chat-container" id="chat-container">
            <div class="chat-messages" id="chat-messages">
              ${messages.length > 0 ? messages.map(m => `
                <div class="chat-bubble ${m.sender === 'client' ? 'chat-mine' : 'chat-theirs'}">
                  <div class="chat-bubble-name">${m.sender === 'client' ? clientName : m.senderName}</div>
                  <div class="chat-bubble-body">${m.body.replace(/\n/g, '<br>')}</div>
                  <div class="chat-bubble-time">${formatChatTime(m.timestamp)}</div>
                </div>
              `).join('') : `
                <div class="chat-empty">
                  <div style="font-size:2.5rem;margin-bottom:var(--space-md);">💬</div>
                  <p>コーチとのチャットを始めましょう</p>
                  <p style="font-size:var(--font-xs);color:var(--text-muted);">食事や体調について気軽に相談できます</p>
                </div>
              `}
            </div>
          </div>

          <div class="chat-input-area">
            <div class="chat-input-row">
              <textarea id="chat-input" class="chat-textarea" rows="1"
                placeholder="メッセージを入力..."
                onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendChatMessage();}"></textarea>
              <button class="chat-send-btn" onclick="sendChatMessage()">
                <span>📤</span>
              </button>
            </div>
          </div>
        </div>`;
  },


  // =============================================
  // COACH PAGES
  // =============================================

  // ========== Coach Dashboard ==========
  coachDashboard() {
    const clients = ChatStorage.getKnownClients();
    const unreadNotifs = Storage.getUnreadCount();

    return `
        <div class="page-container">
          <div style="display:flex;align-items:center;gap:var(--space-md);margin-bottom:var(--space-xl);">
            <div class="avatar-lg" style="background:linear-gradient(135deg,#a78bfa,#ec4899);">🩺</div>
            <div>
              <h1 style="font-size:var(--font-2xl);font-weight:800;">コーチ管理</h1>
              <p style="color:var(--text-secondary);">クライアントの食事を管理</p>
            </div>
          </div>

          ${unreadNotifs > 0 ? `
          <div class="glass-card notification-summary" onclick="navigateTo('notifications')">
            <span>🔔</span>
            <div>
              <div style="font-weight:600;">新着通知</div>
              <div style="font-size:var(--font-sm);color:var(--text-secondary);">${unreadNotifs}件の未読</div>
            </div>
            <span class="count-badge">${unreadNotifs}</span>
          </div>
          ` : ''}

          <div class="section-header">
            <h2>クライアント一覧</h2>
            <span style="color:var(--text-secondary);">${clients.length}名</span>
          </div>

          ${clients.length > 0 ? clients.map(client => {
      const meals = Storage.getMeals(client.id);
      const todayMeals = Storage.getMealsByDate(getToday(), client.id);
      const health = Storage.getHealthDataByDate(getToday(), client.id);
      const chatUnread = ChatStorage.getUnreadCount(client.id, 'coach');
      const color = getClientColor(client.id);
      const initial = getClientInitial(client.name);

      return `
            <div class="glass-card client-card" onclick="viewClientWeek('${client.id}')">
              <div class="client-info">
                <div class="avatar" style="background:${color};">${initial}</div>
                <div>
                  <div class="client-name">${client.name}</div>
                  <div class="client-meta">今日: ${todayMeals.length}食 ${health ? '| 💧' + health.waterGlasses + '杯' : ''}</div>
                </div>
              </div>
              <div class="client-badges">
                ${chatUnread > 0 ? `<span class="count-badge">${chatUnread}件</span>` : ''}
                <span class="status-dot online"></span>
              </div>
            </div>`;
    }).join('') : Components.emptyState('👥', 'クライアントがいません', 'クライアントがアプリに登録すると、ここに表示されます')}
        </div>`;
  },

  // ========== Coach Weekly Review ==========
  coachWeeklyReview(clientId) {
    const clients = ChatStorage.getKnownClients();
    const client = clients.find(c => c.id === clientId);
    const clientName = client ? client.name : 'クライアント';
    const initial = getClientInitial(clientName);
    const color = getClientColor(clientId);

    const weekDates = getWeekDates();
    const weekMeals = Storage.getMealsForWeek(0, clientId);
    const weekHealth = Storage.getHealthDataForWeek(0, clientId);
    const feedbacks = Storage.getFeedbacks(clientId);

    return `
        <div class="page-container">
          <button class="btn-link" onclick="navigateTo('coach-dashboard')" style="margin-bottom:var(--space-lg);">
            ← 戻る
          </button>

          <div style="display:flex;align-items:center;gap:var(--space-md);margin-bottom:var(--space-xl);">
            <div class="avatar-lg" style="background:${color};">${initial}</div>
            <div>
              <h1 style="font-size:var(--font-2xl);font-weight:800;">${clientName}</h1>
              <p style="color:var(--text-secondary);">週次レビュー</p>
            </div>
          </div>

          <!-- Week Calendar -->
          <div class="week-calendar">
            ${weekDates.map(d => {
      const dayMeals = weekMeals.filter(m => m.date === d.date);
      return `
              <div class="calendar-day ${d.isToday ? 'today' : ''}" onclick="showDayDetail('${d.date}')">
                <div class="calendar-day-label">${d.dayLabel}</div>
                <div class="calendar-day-num">${d.dayNum}</div>
                <div class="calendar-day-dots">
                  ${dayMeals.map(m => `<span class="dot ${MEAL_TYPES[m.type]?.badge || ''}"></span>`).join('')}
                </div>
                <div class="calendar-day-count">${dayMeals.length > 0 ? dayMeals.length + '食' : '0食'}</div>
              </div>`;
    }).join('')}
          </div>

          <!-- Health Data -->
          ${weekHealth.length > 0 ? `
          <div class="section-header" style="margin-top:var(--space-xl);">
            <h2>健康データ</h2>
          </div>
          <div class="health-status-row">
            <div class="health-status-item">
              <div class="health-status-icon">💧</div>
              <div class="health-status-value">${(weekHealth.reduce((s, h) => s + h.waterGlasses, 0) / weekHealth.length).toFixed(1)}杯/日</div>
              <div class="health-status-label">平均水分</div>
            </div>
            <div class="health-status-item">
              <div class="health-status-icon">🟢</div>
              <div class="health-status-value">${weekHealth.filter(h => h.bowelMovement).length}/7日</div>
              <div class="health-status-label">排便</div>
            </div>
            <div class="health-status-item">
              <div class="health-status-icon">🌸</div>
              <div class="health-status-value">${weekHealth.filter(h => h.menstruation).length}日間</div>
              <div class="health-status-label">生理</div>
            </div>
          </div>

          <!-- Water Chart -->
          <div class="glass-card" style="margin-top:var(--space-xl);">
            <div class="section-title">水分摂取量</div>
            <div class="water-chart">
              ${weekDates.map(d => {
      const h = weekHealth.find(h => h.date === d.date);
      const glasses = h ? h.waterGlasses : 0;
      const height = Math.max(glasses * 10, 2);
      const chartColor = glasses < 4 ? '#fb923c' : glasses < 7 ? '#3b82f6' : '#22c55e';
      return `
                <div class="chart-bar-container">
                  <span class="chart-bar-value">${glasses}</span>
                  <div class="chart-bar" style="height:${height}%;background:${chartColor};"></div>
                  <span class="chart-bar-label">${d.dayLabel}</span>
                </div>`;
    }).join('')}
            </div>
          </div>
          ` : ''}

          <!-- Meal Records -->
          <div class="section-header" style="margin-top:var(--space-xl);">
            <h2>食事記録</h2>
          </div>
          ${weekMeals.length > 0 ?
        weekMeals.sort((a, b) => b.timestamp.localeCompare(a.timestamp)).slice(0, 10).map(m => Components.mealCard(m)).join('') :
        Components.emptyState('🍽️', 'まだ食事記録がありません', '')
      }

          <!-- Feedback -->
          <div class="section-header" style="margin-top:var(--space-xl);">
            <h2>フィードバック</h2>
          </div>
          <div class="glass-card">
            <textarea id="feedback-textarea" class="form-input" rows="4"
              placeholder="クライアントへのアドバイスやコメント..."></textarea>
            <button class="btn btn-primary" style="width:100%;margin-top:var(--space-md);"
              onclick="submitFeedback('${clientId}')">
              📤 フィードバックを送信
            </button>
          </div>

          ${feedbacks.length > 0 ? `
            <div style="margin-top:var(--space-xl);">
              ${feedbacks.map(fb => Components.feedbackCard(fb)).join('')}
            </div>
          ` : ''}
        </div>`;
  },

  // ========== Coach Chat ==========
  coachChat() {
    const clients = ChatStorage.getKnownClients();

    // If a client is selected for chat, show chat
    if (AppState.chatClientId) {
      const client = clients.find(c => c.id === AppState.chatClientId);
      const clientName = client ? client.name : 'クライアント';
      const messages = ChatStorage.getMessages(AppState.chatClientId);
      ChatStorage.markAsRead(AppState.chatClientId, 'coach');

      return `
            <div class="page-container chat-page">
              <div class="chat-header-bar">
                <button class="btn-link" onclick="AppState.chatClientId=null;navigateTo('coach-chat');">← 戻る</button>
                <div style="font-weight:600;">${clientName}</div>
              </div>

              <div class="chat-container" id="chat-container">
                <div class="chat-messages" id="chat-messages">
                  ${messages.length > 0 ? messages.map(m => `
                    <div class="chat-bubble ${m.sender === 'coach' ? 'chat-mine' : 'chat-theirs'}">
                      <div class="chat-bubble-name">${m.sender === 'coach' ? COACH_NAME : m.senderName}</div>
                      <div class="chat-bubble-body">${m.body.replace(/\n/g, '<br>')}</div>
                      <div class="chat-bubble-time">${formatChatTime(m.timestamp)}</div>
                    </div>
                  `).join('') : `
                    <div class="chat-empty">
                      <div style="font-size:2.5rem;margin-bottom:var(--space-md);">💬</div>
                      <p>${clientName}さんとのチャット</p>
                    </div>
                  `}
                </div>
              </div>

              <div class="chat-input-area">
                <div class="chat-input-row">
                  <textarea id="chat-input" class="chat-textarea" rows="1"
                    placeholder="メッセージを入力..."
                    onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendChatMessage();}"></textarea>
                  <button class="chat-send-btn" onclick="sendChatMessage()">
                    <span>📤</span>
                  </button>
                </div>
              </div>
            </div>`;
    }

    // Otherwise show client list
    return `
        <div class="page-container">
          <div class="greeting">
            <h1>💬 チャット</h1>
            <p>クライアントとのメッセージ</p>
          </div>

          ${clients.length > 0 ? clients.map(client => {
      const chatUnread = ChatStorage.getUnreadCount(client.id, 'coach');
      const messages = ChatStorage.getMessages(client.id);
      const lastMsg = messages[messages.length - 1];
      const color = getClientColor(client.id);
      const initial = getClientInitial(client.name);

      return `
            <div class="glass-card client-card" onclick="AppState.chatClientId='${client.id}';navigateTo('coach-chat');">
              <div class="client-info">
                <div class="avatar" style="background:${color};">${initial}</div>
                <div style="min-width:0;flex:1;">
                  <div class="client-name">${client.name}</div>
                  <div class="chat-preview">${lastMsg ? lastMsg.body.substring(0, 30) + (lastMsg.body.length > 30 ? '...' : '') : 'まだメッセージはありません'}</div>
                </div>
              </div>
              <div class="client-badges">
                ${chatUnread > 0 ? `<span class="count-badge">${chatUnread}</span>` : ''}
                ${lastMsg ? `<span class="chat-time">${formatChatTime(lastMsg.timestamp)}</span>` : ''}
              </div>
            </div>`;
    }).join('') : Components.emptyState('💬', 'チャット相手がいません', 'クライアントが登録すると表示されます')}
        </div>`;
  },

  // ========== Coach Notifications ==========
  coachNotifications() {
    const notifications = Storage.getNotifications();
    Storage.markAllRead();

    return `
        <div class="page-container">
          <div class="greeting">
            <h1>通知 🔔</h1>
          </div>

          ${notifications.length > 0 ? notifications.map(n => `
            <div class="glass-card notification-item ${!n.read ? 'unread' : ''}">
              <div class="notif-icon">${n.type === 'meal_upload' ? '🍽️' : '📋'}</div>
              <div class="notif-body">
                <div>${n.message}</div>
                <div class="notif-time">${formatChatTime(n.timestamp)}</div>
              </div>
            </div>
          `).join('') : Components.emptyState('🔔', '通知はありません', '')}
        </div>`;
  }

};
