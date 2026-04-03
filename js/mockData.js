/* ========================================
   Mock Data for MealCoach App
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
  // Matches image patterns to likely foods (simulated)
  patterns: [
    {
      menu: '鮭の塩焼き定食',
      ingredients: ['鮭', '白米', '味噌汁', 'ほうれん草', '大根おろし'],
      calories: 520
    },
    {
      menu: 'チキンサラダ',
      ingredients: ['鶏胸肉', 'レタス', 'トマト', 'きゅうり', 'ゆで卵', 'オリーブオイル'],
      calories: 380
    },
    {
      menu: 'パスタ ボロネーゼ',
      ingredients: ['スパゲッティ', '合挽き肉', 'トマトソース', '玉ねぎ', 'パルメザンチーズ'],
      calories: 680
    },
    {
      menu: '野菜炒め定食',
      ingredients: ['豚肉', 'キャベツ', 'にんじん', 'もやし', '白米', 'わかめスープ'],
      calories: 580
    },
    {
      menu: 'おにぎりとお味噌汁',
      ingredients: ['白米', '海苔', '梅干し', '味噌', '豆腐', 'ねぎ'],
      calories: 350
    },
    {
      menu: 'アサイーボウル',
      ingredients: ['アサイー', 'バナナ', 'グラノーラ', 'ブルーベリー', 'はちみつ'],
      calories: 420
    },
    {
      menu: '照り焼きチキン丼',
      ingredients: ['鶏もも肉', '白米', 'レタス', 'マヨネーズ', '照り焼きソース'],
      calories: 650
    },
    {
      menu: 'サーモン寿司セット',
      ingredients: ['サーモン', '酢飯', 'わさび', '醤油', 'ガリ', '枝豆'],
      calories: 490
    },
    {
      menu: '豚汁と焼き魚',
      ingredients: ['さば', '大根', 'にんじん', 'こんにゃく', '豚肉', '味噌'],
      calories: 450
    },
    {
      menu: 'グリーンスムージー',
      ingredients: ['ほうれん草', 'バナナ', 'りんご', '豆乳', 'チアシード'],
      calories: 220
    }
  ]
};

// Sample meal photos (using placeholder gradients)
const SAMPLE_PHOTOS = [
  'linear-gradient(135deg, #f97316, #eab308)',
  'linear-gradient(135deg, #22c55e, #14b8a6)',
  'linear-gradient(135deg, #ef4444, #f97316)',
  'linear-gradient(135deg, #8b5cf6, #ec4899)',
  'linear-gradient(135deg, #3b82f6, #06b6d4)',
  'linear-gradient(135deg, #f59e0b, #84cc16)',
];

// Generate sample data for the past week
function generateSampleWeekData() {
  const meals = [];
  const healthData = [];
  const now = new Date();

  for (let i = 6; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    const dateStr = formatDateKey(date);

    // Random meals for each day
    const dayMealCount = Math.floor(Math.random() * 3) + 2; // 2-4 meals
    const mealTypes = ['breakfast', 'lunch', 'dinner', 'snack'];

    for (let j = 0; j < dayMealCount; j++) {
      const prediction = AI_PREDICTIONS.patterns[Math.floor(Math.random() * AI_PREDICTIONS.patterns.length)];
      const photoGrad = SAMPLE_PHOTOS[Math.floor(Math.random() * SAMPLE_PHOTOS.length)];

      meals.push({
        id: `meal-${dateStr}-${j}`,
        date: dateStr,
        type: mealTypes[j] || 'snack',
        menu: prediction.menu,
        ingredients: prediction.ingredients,
        calories: prediction.calories,
        photo: null,
        photoGradient: photoGrad,
        timestamp: new Date(date.getFullYear(), date.getMonth(), date.getDate(),
          j === 0 ? 7 : j === 1 ? 12 : j === 2 ? 19 : 15,
          Math.floor(Math.random() * 60)
        ).toISOString(),
        clientId: 'client-1'
      });
    }

    // Health data for each day
    healthData.push({
      date: dateStr,
      waterGlasses: Math.floor(Math.random() * 6) + 3, // 3-8 glasses
      bowelMovement: Math.random() > 0.3,
      bowelQuality: Math.random() > 0.5 ? 'good' : 'normal',
      menstruation: i <= 1 && Math.random() > 0.5,
      weight: (55 + Math.random() * 3).toFixed(1),
      note: '',
      clientId: 'client-1'
    });
  }

  return { meals, healthData };
}

// Sample clients (for coach view)
const SAMPLE_CLIENTS = [
  {
    id: 'client-1',
    name: '田中 美咲',
    initial: '田',
    startDate: '2026-03-01',
    goalWeight: 52,
    currentWeight: 55.8,
    lastUpload: '2時間前',
    newMeals: 3,
    gradient: 'linear-gradient(135deg, #4ade80, #22d3ee)'
  },
  {
    id: 'client-2',
    name: '佐藤 花子',
    initial: '佐',
    startDate: '2026-03-15',
    goalWeight: 48,
    currentWeight: 51.2,
    lastUpload: '5時間前',
    newMeals: 1,
    gradient: 'linear-gradient(135deg, #a78bfa, #f472b6)'
  },
  {
    id: 'client-3',
    name: '鈴木 優子',
    initial: '鈴',
    startDate: '2026-02-20',
    goalWeight: 55,
    currentWeight: 58.5,
    lastUpload: '1日前',
    newMeals: 0,
    gradient: 'linear-gradient(135deg, #fb923c, #f472b6)'
  }
];

// Sample feedback
const SAMPLE_FEEDBACKS = [
  {
    id: 'fb-1',
    coachName: 'コーチ 山田',
    date: '2026-03-28',
    clientId: 'client-1',
    body: '今週もお疲れ様でした！全体的にバランスの良い食事が取れていますね👏 特に野菜の摂取量が増えているのが素晴らしいです。\n\n来週は、朝食のタンパク質をもう少し増やすことを意識してみましょう。ゆで卵やヨーグルトを追加するだけでOKです！\n\n水分量も安定して8杯以上取れていますね。この調子で続けましょう💪'
  },
  {
    id: 'fb-2',
    coachName: 'コーチ 山田',
    date: '2026-03-21',
    clientId: 'client-1',
    body: '先週のフィードバックを踏まえて、夕食の炭水化物量を減らせていますね。とても良い傾向です！\n\n間食が少し多めだった日もありましたが、選んでいるものはナッツやフルーツなので問題ありません。\n\n排便リズムが少し乱れている日があったので、食物繊維を意識してみてください🥦'
  }
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
