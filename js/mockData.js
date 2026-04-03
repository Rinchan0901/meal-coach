/* ========================================
   Data Constants & Helpers for MealCoach
   ======================================== */

const MEAL_TYPES = {
  breakfast: { label: '朝食', icon: '🌅', badge: 'badge-breakfast' },
  lunch: { label: '昼食', icon: '☀️', badge: 'badge-lunch' },
  dinner: { label: '夕食', icon: '🌙', badge: 'badge-dinner' },
  snack: { label: '間食', icon: '🍪', badge: 'badge-snack' }
};

const DAYS_JP = ['日', '月', '火', '水', '木', '金', '土'];

// AI Prediction mock patterns
const AI_PREDICTIONS = {
  patterns: [
    { menu: '鮭の塩焼き定食', ingredients: ['鮭', '白米', '味噌汁', 'ほうれん草', '大根おろし'], calories: 520 },
    { menu: 'チキンサラダ', ingredients: ['鶏胸肉', 'レタス', 'トマト', 'きゅうり', 'ゆで卵', 'オリーブオイル'], calories: 380 },
    { menu: 'パスタ ボロネーゼ', ingredients: ['スパゲッティ', '合挽き肉', 'トマトソース', '玉ねぎ', 'パルメザンチーズ'], calories: 680 },
    { menu: '野菜炒め定食', ingredients: ['豚肉', 'キャベツ', 'にんじん', 'もやし', '白米', 'わかめスープ'], calories: 580 },
    { menu: 'おにぎりとお味噌汁', ingredients: ['白米', '海苔', '梅干し', '味噌', '豆腐', 'ねぎ'], calories: 350 },
    { menu: 'アサイーボウル', ingredients: ['アサイー', 'バナナ', 'グラノーラ', 'ブルーベリー', 'はちみつ'], calories: 420 },
    { menu: '照り焼きチキン丼', ingredients: ['鶏もも肉', '白米', 'レタス', 'マヨネーズ', '照り焼きソース'], calories: 650 },
    { menu: 'サーモン寿司セット', ingredients: ['サーモン', '酢飯', 'わさび', '醤油', 'ガリ', '枝豆'], calories: 490 },
    { menu: '豚汁と焼き魚', ingredients: ['さば', '大根', 'にんじん', 'こんにゃく', '豚肉', '味噌'], calories: 450 },
    { menu: 'グリーンスムージー', ingredients: ['ほうれん草', 'バナナ', 'りんご', '豆乳', 'チアシード'], calories: 220 }
  ]
};

const SAMPLE_PHOTOS = [
  'linear-gradient(135deg, #f97316, #eab308)',
  'linear-gradient(135deg, #22c55e, #14b8a6)',
  'linear-gradient(135deg, #ef4444, #f97316)',
  'linear-gradient(135deg, #8b5cf6, #ec4899)',
  'linear-gradient(135deg, #3b82f6, #06b6d4)',
  'linear-gradient(135deg, #f59e0b, #84cc16)',
];

// Admin password
const ADMIN_PASSWORD = 'kazuna2026';
const COACH_NAME = 'コーチ';

// Avatar colors for clients
const CLIENT_COLORS = [
  'linear-gradient(135deg, #4ade80, #22d3ee)',
  'linear-gradient(135deg, #a78bfa, #f472b6)',
  'linear-gradient(135deg, #fb923c, #f472b6)',
  'linear-gradient(135deg, #f472b6, #ef4444)',
  'linear-gradient(135deg, #22d3ee, #3b82f6)',
];

// Helper functions
function formatDateKey(date) {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

function formatDateDisplay(dateStr) {
  const d = new Date(dateStr);
  return `${d.getMonth() + 1}/${d.getDate()}(${DAYS_JP[d.getDay()]})`;
}

function formatTime(isoString) {
  const d = new Date(isoString);
  return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
}

function getToday() {
  return formatDateKey(new Date());
}

function getWeekDates(offset = 0) {
  const dates = [];
  const now = new Date();
  const startOfWeek = new Date(now);
  startOfWeek.setDate(now.getDate() - now.getDay() + (offset * 7));

  for (let i = 0; i < 7; i++) {
    const d = new Date(startOfWeek);
    d.setDate(startOfWeek.getDate() + i);
    dates.push({
      date: formatDateKey(d),
      dayLabel: DAYS_JP[d.getDay()],
      dayNum: d.getDate(),
      isToday: formatDateKey(d) === getToday()
    });
  }
  return dates;
}

function formatChatTime(isoString) {
  const d = new Date(isoString);
  const now = new Date();
  const diff = now - d;
  if (diff < 60000) return 'たった今';
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分前`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}時間前`;
  return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
}

function getClientInitial(name) {
  return name ? name.charAt(0) : '?';
}

function getClientColor(clientId) {
  // Deterministic color from clientId
  let hash = 0;
  for (let i = 0; i < clientId.length; i++) hash = clientId.charCodeAt(i) + ((hash << 5) - hash);
  return CLIENT_COLORS[Math.abs(hash) % CLIENT_COLORS.length];
}
