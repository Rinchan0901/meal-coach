/* ========================================
   App Controller
   ======================================== */

// ========== App State ==========
const AppState = {
  currentRole: 'client', // 'client' or 'coach'
  currentPage: 'dashboard',
  currentMealType: 'lunch',
  uploadedImage: null,
  uploadedImageData: null,
  ingredients: [],
  healthData: null,
  selectedClientId: null,
  chatClientId: null
};

// ========== Navigation Config ==========
const NAV_CONFIG = {
  client: [
    { id: 'dashboard', icon: '🏠', label: 'ホーム' },
    { id: 'upload', icon: '📷', label: '記録' },
    { id: 'health', icon: '💧', label: '健康' },
    { id: 'chat', icon: '💬', label: 'チャット' },
    { id: 'history', icon: '📊', label: '履歴' }
  ],
  coach: [
    { id: 'coach-dashboard', icon: '📋', label: '管理' },
    { id: 'coach-chat', icon: '💬', label: 'チャット' },
    { id: 'notifications', icon: '🔔', label: '通知' }
  ]
};

// ========== Initialization ==========
document.addEventListener('DOMContentLoaded', () => {
  // Check if client is registered
  if (!Storage.isRegistered()) {
    showWelcome();
  } else {
    initApp();
  }
});

function initApp() {
  updateHeader();
  renderNav();
  navigateTo('dashboard');
}

function showWelcome() {
  const header = document.getElementById('app-header');
  const nav = document.getElementById('bottom-nav');
  const main = document.getElementById('main-content');
  header.style.display = 'none';
  nav.style.display = 'none';
  main.innerHTML = Pages.welcome();
  setTimeout(() => {
    const input = document.getElementById('client-name-input');
    if (input) input.focus();
  }, 300);
}

function registerClient() {
  const input = document.getElementById('client-name-input');
  const name = input ? input.value.trim() : '';
  if (!name) {
    showToast('お名前を入力してください');
    return;
  }
  Storage.setClientName(name);
  const header = document.getElementById('app-header');
  const nav = document.getElementById('bottom-nav');
  header.style.display = '';
  nav.style.display = '';
  initApp();
  showToast(`ようこそ、${name}さん！🎉`);
}

// ========== Admin Login ==========
function showAdminLogin() {
  AppState.currentPage = 'admin-login';
  const main = document.getElementById('main-content');
  const nav = document.getElementById('bottom-nav');
  nav.style.display = 'none';
  main.innerHTML = Pages.adminLogin();
  setTimeout(() => {
    const input = document.getElementById('admin-password-input');
    if (input) input.focus();
  }, 300);
}

function attemptAdminLogin() {
  const input = document.getElementById('admin-password-input');
  const password = input ? input.value : '';

  if (password === ADMIN_PASSWORD) {
    AppState.currentRole = 'coach';
    const nav = document.getElementById('bottom-nav');
    nav.style.display = '';
    updateHeader();
    renderNav();
    navigateTo('coach-dashboard');
    showToast('管理者としてログインしました 🩺');
  } else {
    const errorEl = document.getElementById('login-error');
    if (errorEl) errorEl.style.display = 'block';
    if (input) {
      input.value = '';
      input.focus();
      input.style.borderColor = '#ef4444';
      setTimeout(() => { input.style.borderColor = ''; }, 2000);
    }
  }
}

function logoutAdmin() {
  AppState.currentRole = 'client';
  AppState.chatClientId = null;
  updateHeader();
  renderNav();
  navigateTo('dashboard');
  showToast('クライアント画面に戻りました');
}

// ========== Header ==========
function updateHeader() {
  const headerRight = document.querySelector('.header-right');
  if (AppState.currentRole === 'coach') {
    headerRight.innerHTML = `
            <button class="role-toggle-btn coach" onclick="logoutAdmin()">
                <span>🩺</span>
                <span>ログアウト</span>
            </button>
        `;
  } else {
    // Subtle admin access icon
    headerRight.innerHTML = `
            <button class="admin-access-btn" onclick="showAdminLogin()" title="管理者">
                <span>⚙️</span>
            </button>
        `;
  }
}

// ========== Navigation ==========
function renderNav() {
  const nav = document.getElementById('bottom-nav');
  const items = NAV_CONFIG[AppState.currentRole];
  const unreadNotifs = Storage.getUnreadCount();
  const clientId = Storage.getClientId();
  const chatUnread = AppState.currentRole === 'client'
    ? ChatStorage.getUnreadCount(clientId, 'client')
    : ChatStorage.getTotalUnreadForCoach();

  nav.innerHTML = items.map(item => {
    const isChatItem = item.id === 'chat' || item.id === 'coach-chat';
    const isNotifItem = item.id === 'notifications';
    const badge = (isChatItem && chatUnread > 0)
      ? `<span class="nav-badge">${chatUnread}</span>`
      : (isNotifItem && unreadNotifs > 0)
        ? `<span class="nav-badge">${unreadNotifs}</span>`
        : '';

    return `
        <button class="nav-item ${AppState.currentPage === item.id ? 'active' : ''}"
                onclick="navigateTo('${item.id}')" id="nav-${item.id}">
          <span class="nav-icon">${item.icon}</span>
          <span>${item.label}</span>
          ${badge}
        </button>`;
  }).join('');
}

function navigateTo(pageId) {
  AppState.currentPage = pageId;
  const main = document.getElementById('main-content');

  // Reset upload state when leaving upload page
  if (pageId !== 'upload') {
    AppState.uploadedImage = null;
    AppState.uploadedImageData = null;
    AppState.ingredients = [];
  }

  // Render page
  switch (pageId) {
    case 'dashboard':
      main.innerHTML = Pages.clientDashboard();
      break;
    case 'upload':
      main.innerHTML = Pages.mealUpload();
      break;
    case 'health':
      main.innerHTML = Pages.healthTracker();
      break;
    case 'history':
      main.innerHTML = Pages.clientHistory();
      break;
    case 'chat':
      main.innerHTML = Pages.clientChat();
      scrollChatToBottom();
      break;
    case 'coach-dashboard':
      main.innerHTML = Pages.coachDashboard();
      break;
    case 'weekly-review':
      main.innerHTML = Pages.coachWeeklyReview(AppState.selectedClientId);
      break;
    case 'coach-chat':
      main.innerHTML = Pages.coachChat();
      scrollChatToBottom();
      break;
    case 'notifications':
      main.innerHTML = Pages.coachNotifications();
      break;
    default:
      main.innerHTML = Pages.clientDashboard();
  }

  renderNav();
  if (pageId !== 'chat' && pageId !== 'coach-chat') {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

// ========== Meal Upload Functions ==========
function selectMealType(type) {
  AppState.currentMealType = type;
  document.querySelectorAll('.meal-type-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.type === type);
  });
}

async function handlePhotoUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = async (e) => {
    AppState.uploadedImageData = e.target.result;
    AppState.uploadedImage = file;

    const uploadArea = document.getElementById('upload-area');
    uploadArea.className = 'upload-area has-image';
    uploadArea.innerHTML = `
      <img src="${e.target.result}" alt="食事写真">
      <button class="change-photo-btn" onclick="event.stopPropagation();document.getElementById('photo-input').click();">
        📷 写真を変更
      </button>
    `;

    const aiSection = document.getElementById('ai-section');
    aiSection.classList.remove('hidden');
    aiSection.innerHTML = `
      <div class="ai-analyzing">
        <div class="spinner"></div>
        <div class="ai-analyzing-text">🤖 AIがメニューを分析中...</div>
      </div>
    `;

    try {
      const result = await AIPredictor.analyzePhoto(file);
      if (result.success) {
        showAIPrediction(result.prediction);
      }
    } catch (err) {
      console.error('AI prediction error:', err);
      showManualInput();
    }
  };
  reader.readAsDataURL(file);
}

function showAIPrediction(prediction) {
  const aiSection = document.getElementById('ai-section');
  const ingredientsHtml = prediction.ingredients.map(ing =>
    `<span class="chip">${ing}</span>`
  ).join('');

  aiSection.innerHTML = `
    <div class="ai-prediction animate-scale">
      <div class="ai-prediction-header">
        <span>🤖</span>
        <span>AI分析結果</span>
      </div>
      <div class="ai-prediction-menu">${prediction.menu}</div>
      <div style="font-size:var(--font-sm);color:var(--text-secondary);margin-bottom:var(--space-md);">
        推定 ${prediction.estimatedCalories}kcal
      </div>
      <div class="ai-prediction-ingredients">
        ${ingredientsHtml}
      </div>
      <div style="display:flex;gap:var(--space-md);margin-top:var(--space-xl);">
        <button class="btn btn-primary" style="flex:1;" onclick="acceptAIPrediction(${JSON.stringify(prediction).replace(/"/g, '&quot;')})">
          ✓ この内容で保存
        </button>
        <button class="btn btn-secondary" onclick="editAIPrediction(${JSON.stringify(prediction).replace(/"/g, '&quot;')})">
          ✏️ 編集
        </button>
      </div>
    </div>
  `;

  document.getElementById('skip-ai').classList.add('hidden');
}

function acceptAIPrediction(prediction) {
  const clientId = Storage.getClientId();
  AppState.ingredients = prediction.ingredients;
  const meal = {
    id: 'meal-' + Date.now(),
    date: getToday(),
    type: AppState.currentMealType,
    menu: prediction.menu,
    ingredients: prediction.ingredients,
    calories: prediction.estimatedCalories,
    photo: AppState.uploadedImageData,
    photoGradient: null,
    timestamp: new Date().toISOString(),
    clientId: clientId
  };

  Storage.addMeal(meal);
  showToast('食事を保存しました 🎉');
  setTimeout(() => navigateTo('dashboard'), 1000);
}

function editAIPrediction(prediction) {
  AppState.ingredients = [...prediction.ingredients];
  showManualInput();

  setTimeout(() => {
    document.getElementById('menu-name').value = prediction.menu;
    document.getElementById('calories-input').value = prediction.estimatedCalories;
    renderIngredientChips();
  }, 100);
}

function showManualInput() {
  document.getElementById('manual-input').classList.remove('hidden');
  document.getElementById('skip-ai').classList.add('hidden');
}

function addIngredient() {
  const input = document.getElementById('ingredient-input');
  const val = input.value.trim();
  if (val && !AppState.ingredients.includes(val)) {
    AppState.ingredients.push(val);
    renderIngredientChips();
    input.value = '';
    hideSuggestions();
  }
}

function removeIngredient(index) {
  AppState.ingredients.splice(index, 1);
  renderIngredientChips();
}

function renderIngredientChips() {
  const container = document.getElementById('ingredients-chips');
  container.innerHTML = AppState.ingredients.map((ing, i) => `
    <span class="chip">
      ${ing}
      <span class="chip-remove" onclick="removeIngredient(${i})">✕</span>
    </span>
  `).join('');
}

function showIngredientSuggestions(query) {
  const suggestions = AIPredictor.suggestIngredients(query);
  const container = document.getElementById('ingredient-suggestions');

  if (suggestions.length > 0 && query.length > 0) {
    container.classList.remove('hidden');
    container.innerHTML = suggestions.slice(0, 8).map(s => `
      <button class="toggle-option" onclick="AppState.ingredients.push('${s}');renderIngredientChips();document.getElementById('ingredient-input').value='';hideSuggestions();">
        ${s}
      </button>
    `).join('');
  } else {
    hideSuggestions();
  }
}

function hideSuggestions() {
  const container = document.getElementById('ingredient-suggestions');
  if (container) container.classList.add('hidden');
}

function saveMeal() {
  const menu = document.getElementById('menu-name').value.trim();
  if (!menu) {
    showToast('メニュー名を入力してください');
    return;
  }

  const clientId = Storage.getClientId();
  const calories = parseInt(document.getElementById('calories-input').value) || 0;

  const meal = {
    id: 'meal-' + Date.now(),
    date: getToday(),
    type: AppState.currentMealType,
    menu: menu,
    ingredients: [...AppState.ingredients],
    calories: calories,
    photo: AppState.uploadedImageData,
    photoGradient: SAMPLE_PHOTOS[Math.floor(Math.random() * SAMPLE_PHOTOS.length)],
    timestamp: new Date().toISOString(),
    clientId: clientId
  };

  Storage.addMeal(meal);
  showToast('食事を保存しました 🎉');
  setTimeout(() => navigateTo('dashboard'), 1000);
}

// ========== Health Tracker Functions ==========
function setWaterGlasses(count) {
  const data = getCurrentHealthData();
  data.waterGlasses = count;
  Storage.saveHealthData(data);

  document.querySelectorAll('.water-glass').forEach((el, i) => {
    el.classList.toggle('filled', i < count);
  });
  document.getElementById('water-count').textContent = count;
  document.getElementById('water-big-count').textContent = count;
}

function toggleBowel() {
  const data = getCurrentHealthData();
  data.bowelMovement = !data.bowelMovement;
  Storage.saveHealthData(data);

  const toggle = document.getElementById('bowel-toggle');
  toggle.classList.toggle('active');

  const quality = document.getElementById('bowel-quality');
  quality.classList.toggle('hidden', !data.bowelMovement);
}

function setBowelQuality(quality) {
  const data = getCurrentHealthData();
  data.bowelQuality = quality;
  Storage.saveHealthData(data);

  document.querySelectorAll('#bowel-quality .toggle-option').forEach(btn => {
    btn.classList.remove('active');
  });
  event.target.classList.add('active');
}

function toggleMenstruation() {
  const data = getCurrentHealthData();
  data.menstruation = !data.menstruation;
  Storage.saveHealthData(data);

  const toggle = document.getElementById('mens-toggle');
  if (data.menstruation) {
    toggle.classList.add('active-pink');
  } else {
    toggle.classList.remove('active-pink');
  }
}

function saveHealthData() {
  const data = getCurrentHealthData();
  data.weight = document.getElementById('weight-input')?.value || '';
  data.note = document.getElementById('health-note')?.value || '';
  Storage.saveHealthData(data);
  showToast('保存しました 💾');
}

function getCurrentHealthData() {
  const today = getToday();
  const clientId = Storage.getClientId();
  return Storage.getHealthDataByDate(today, clientId) || {
    date: today,
    waterGlasses: 0,
    bowelMovement: false,
    bowelQuality: 'normal',
    menstruation: false,
    weight: '',
    note: '',
    clientId: clientId
  };
}

// ========== Chat Functions ==========
function sendChatMessage() {
  const input = document.getElementById('chat-input');
  const body = input ? input.value.trim() : '';
  if (!body) return;

  const isCoach = AppState.currentRole === 'coach';
  const clientId = isCoach ? AppState.chatClientId : Storage.getClientId();
  const senderName = isCoach ? COACH_NAME : Storage.getClientName();

  ChatStorage.addMessage(clientId, {
    sender: isCoach ? 'coach' : 'client',
    senderName: senderName,
    body: body
  });

  // Refresh chat page
  navigateTo(isCoach ? 'coach-chat' : 'chat');
}

function scrollChatToBottom() {
  setTimeout(() => {
    const container = document.getElementById('chat-messages');
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }, 100);
}

// ========== Coach Functions ==========
function viewClientWeek(clientId) {
  AppState.selectedClientId = clientId;
  navigateTo('weekly-review');
}

function submitFeedback(clientId) {
  const textarea = document.getElementById('feedback-textarea');
  const body = textarea.value.trim();

  if (!body) {
    showToast('フィードバックを入力してください');
    return;
  }

  const feedback = {
    id: 'fb-' + Date.now(),
    coachName: COACH_NAME,
    date: getToday(),
    clientId: clientId,
    body: body
  };

  Storage.addFeedback(feedback);
  showToast('フィードバックを送信しました 📤');
  textarea.value = '';
}

// ========== Day Detail Modal ==========
function showDayDetail(dateStr) {
  const targetClientId = AppState.currentRole === 'coach'
    ? (AppState.selectedClientId || Storage.getClientId())
    : Storage.getClientId();
  const meals = Storage.getMealsByDate(dateStr, targetClientId);
  const health = Storage.getHealthDataByDate(dateStr, targetClientId);

  const modalBody = document.getElementById('modal-body');
  modalBody.innerHTML = `
    <h2 style="font-size:var(--font-xl);font-weight:700;margin-bottom:var(--space-xl);">
      ${formatDateDisplay(dateStr)} の記録
    </h2>

    ${meals.length > 0 ? `
      <div style="margin-bottom:var(--space-xl);">
        <h3 style="font-size:var(--font-md);font-weight:600;margin-bottom:var(--space-md);">🍽️ 食事</h3>
        ${meals.map(m => Components.mealCard(m)).join('')}
      </div>
    ` : `
      <div style="margin-bottom:var(--space-xl);">
        ${Components.emptyState('🍽️', '食事記録なし', '')}
      </div>
    `}

    ${health ? `
      <div>
        <h3 style="font-size:var(--font-md);font-weight:600;margin-bottom:var(--space-md);">🏃‍♀️ 健康データ</h3>
        <div class="health-status-row">
          <div class="health-status-item">
            <div class="health-status-icon">💧</div>
            <div class="health-status-value">${health.waterGlasses}杯</div>
            <div class="health-status-label">水分</div>
          </div>
          <div class="health-status-item">
            <div class="health-status-icon">${health.bowelMovement ? '🟢' : '🔴'}</div>
            <div class="health-status-value">${health.bowelMovement ? 'あり' : 'なし'}</div>
            <div class="health-status-label">排便</div>
          </div>
          <div class="health-status-item">
            <div class="health-status-icon">🌸</div>
            <div class="health-status-value">${health.menstruation ? 'あり' : 'なし'}</div>
            <div class="health-status-label">生理</div>
          </div>
        </div>
        ${health.weight ? `
          <div style="margin-top:var(--space-md);text-align:center;font-size:var(--font-sm);color:var(--text-secondary);">
            体重: <strong>${health.weight}kg</strong>
          </div>
        ` : ''}
        ${health.note ? `
          <div style="margin-top:var(--space-md);padding:var(--space-md);background:var(--bg-glass);border-radius:var(--radius-md);font-size:var(--font-sm);color:var(--text-secondary);">
            📝 ${health.note}
          </div>
        ` : ''}
      </div>
    ` : ''}
  `;

  openModal();
}

// ========== Modal ==========
function openModal() {
  document.getElementById('modal-overlay').classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('modal-overlay').classList.add('hidden');
  document.body.style.overflow = '';
}

// ========== Toast ==========
function showToast(message) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.remove('hidden');
  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.classList.add('hidden'), 300);
  }, 2500);
}
