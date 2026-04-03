/* ========================================
   AI Food Predictor (Mock)
   Future: Replace with GPT-4 Vision API
   ======================================== */

const AIPredictor = {
    /**
     * Simulate AI analysis of food photo
     * In production, this would send the image to an API like:
     * - OpenAI GPT-4 Vision
     * - Google Gemini Vision
     * - Custom food recognition model
     *
     * @param {File|Blob} imageFile - The uploaded image
     * @returns {Promise<Object>} Predicted menu and ingredients
     */
    async analyzePhoto(imageFile) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1500 + Math.random() * 1000));

        // Pick a random prediction
        const predictions = AI_PREDICTIONS.patterns;
        const prediction = predictions[Math.floor(Math.random() * predictions.length)];

        return {
            success: true,
            confidence: (0.75 + Math.random() * 0.2).toFixed(2),
            prediction: {
                menu: prediction.menu,
                ingredients: [...prediction.ingredients],
                estimatedCalories: prediction.calories
            }
        };
    },

    /**
     * Get suggestions for partial ingredient input
     * @param {string} query - Partial ingredient name
     * @returns {string[]} Matching ingredient suggestions
     */
    suggestIngredients(query) {
        const allIngredients = [
            '白米', '玄米', 'パン', 'うどん', 'そば', 'パスタ',
            '鶏胸肉', '鶏もも肉', '豚肉', '牛肉', '鮭', 'さば', 'まぐろ', 'えび',
            '豆腐', '納豆', '卵', 'ヨーグルト', 'チーズ', '牛乳',
            'レタス', 'トマト', 'きゅうり', 'ほうれん草', 'キャベツ', 'ブロッコリー',
            'にんじん', '玉ねぎ', 'じゃがいも', '大根', 'もやし',
            'りんご', 'バナナ', 'いちご', 'ブルーベリー', 'みかん',
            'オリーブオイル', '醤油', '味噌', 'マヨネーズ', 'ケチャップ',
            'アーモンド', 'くるみ', 'チアシード', 'グラノーラ'
        ];

        if (!query) return [];
        return allIngredients.filter(ing => ing.includes(query));
    }
};
