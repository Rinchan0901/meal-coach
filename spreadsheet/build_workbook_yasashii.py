"""
副業はじめての人のための やさしい0→1ワークシート（v2 ビギナー版）
=====================================================================
「ビジネスって何？」レベルから伴走する、徹底超初心者向けワークブック。
専門用語ゼロ、Q1→答えだけ式、例3パターン、わからなくてOKメッセージ満載。
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation


# ============================================================
# やさしいカラー（あたたかい・落ち着く）
# ============================================================
COLORS = {
    "bg": "FBF7F2",
    "bg_soft": "F5EFE6",
    "paper": "FFFFFF",
    "text": "3A3530",
    "text_soft": "6B6358",
    "accent": "C28E6E",        # テラコッタ
    "accent_deep": "A06F50",
    "accent_soft": "F2DFD1",
    "pink": "E8B7B0",
    "pink_soft": "FBE9E5",
    "mint": "A8C3B5",
    "mint_soft": "DCE8E1",
    "yellow": "FAF1DC",
    "input": "FFF8E1",
    "line": "E8DFD2",
}

THIN = Border(
    left=Side(style="thin", color=COLORS["line"]),
    right=Side(style="thin", color=COLORS["line"]),
    top=Side(style="thin", color=COLORS["line"]),
    bottom=Side(style="thin", color=COLORS["line"]),
)


# ============================================================
# ヘルパー：書き込み + スタイル
# ============================================================
def title(ws, row, text):
    ws.cell(row=row, column=1, value=text).font = Font(name="Noto Sans JP", size=20, bold=True, color=COLORS["accent_deep"])
    ws.row_dimensions[row].height = 36


def subtitle(ws, row, text, col_span=4):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=col_span)
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = Font(name="Noto Sans JP", size=12, color=COLORS["text_soft"])
    cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[row].height = 24


def section_bar(ws, row, text, color=None, col_span=4):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=col_span)
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = Font(name="Noto Sans JP", size=14, bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor=color or COLORS["accent"])
    cell.alignment = Alignment(vertical="center", horizontal="left", indent=1)
    ws.row_dimensions[row].height = 28


def warm_box(ws, row, text, col_span=4, height=60, fill=None):
    """温かいメッセージボックス（励まし・なぜ・不安ケア）"""
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=col_span)
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = Font(name="Noto Sans JP", size=11, color=COLORS["text"])
    cell.fill = PatternFill("solid", fgColor=fill or COLORS["pink_soft"])
    cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left", indent=1)
    ws.row_dimensions[row].height = height


def question(ws, row, q_text, col_span=4):
    """質問行"""
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=col_span)
    cell = ws.cell(row=row, column=1, value=q_text)
    cell.font = Font(name="Noto Sans JP", size=12, bold=True, color=COLORS["accent_deep"])
    cell.fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
    cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left", indent=1)
    ws.row_dimensions[row].height = 28


def examples(ws, row, examples_list, col_span=4):
    """例3つを薄字で表示"""
    text = "💡 例：" + " ／ ".join(examples_list)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=col_span)
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = Font(name="Noto Sans JP", size=10, italic=True, color="999999")
    cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left", indent=1)
    ws.row_dimensions[row].height = 22


def input_box(ws, row, height=50, col_span=4):
    """入力欄（黄色のセル）"""
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=col_span)
    cell = ws.cell(row=row, column=1, value="")
    cell.fill = PatternFill("solid", fgColor=COLORS["input"])
    cell.border = THIN
    cell.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left", indent=1)
    ws.row_dimensions[row].height = height


def step_row(ws, row, num, text, col_span=4):
    """1ステップずつ書く番号付きリスト"""
    ws.cell(row=row, column=1, value=str(num)).font = Font(size=14, bold=True, color="FFFFFF")
    ws.cell(row=row, column=1).fill = PatternFill("solid", fgColor=COLORS["accent"])
    ws.cell(row=row, column=1).alignment = Alignment(horizontal="center", vertical="center")
    ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=col_span)
    ws.cell(row=row, column=2, value=text).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
    ws.cell(row=row, column=2).font = Font(name="Noto Sans JP", size=11)
    ws.row_dimensions[row].height = 36


def check_row(ws, row, text, col_span=4):
    """チェックボックス行"""
    ws.cell(row=row, column=1, value="☐").font = Font(size=16, color=COLORS["accent"])
    ws.cell(row=row, column=1).alignment = Alignment(horizontal="center", vertical="center")
    ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=col_span)
    ws.cell(row=row, column=2, value=text).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
    ws.cell(row=row, column=2).font = Font(name="Noto Sans JP", size=11)
    ws.row_dimensions[row].height = 26


def gentle(ws, row, text, col_span=4, height=50):
    """『不安かも。でも大丈夫』系メッセージ（ピンク）"""
    warm_box(ws, row, text, col_span, height, fill=COLORS["pink_soft"])


def why(ws, row, text, col_span=4, height=44):
    """『なぜこれをやるの？』（ミント）"""
    warm_box(ws, row, "💚 なぜこれをやるの？　" + text, col_span, height, fill=COLORS["mint_soft"])


def cheer(ws, row, text, col_span=4, height=60):
    """応援メッセージ（黄色）"""
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=col_span)
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = Font(name="Noto Sans JP", size=12, bold=True, italic=True, color=COLORS["accent_deep"])
    cell.fill = PatternFill("solid", fgColor=COLORS["pink_soft"])
    cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws.row_dimensions[row].height = height


def setup_ws(ws, col_widths):
    for col, w in col_widths.items():
        ws.column_dimensions[col].width = w
    ws.sheet_view.showGridLines = False


# ============================================================
# Tab 00: ようこそ（超かんたん使い方）
# ============================================================
def build_welcome(wb):
    ws = wb.create_sheet("00_ようこそ")
    setup_ws(ws, {"A": 6, "B": 24, "C": 65, "D": 20})

    title(ws, 1, "🌿 副業ってよく分からない…そんなあなたへ")
    subtitle(ws, 2, "このシートは、副業を一度もやったことがない人のために作りました。専門用語ゼロ・1日5分でOK・わからなくても進めます。")

    section_bar(ws, 4, "📖 このシートでできること")
    items = [
        "なんとなく副業に興味があるけど、何から始めればいいかわからない人へ。",
        "30日間で「はじめての副業収入」を目指します。",
        "毎日のやることを「1つだけ」決めるので、迷いません。",
        "わからない言葉が出てきたら、いつでも『01_ことば辞典』タブを開いてください。",
        "「ちゃんとやらなきゃ」を捨てて、「できる範囲でOK」で進めます。",
    ]
    r = 5
    for it in items:
        ws.cell(row=r, column=2, value="✓").font = Font(size=12, color=COLORS["mint"], bold=True)
        ws.cell(row=r, column=2).alignment = Alignment(horizontal="center")
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        ws.cell(row=r, column=3, value=it).font = Font(size=11)
        ws.cell(row=r, column=3).alignment = Alignment(wrap_text=True, vertical="center")
        ws.row_dimensions[r].height = 28
        r += 1

    r += 1
    section_bar(ws, r, "🌿 大事なお願い（3つだけ）", color=COLORS["mint"])
    r += 1
    rules = [
        ("①", "1日5分でいい", "5分やったら今日はOK。続けることだけ大事。続かなくなったら『11_こまったとき』タブを開いてください。"),
        ("②", "黄色いセルだけ埋める", "白いセルは説明、黄色いセルがあなたが書く場所。読むだけのページもあります。"),
        ("③", "わからない言葉は飛ばしていい", "あとで『01_ことば辞典』を見れば全部書いてあります。今は止まらないで進む。"),
    ]
    for num, head, body in rules:
        ws.cell(row=r, column=1, value=num).font = Font(size=11, bold=True, color=COLORS["accent"])
        ws.cell(row=r, column=1).alignment = Alignment(horizontal="center", vertical="top")
        ws.cell(row=r, column=2, value=head).font = Font(size=11, bold=True)
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        ws.cell(row=r, column=3, value=body).font = Font(size=11)
        ws.cell(row=r, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 50
        r += 1

    r += 1
    section_bar(ws, r, "📑 タブの順番（上から下へ進むだけ）", color=COLORS["accent_deep"])
    r += 1
    tabs = [
        ("00", "ようこそ", "今ここ。読んだらOK。"),
        ("01", "ことば辞典", "わからない言葉が出てきたらここを見る。"),
        ("02", "30日カレンダー", "毎日ここに戻って、今日のDayを確認。"),
        ("03", "Day 0 はじめての自分メモ", "副業を始める前の気持ちを書く。10分。"),
        ("04", "Day 1-3 こころの準備", "読むだけ。3日間で気持ちを整える。"),
        ("05", "Day 4-7 売るものを見つける", "5つの質問に答えるだけ。何を売るか決まる。"),
        ("06", "Day 8-10 LINE（お知らせを送る場所）", "LINE公式アカウントの設定を1ステップずつ。"),
        ("07", "Day 11-14 BASE（お店）", "ネットでお店を開く。デザイン苦手でも大丈夫。"),
        ("08", "Day 15-21 Threads（お知らせをする）", "1日1つ短文を書くだけ。顔出し不要。"),
        ("09", "Day 18-21 つなぐ", "Threads→LINE→BASEを1本の道にする。"),
        ("10", "Day 22-30 はじめての販売", "やさしくお客さんに声をかける。"),
        ("11", "こまったときの相談室", "やる気が出ない・怖いとき、ここを開く。"),
        ("12", "ひとりごとメモ", "気持ちや気づきを自由に書く場所。"),
    ]
    for num, name, desc in tabs:
        ws.cell(row=r, column=1, value=num).font = Font(size=11, bold=True, color=COLORS["accent"])
        ws.cell(row=r, column=1).alignment = Alignment(horizontal="center")
        ws.cell(row=r, column=2, value=name).font = Font(size=11, bold=True)
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="center")
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        ws.cell(row=r, column=3, value=desc).font = Font(size=11)
        ws.cell(row=r, column=3).alignment = Alignment(wrap_text=True, vertical="center")
        ws.row_dimensions[r].height = 26
        r += 1

    r += 2
    cheer(ws, r, "副業は、特別な人がやるものじゃない。\nこのシートを開いた今のあなたが、もう始まっています。")
    cheer(ws, r+1, "1日5分でいい。今日のぶん、終わったら閉じてOK。\nまた明日、ここで会いましょう🌿", height=60)

    ws.freeze_panes = "A4"


# ============================================================
# Tab 01: ことば辞典
# ============================================================
def build_glossary(wb):
    ws = wb.create_sheet("01_ことば辞典")
    setup_ws(ws, {"A": 6, "B": 24, "C": 65})

    title(ws, 1, "📖 ことば辞典（わからない言葉が出てきたらここ）")
    subtitle(ws, 2, "副業の本やSNSでよく出てくる言葉を、ふつうの日本語にしました。Ctrl+F（Mac は Cmd+F）で検索もできます。", col_span=3)

    headers = ["No", "こんな言葉", "やさしい意味"]
    for i, h in enumerate(headers, start=1):
        cell = ws.cell(row=4, column=i, value=h)
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.fill = PatternFill("solid", fgColor=COLORS["accent_deep"])
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[4].height = 28

    glossary = [
        ("副業", "本業（メインの仕事）以外でやるお仕事。お小遣い稼ぎから始めればOK。"),
        ("0→1（ゼロイチ）", "「初めての売上1件」のこと。0円→1円になる、その瞬間。"),
        ("商品", "あなたが売るもの。PDF・テンプレート・ノウハウ集など、形がなくてもOK。"),
        ("デジタル商品", "PDFや動画など、ネットで送るだけで届けられる商品。在庫なし・送料なし。"),
        ("ペルソナ", "「あなたが届けたいたった1人のお客さん」のこと。むずかしい言葉だけど、ただの『誰に向けて』のこと。"),
        ("コンセプト", "売るものの『一言説明』。「○○な人の△△な悩みを□□で解決する」みたいな1行。"),
        ("ターゲット", "ペルソナとほぼ同じ意味。お客さんになりそうな人のこと。"),
        ("LP（ランディングページ）", "売るための1枚のWebページ。BASEの商品ページもLPの一種。"),
        ("セールスページ", "LPと同じ意味。商品を売るページ。"),
        ("BASE（ベース）", "無料でネットショップが作れるサービス。thebase.com で開く。"),
        ("Threads（スレッズ）", "Instagramが作った文字メインのSNS。Twitter（X）に似てる。"),
        ("公式LINE", "LINEで「お店からのお知らせ」を送れる仕組み。お友達追加してもらってメッセージを配信。"),
        ("LINE公式アカウント", "公式LINEと同じ。正式名称はこっち。"),
        ("リード", "「お客さんになりそうな人」のこと。連絡先（LINEとか）を持っている人。"),
        ("リード管理", "「お客さんになりそうな人」のリストを整える作業。"),
        ("リスト", "公式LINEに登録してくれた人の集まり。"),
        ("集客", "お客さんを集めること。Threadsやインスタで発信して人を呼ぶこと。"),
        ("動線（どうせん）", "お客さんが歩く道。Threads → LINE → BASE のように、つながりを作ること。"),
        ("ファネル", "動線の英語版。漏斗（じょうご）の形にお客さんが流れていくイメージ。"),
        ("ステップ配信", "LINEで『1日後にこのメッセージ、3日後にこのメッセージ』と決めた順に自動で送る仕組み。"),
        ("リッチメニュー", "公式LINEのトーク画面の下に出るボタン。タップでお店に飛ばせる。"),
        ("特商法（とくしょうほう）", "ネット販売で「私はこういう人で、住所はここです」と公表しなきゃいけない法律。"),
        ("バーチャルオフィス", "本当の住所を出したくない人が借りる『書類用の住所』。月990円〜。"),
        ("プロフィール", "SNSの自己紹介欄。あなたが何の人かを書く場所。"),
        ("インプレッション", "投稿が表示された回数。見られた数。"),
        ("リーチ", "投稿を見た人数。"),
        ("エンゲージメント", "いいね・コメント・保存・シェアなど、リアクションされた数。"),
        ("コンバージョン（CV）", "目的が達成された数。販売が完了した数のこと。"),
        ("コピー", "宣伝の文章。キャッチコピーは『つかみの一言』。"),
        ("クロージング", "最後の一押し。『買ってください』のメッセージのこと。"),
        ("オファー", "「これで○○円ですよ」と提案すること。"),
        ("ローンチ", "新商品を売り出すこと。"),
        ("ストーリーローンチ", "数日かけて物語を語りながら商品を売り出すやり方。"),
        ("先行案内", "「もうすぐ販売します」の予告。期待を作る。"),
        ("クーポン", "BASEで使える割引コード。"),
        ("CV率（コンバージョン率）", "ページを見た人のうち、買ってくれた人の割合。"),
        ("PV（ページビュー）", "ページが見られた回数。"),
        ("KPI", "目標数値。フォロワー数や登録数など『追いかける数字』。"),
        ("マネタイズ", "お金にする・稼ぐこと。"),
        ("パッシブインカム", "寝ていても入る収入。デジタル商品なら作れば自動販売。"),
        ("ASP", "アフィリエイト（紹介）でお金がもらえる仕組み。今は気にしなくてOK。"),
        ("プラットフォーム", "ネットの場所。BASE・Threads・LINEもプラットフォーム。"),
        ("コンテンツ", "中身。記事・動画・PDFなど『作ったもの』全般。"),
        ("ブランディング", "「あなたっぽさ」を作ること。色・言葉・雰囲気を統一すること。"),
        ("ニッチ", "せまい市場。特定の人向けに絞ること。"),
        ("マインドセット", "考え方の基本姿勢。『完璧主義はやめよう』みたいな心がけ。"),
        ("先行者利益", "早く始めた人が得する利益。"),
        ("レバレッジ", "てこの原理。1つのものを大勢に届けて稼ぐこと。"),
        ("Canva（キャンバ）", "無料で画像が作れるサービス。canva.com。テンプレ豊富。"),
        ("Notion（ノーション）", "メモ・整理ができる無料アプリ。商品作りに便利。"),
    ]
    r = 5
    for i, (term, defi) in enumerate(glossary, start=1):
        ws.cell(row=r, column=1, value=i).font = Font(size=10, color="999999")
        ws.cell(row=r, column=1).alignment = Alignment(horizontal="center", vertical="top")
        ws.cell(row=r, column=2, value=term).font = Font(bold=True, color=COLORS["accent_deep"], size=11)
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=r, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=r, column=3, value=defi).font = Font(size=11)
        ws.cell(row=r, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 36
        r += 1

    ws.freeze_panes = "A5"


# ============================================================
# Tab 02: 30日カレンダー
# ============================================================
def build_calendar(wb):
    ws = wb.create_sheet("02_30日カレンダー")
    setup_ws(ws, {"A": 7, "B": 12, "C": 50, "D": 12, "E": 30})

    title(ws, 1, "🗺 30日カレンダー（毎日ここに戻る）")
    subtitle(ws, 2, "今日のDayの行を見て、やることを1つやればOK。終わったらD列を「できた」に。", col_span=5)

    headers = ["Day", "日付", "今日のひとこと（やること）", "できた？", "ひとことメモ"]
    for i, h in enumerate(headers, start=1):
        cell = ws.cell(row=4, column=i, value=h)
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.fill = PatternFill("solid", fgColor=COLORS["accent_deep"])
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[4].height = 28

    days = [
        # day, task, color
        (0, "🌱 タブ『03_Day0 はじめての自分メモ』を開いて、気持ちを書く（10分）", COLORS["pink_soft"]),
        (1, "💭 タブ『04_こころの準備』を読む。書かなくていい、読むだけ（5分）", COLORS["pink_soft"]),
        (2, "💭 同じく『04_こころの準備』の続きを読む（5分）", COLORS["pink_soft"]),
        (3, "💭 『04_こころの準備』を読み終える。読書感想は不要（5分）", COLORS["pink_soft"]),
        (4, "🔍 タブ『05_売るものを見つける』のQ1〜Q3を埋める（15分）", COLORS["mint_soft"]),
        (5, "🔍 『05_売るものを見つける』のQ4を埋める（10分）", COLORS["mint_soft"]),
        (6, "🔍 『05_売るものを見つける』のQ5を埋める（10分）", COLORS["mint_soft"]),
        (7, "🔍 『05_売るものを見つける』のまとめ欄を埋める（10分）", COLORS["mint_soft"]),
        (8, "💚 タブ『06_LINE設定』のステップ1〜3を進める（15分）", COLORS["accent_soft"]),
        (9, "💚 『06_LINE設定』のステップ4〜6を進める（20分）", COLORS["accent_soft"]),
        (10, "💚 『06_LINE設定』のステップ7〜9を進める（15分）", COLORS["accent_soft"]),
        (11, "🛍 タブ『07_BASE設定』のステップ1〜3を進める（20分）", COLORS["yellow"]),
        (12, "🛍 『07_BASE設定』のステップ4〜5を進める（15分）", COLORS["yellow"]),
        (13, "🛍 『07_BASE設定』のステップ6（商品ページ作成）を進める（30分）", COLORS["yellow"]),
        (14, "🛍 『07_BASE設定』のステップ7〜8を進める＝公開！（20分）", COLORS["yellow"]),
        (15, "🧵 タブ『08_Threads発信』のプロフィールを書く（15分）", COLORS["bg_soft"]),
        (16, "🧵 『08_Threads発信』の今日の投稿を1つ書く（5分）", COLORS["bg_soft"]),
        (17, "🧵 同じく今日の投稿を1つ書く（5分）", COLORS["bg_soft"]),
        (18, "🧵 投稿1つ＋公式LINEに誘う投稿を1つ（10分）", COLORS["bg_soft"]),
        (19, "🧵 投稿1つ。タブ『09_つなぐ』もチラ見（10分）", COLORS["bg_soft"]),
        (20, "🧵 投稿1つ＋LINE誘導投稿を1つ（10分）", COLORS["bg_soft"]),
        (21, "🧵 タブ『09_つなぐ』のテストを自分でやってみる（20分）", COLORS["bg_soft"]),
        (22, "🚀 タブ『10_はじめての販売』のDay22の予告を書く（15分）", COLORS["pink_soft"]),
        (23, "🚀 Day23の自分の話を書いて投稿（15分）", COLORS["pink_soft"]),
        (24, "🚀 Day24の予告を書く＋クーポンコードを準備（15分）", COLORS["pink_soft"]),
        (25, "🚀 Day25：販売開始！LINEとThreadsで案内する（20分）", COLORS["pink_soft"]),
        (26, "🚀 1to1メッセージを5人に送ってみる（30分）", COLORS["pink_soft"]),
        (27, "🚀 「あと1日です」のリマインドを送る（10分）", COLORS["pink_soft"]),
        (28, "🎉 もし買ってもらえたら、お礼メッセージを書く（5分）", COLORS["pink_soft"]),
        (29, "🌿 投稿を続ける／お休みしてもOK（5分）", COLORS["pink_soft"]),
        (30, "📝 タブ『10_はじめての販売』の30日ふりかえりを書く（15分）", COLORS["pink_soft"]),
    ]

    r = 5
    for d, task, color in days:
        ws.cell(row=r, column=1, value=f"Day {d}").font = Font(bold=True, color=COLORS["accent_deep"], size=11)
        ws.cell(row=r, column=1).alignment = Alignment(horizontal="center", vertical="center")
        ws.cell(row=r, column=2, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
        ws.cell(row=r, column=2).border = THIN
        ws.cell(row=r, column=3, value=task).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.cell(row=r, column=4, value="まだ").alignment = Alignment(horizontal="center", vertical="center")
        ws.cell(row=r, column=4).fill = PatternFill("solid", fgColor=COLORS["input"])
        ws.cell(row=r, column=4).border = THIN
        ws.cell(row=r, column=5, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
        ws.cell(row=r, column=5).border = THIN
        for col in [1, 3]:
            ws.cell(row=r, column=col).fill = PatternFill("solid", fgColor=color)
            ws.cell(row=r, column=col).border = THIN
        ws.row_dimensions[r].height = 32
        r += 1

    dv = DataValidation(type="list", formula1='"まだ,やってる,できた,お休み"', allow_blank=True)
    dv.add(f"D5:D{4+len(days)}")
    ws.add_data_validation(dv)

    ws.freeze_panes = "A5"


# ============================================================
# Tab 03: Day 0 はじめての自分メモ
# ============================================================
def build_day0(wb):
    ws = wb.create_sheet("03_Day0_自分メモ")
    setup_ws(ws, {"A": 6, "B": 70, "C": 6})

    title(ws, 1, "🌱 Day 0：副業を始める前の自分メモ")
    subtitle(ws, 2, "30日後、ここを読み返すために。気持ちを残しておく日です。", col_span=3)

    warm_box(ws, 4, "今日は『書くだけ』。難しいこと何もありません。10分で終わります。", col_span=3, height=36, fill=COLORS["bg_soft"])

    section_bar(ws, 6, "📝 質問に答えるだけ（10問）", col_span=3)

    questions = [
        "Q1. なぜ副業を始めたい？（理由はなんでもOK。お金・自信・趣味・将来の不安…）",
        "Q2. 30日後、自分がどうなっていたら嬉しい？（小さくてOK。「1人にありがとうと言われる」でも◎）",
        "Q3. 今いちばん不安なことは？（『失敗したらどうしよう』など、何でも）",
        "Q4. 今いちばんワクワクすることは？",
        "Q5. 自分が好きなことを3つ書く（仕事と関係なくてOK。コーヒー・散歩・寝かしつけ…）",
        "Q6. 友達やまわりの人から『○○について教えて』とよく聞かれることはある？",
        "Q7. 過去の自分が知りたかった『これさえ知ってたらラクだったのに』ってある？",
        "Q8. 30日のうち、1日にどのくらい時間が取れそう？（5分／15分／30分／1時間）",
        "Q9. 家族や周りに副業のこと、話す？話さない？（話さなくてOKです）",
        "Q10. 今の自分に「がんばってる」と一言かけるなら？",
    ]
    r = 7
    for q in questions:
        question(ws, r, q, col_span=3)
        r += 1
        input_box(ws, r, height=70, col_span=3)
        r += 1

    r += 1
    cheer(ws, r, "ぜんぶ書けなくてOK。1個でも書いたあなたが偉い。\n明日からは、考え方の準備をしていきます🌿", col_span=3)

    ws.freeze_panes = "A4"


# ============================================================
# Tab 04: Day 1-3 こころの準備（読むだけ）
# ============================================================
def build_mindset(wb):
    ws = wb.create_sheet("04_こころの準備")
    setup_ws(ws, {"A": 6, "B": 72, "C": 6})

    title(ws, 1, "💭 Day 1〜3：こころの準備（読むだけでOK）")
    subtitle(ws, 2, "副業を始める前に、これだけ知っておけば大丈夫。書く欄はありません。読み終わったらDay 4へ。", col_span=3)

    section_bar(ws, 4, "Day 1：完璧主義をやめる", col_span=3)
    warm_box(ws, 5, "副業で詰まる人の99%は、『ちゃんと準備してから出したい』と思っているうちに半年経ちます。あなたも『ちゃんと』やりたいタイプですか？", col_span=3, height=44, fill=COLORS["bg_soft"])

    msgs1 = [
        "副業の準備に『100点』はありません。出してみないと、何が必要かわからないからです。",
        "覚えてほしいのは、たったひとつだけ：『今日のぶん、終わらせる』です。",
        "「ちゃんと」の代わりに「とりあえず」を使ってみてください。",
        "例えば「ちゃんと商品を作ろう」→「とりあえず1ページ書いてみる」",
        "「ちゃんと自己紹介を書こう」→「とりあえず3行書いて、明日直す」",
        "未完成のまま出すのは、失礼じゃない。放置するほうが失礼です。",
    ]
    r = 6
    for m in msgs1:
        warm_box(ws, r, "🌿 " + m, col_span=3, height=36, fill=COLORS["paper"])
        r += 1

    r += 1
    section_bar(ws, r, "Day 2：お金をいただくのは申し訳ない？", col_span=3)
    r += 1
    warm_box(ws, r, "「お金を取るのは申し訳ない」と感じる人は、優しい人。でも、その優しさが副業のブレーキになります。", col_span=3, height=44, fill=COLORS["bg_soft"])
    r += 1

    msgs2 = [
        "事実：お金を払って買った人ほど、本気で取り組みます。無料だと適当に消費されます。",
        "つまり、お金をもらうことは『お客さんの本気を引き出す』というサービスでもあります。",
        "値段は、迷ったら 2,980円 から始めてOK。これがいちばん買いやすい金額です。",
        "ガッカリされたらどうしよう？→『ご満足いただけなければ全額返金』と書けば解決。返金される確率は1%以下です。",
        "「お金をいただいてありがとうございます」を、声に出して10回言ってみてください。",
        "「申し訳ない」の反対は『傲慢』じゃなく、『ありがとう』です。",
    ]
    for m in msgs2:
        warm_box(ws, r, "🌿 " + m, col_span=3, height=36, fill=COLORS["paper"])
        r += 1

    r += 1
    section_bar(ws, r, "Day 3：時間がない人ほど続けられる方法", col_span=3)
    r += 1
    warm_box(ws, r, "「1日2時間取れたら本気でやる」と思っている人は、いつまでも始められません。子どもが大きくなれば別の用事が増えるだけ。", col_span=3, height=44, fill=COLORS["bg_soft"])
    r += 1

    msgs3 = [
        "解決策：『1日5分でも進む設計』に変える。このシートはそれで作ってあります。",
        "おすすめ：朝の3分＋夜の2分でもOK。連続してなくていい。",
        "子どもが寝た後の静かな15分が、一番集中できる時間。",
        "週に1日『何もしない日』を最初から決めておく。罪悪感ループに入る前に休む。",
        "続けられる人の共通点は、『同じ時間・同じ場所・同じきっかけ』で作業すること。",
        "例：「子どもが寝たら、ソファでスマホを開いて、Threadsを1つ投稿する」",
    ]
    for m in msgs3:
        warm_box(ws, r, "🌿 " + m, col_span=3, height=36, fill=COLORS["paper"])
        r += 1

    r += 2
    cheer(ws, r, "読むだけのDayは、これで終わりです。\n明日から、いよいよ『売るもの』を見つけにいきます🌿", col_span=3)

    ws.freeze_panes = "A4"


# ============================================================
# Tab 05: Day 4-7 売るものを見つける
# ============================================================
def build_find_product(wb):
    ws = wb.create_sheet("05_売るものを見つける")
    setup_ws(ws, {"A": 6, "B": 30, "C": 60, "D": 8})

    title(ws, 1, "🔍 Day 4〜7：売るものを見つけよう")
    subtitle(ws, 2, "難しく考えなくて大丈夫。あなたの『当たり前』が、誰かの『ありがたい』になります。")

    why(ws, 4, "副業の最初は『何を売るか』が9割。先に決めてしまえば、あとはラクです。")

    # Q1
    section_bar(ws, 6, "Q1. あなたが過去に乗り越えた『悩み』はなに？")
    why(ws, 7, "過去のあなたが解決したことは、今同じ悩みの人にとって宝物です。")
    examples(ws, 8, ["寝かしつけのコツがわからなかった", "お金の管理が下手だった", "在宅ワークで集中できなかった"])
    input_box(ws, 9, height=80)

    # Q2
    section_bar(ws, 11, "Q2. 友達やママ友からよく聞かれることは？")
    why(ws, 12, "聞かれること=他の人も困っていること。商品の種は『誰かの質問』の中にあります。")
    examples(ws, 13, ["離乳食どうしてる？", "おむつ卒業のタイミング教えて", "在宅ワーク何してるの？"])
    input_box(ws, 14, height=80)

    # Q3
    section_bar(ws, 16, "Q3. つい何時間でも調べてしまうテーマは？")
    why(ws, 17, "好きなテーマは続けられる。続けられるテーマは商品になります。")
    examples(ws, 18, ["時短レシピ", "片付け・収納", "家計管理アプリ"])
    input_box(ws, 19, height=80)

    # Q4
    section_bar(ws, 21, "Q4. Q1〜Q3を見て、いちばん『これだ』と感じたテーマは？", color=COLORS["mint"])
    why(ws, 22, "ここで決めるのは『テーマ』だけ。商品の中身はあとで。")
    examples(ws, 23, ["離乳食の段取り", "ワーママの家計管理", "片付けの初級コツ"])
    input_box(ws, 24, height=60)

    # Q5
    section_bar(ws, 26, "Q5. そのテーマで、3ヶ月前のあなたが『3,000円払ってでも欲しい』と思うものは？", color=COLORS["mint"])
    why(ws, 27, "3ヶ月前の自分が買いたいもの=同じ場所にいる人が買いたいもの。")
    examples(ws, 28, ["離乳食4週間ぶんの献立PDF", "ワーママ用の月3万円貯金ワークシート", "10分でできる片付けチェックリスト"])
    input_box(ws, 29, height=80)

    # まとめ
    section_bar(ws, 31, "📝 まとめ：あなたの最初の商品", color=COLORS["accent_deep"])
    matome_fields = [
        ("1. 商品の名前（タイトル）", "例：離乳食ママの月3,000円・15分献立PDF"),
        ("2. 誰のため？（1人だけ思い浮かべる）", "例：1歳の息子をもつ友人のあやかさん"),
        ("3. その人のいちばんの悩みは？", "例：毎日メニューを考えるのに疲れている"),
        ("4. その悩みをどう解決する？", "例：4週間ぶんの献立を渡せば、考えなくて済む"),
        ("5. いくらで売る？（迷ったら2,980円）", "1,980 / 2,980 / 3,980 / 4,980 から1つ"),
        ("6. どんな形で渡す？", "PDF / ワークシート / 動画 / チェックリスト から1つ"),
    ]
    r = 32
    for label, hint in matome_fields:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
        ws.cell(row=r, column=1, value=label).font = Font(bold=True, color=COLORS["accent_deep"], size=11)
        ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        ws.cell(row=r, column=3, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
        ws.cell(row=r, column=3).border = THIN
        ws.row_dimensions[r].height = 38
        r += 1
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        ws.cell(row=r, column=1, value=f"💡{hint}").font = Font(italic=True, size=10, color="999999")
        ws.row_dimensions[r].height = 18
        r += 1

    r += 1
    gentle(ws, r, "💭 「私のテーマじゃダメかも」と思った？\n大丈夫。商品テーマは、あとから何度でも変えられます。今日決めるのは『仮』でOK。", height=60)
    r += 1
    cheer(ws, r+1, "売るものが決まった！\n次はお客さんとつながる場所（LINE）を作ります🌿", height=50)

    ws.freeze_panes = "A4"


# ============================================================
# Tab 06: Day 8-10 LINE
# ============================================================
def build_line(wb):
    ws = wb.create_sheet("06_LINE設定")
    setup_ws(ws, {"A": 6, "B": 30, "C": 60, "D": 8})

    title(ws, 1, "💚 Day 8〜10：LINE（お知らせを届ける場所）を作る")
    subtitle(ws, 2, "公式LINE＝『お店からのお知らせを送れる仕組み』。お友達追加してもらえば、確実にメッセージが届きます。")

    why(ws, 4, "Threadsの投稿は10〜20%しか見られないけど、LINEは60〜80%届きます。だからまずはLINEを先に作るのが鉄則。")

    section_bar(ws, 6, "🎯 ゴール：LINEに『友だち追加してね』と言える状態にする")

    section_bar(ws, 8, "📋 やることリスト（9ステップ）", color=COLORS["accent_deep"])
    steps = [
        "スマホで『LINE Official Account Manager』を検索→アプリをダウンロード（無料）",
        "メールアドレスとパスワードを決めて、新規アカウント作成",
        "アカウント名を決める。例：『あさみ｜離乳食コーチ』のような『名前｜何の人か』形式",
        "プロフィール画像を設定（自撮り顔出しNGなら、Canvaで作ったロゴでOK）",
        "ステータスメッセージ20字以内で『何を配信する人か』を書く",
        "あいさつメッセージを書く（次の項目にテンプレあり、コピペでOK）",
        "登録特典の無料プレゼントPDFを準備（次の項目で詳しく）",
        "自動応答で『特典』というキーワードを設定",
        "自分のスマホでLINEを友だち追加してテスト→ぜんぶ届くか確認",
    ]
    r = 9
    for i, s in enumerate(steps, start=1):
        step_row(ws, r, i, s)
        r += 1

    r += 1
    section_bar(ws, r, "✏️ あいさつメッセージのテンプレ（コピペして埋めるだけ）", color=COLORS["mint"])
    r += 1
    template_text = """はじめまして、{あなたの名前}と申します🌿

このLINEでは、{テーマ}についての
ちょっとしたコツや小ネタを
ゆるっと配信しています。

🎁登録のお礼に、無料プレゼントをご用意しました
↓こちらをタップして「特典」と送ってください
（自動でPDFが届きます）

ご感想やご質問は、
このトークから気軽に送ってくださいね。
1通1通、必ず読んでいます🍃"""
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.cell(row=r, column=1, value=template_text).font = Font(name="Noto Sans Mono", size=11)
    ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=COLORS["yellow"])
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="top", indent=1)
    ws.row_dimensions[r].height = 220
    r += 1

    r += 1
    section_bar(ws, r, "📝 あなたのあいさつメッセージ（書き写して直す）", color=COLORS["accent_deep"])
    r += 1
    input_box(ws, r, height=200)
    r += 1

    r += 1
    section_bar(ws, r, "🎁 無料プレゼント（登録特典）の作り方", color=COLORS["mint"])
    r += 1
    gift_msgs = [
        "登録特典＝『LINE登録してくれた人にあげる無料のもの』。これがあると、登録率が3倍になります。",
        "中身は『商品の縮小版』でOK。例えば、商品が4週間献立PDFなら、特典は7日ぶんのミニ版。",
        "作り方：Canvaで「PDF テンプレート」と検索→好きなテンプレを選ぶ→文字を置き換えるだけ。",
        "保存：Googleドライブにアップロード→『リンクを知っている全員が閲覧可』に設定→URLをコピー。",
        "そのURLを、自動応答メッセージに貼り付ければ完成。",
    ]
    for m in gift_msgs:
        warm_box(ws, r, "🌿 " + m, col_span=4, height=36, fill=COLORS["paper"])
        r += 1

    r += 1
    section_bar(ws, r, "💭 不安かもしれないけど…", color=COLORS["pink"])
    r += 1
    fears = [
        ("「本名を出したくない」", "ニックネームでOK。下の名前だけ（あさみ・まりこ等）が一番信頼されやすい。"),
        ("「リッチメニューって作れるかな」", "最初は文字だけでOK。Canvaで『LINE リッチメニュー』検索→テンプレ無料。15分でできます。"),
        ("「住所を公表したくない」", "バーチャルオフィス（月990円〜）か、特商法の『請求があれば開示』を選択でOK。"),
    ]
    for fear, answer in fears:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        ws.cell(row=r, column=1, value="💭 " + fear).font = Font(bold=True, color="6B2A22")
        ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=COLORS["pink_soft"])
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.row_dimensions[r].height = 22
        r += 1
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        ws.cell(row=r, column=1, value="🌿 " + answer).font = Font(color="2F4A3D")
        ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=COLORS["mint_soft"])
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.row_dimensions[r].height = 36
        r += 1

    r += 2
    cheer(ws, r, "LINE開設、おつかれさま！\n次はお店（BASE）を作ります🌿", height=50)

    ws.freeze_panes = "A4"


# ============================================================
# Tab 07: Day 11-14 BASE
# ============================================================
def build_base(wb):
    ws = wb.create_sheet("07_BASE設定")
    setup_ws(ws, {"A": 6, "B": 30, "C": 60, "D": 8})

    title(ws, 1, "🛍 Day 11〜14：BASE（お店）を作る")
    subtitle(ws, 2, "BASE＝『無料でネットショップが開ける場所』。thebase.com で開設。送料の心配なし。")

    why(ws, 4, "BASEは初期費用も月額も0円。売れた時に手数料が引かれるだけ。デジタル商品なら配送もありません。")

    section_bar(ws, 6, "🎯 ゴール：商品ページを作って『公開』ボタンを押す")

    section_bar(ws, 8, "📋 やることリスト（8ステップ）", color=COLORS["accent_deep"])
    steps = [
        "PCかスマホで『thebase.com』を開く（Google検索でも『BASE』でOK）",
        "緑の『無料でネットショップを開設』ボタンを押す",
        "メールアドレスとパスワードを決める。ショップURL（後から変えられないので慎重に）も決める",
        "テーマ（デザイン）を選ぶ。『Simple』系がデジタル商品向き",
        "管理画面の『Apps』をタップ→次の3つを追加：『デジタルコンテンツApp』『商品レビューApp』『クーポンApp』",
        "『設定』→『特定商取引法に基づく表記』を入力（次の項目に書き方あり）",
        "商品ページを作る（次の項目に7ブロック型あり）。商品画像3枚（Canvaで作成）も用意",
        "自分のスマホで自分のショップを見て、購入動線をテスト→OKなら『公開』ボタン！",
    ]
    r = 9
    for i, s in enumerate(steps, start=1):
        step_row(ws, r, i, s)
        r += 1

    r += 1
    section_bar(ws, r, "✏️ 特商法（とくしょうほう）の書き方", color=COLORS["mint"])
    r += 1
    tokusho_text = """販売事業者：{あなたの本名}
所在地：{自宅住所 または「請求があれば開示」を選択}
電話番号：{電話番号 または「請求があれば開示」を選択}
メールアドレス：{連絡用メール}
販売価格：各商品ページに記載
送料・手数料：デジタル商品のため無料
お支払い方法：クレジットカード／コンビニ決済／銀行振込
お支払い時期：注文時にお支払い
商品の引渡し時期：決済確認後すぐにダウンロードURLをお送りします
返品・交換：デジタル商品の特性上、原則として返品・返金はお受けしておりません。
ただし、商品に不備があった場合はメールにてご連絡ください。"""
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.cell(row=r, column=1, value=tokusho_text).font = Font(name="Noto Sans Mono", size=10)
    ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=COLORS["yellow"])
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="top", indent=1)
    ws.row_dimensions[r].height = 220
    r += 1

    r += 1
    section_bar(ws, r, "📝 商品ページの作り方（7ブロック）", color=COLORS["accent_deep"])
    r += 1
    warm_box(ws, r, "下の7ブロックを順番に書くだけで、売れる商品ページが完成します。下書き欄に書いてからBASEに貼り付ければOK。", col_span=4, height=44, fill=COLORS["bg_soft"])
    r += 1

    blocks = [
        ("ブロック1：最初の3行（つかみ）", "こんにちは、{お客さんの呼びかけ}さん。「{お客さんの本音セリフ}」そんなあなたに届けたいPDFができました。"),
        ("ブロック2：こんな悩みありませんか", "□ 悩み1 □ 悩み2 □ 悩み3 □ 悩み4 □ 悩み5"),
        ("ブロック3：私もそうでした（あなたの過去の話）", "私自身、{過去の悩み}でした。{何を試して何がダメだったか}そこで{気づき}があって、{今の姿}に変わりました。"),
        ("ブロック4：このPDFで得られるもの", "✅ 結果1 ✅ 結果2 ✅ 結果3 ✅ 結果4"),
        ("ブロック5：内容（目次）", "全{X}ページ／PDF形式 ▼目次 P1表紙 P2-3はじめに …"),
        ("ブロック6：価格と保証", "通常価格{X,XXX}円。ご購入後すぐにダウンロードURLが届きます。ご満足いただけなければ全額返金。"),
        ("ブロック7：作者からのメッセージ", "最後までお読みいただきありがとうございます。このPDFは、{あなたの想い}。{ニックネーム}より🌿"),
    ]
    for i, (label, template) in enumerate(blocks, start=1):
        ws.cell(row=r, column=1, value=str(i)).font = Font(size=14, bold=True, color=COLORS["accent"])
        ws.cell(row=r, column=1).alignment = Alignment(horizontal="center", vertical="top")
        ws.cell(row=r, column=2, value=label).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=r, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        ws.cell(row=r, column=3, value=f"📋ひな型：{template}").font = Font(italic=True, size=10, color="888888")
        ws.cell(row=r, column=3).alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.row_dimensions[r].height = 70
        r += 1
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        ws.cell(row=r, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
        ws.cell(row=r, column=1).border = THIN
        ws.row_dimensions[r].height = 100
        r += 1

    r += 1
    section_bar(ws, r, "💭 不安かもしれないけど…", color=COLORS["pink"])
    r += 1
    fears = [
        ("「公開ボタンが押せない」", "押した瞬間、99.99%の人はあなたのお店に気づきません。Threadsで誘導しないかぎり、誰も来ない『静かな部屋』状態。だから安心して押す。"),
        ("「商品画像が作れない」", "Canvaで『商品サムネイル』検索→無料テンプレ→文字を変えるだけ。15分で1枚できます。"),
        ("「自分の本名を出すのが怖い」", "BASEで『請求があれば遅滞なく開示する』を選べます。または月990円のバーチャルオフィスで対応可。"),
    ]
    for fear, answer in fears:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        ws.cell(row=r, column=1, value="💭 " + fear).font = Font(bold=True, color="6B2A22")
        ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=COLORS["pink_soft"])
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.row_dimensions[r].height = 22
        r += 1
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        ws.cell(row=r, column=1, value="🌿 " + answer).font = Font(color="2F4A3D")
        ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=COLORS["mint_soft"])
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.row_dimensions[r].height = 40
        r += 1

    r += 2
    cheer(ws, r, "お店が、できました！\nまだお客さんは来ていなくても大丈夫。\n次はお客さんを呼びにいきます🌿", height=60)

    ws.freeze_panes = "A4"


# ============================================================
# Tab 08: Day 15-21 Threads
# ============================================================
def build_threads(wb):
    ws = wb.create_sheet("08_Threads発信")
    setup_ws(ws, {"A": 6, "B": 14, "C": 16, "D": 50, "E": 12})

    title(ws, 1, "🧵 Day 15〜21：Threads（おしゃべりの場所）を始める")
    subtitle(ws, 2, "Threads＝『文字メインのSNS』。Twitterに似てるけど、もっとやさしい雰囲気。顔出し不要。", col_span=5)

    why(ws, 4, "1日5分の投稿で、お店に来てくれる人を増やせる場所。最初の30投稿は『種まき』、収穫はそのあとです。", col_span=5)

    section_bar(ws, 6, "🎯 ゴール：1日1つ投稿。21日後にLINE登録1人を目指す。", col_span=5)

    section_bar(ws, 8, "📝 プロフィールを書く（Day 15）", color=COLORS["accent_deep"], col_span=5)
    profile_fields = [
        ("名前欄（10〜15文字）", "例：あさみ｜離乳食ラクするコーチ"),
        ("自己紹介1行目：誰のための発信か", "例：離乳食はじめたてママのためのラク献立"),
        ("自己紹介2行目：あなたのこと", "例：元保育士／2児のママ／レシピ歴3年"),
        ("自己紹介3行目：いつ何を発信？", "例：毎日21時にラクできる時短ネタ"),
        ("自己紹介4行目：オファー", "🎁無料プレゼント中→プロフ下のリンクから"),
        ("リンク欄", "公式LINEの友だち追加URL"),
    ]
    r = 9
    for label, hint in profile_fields:
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
        ws.cell(row=r, column=2, value=label).font = Font(bold=True, color=COLORS["accent_deep"], size=11)
        ws.cell(row=r, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=5)
        ws.cell(row=r, column=4, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
        ws.cell(row=r, column=4).border = THIN
        ws.row_dimensions[r].height = 30
        r += 1
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
        ws.cell(row=r, column=2, value=f"💡{hint}").font = Font(italic=True, size=10, color="999999")
        ws.row_dimensions[r].height = 18
        r += 1

    r += 1
    section_bar(ws, r, "✏️ 投稿のかんたんな型（5つ）", color=COLORS["mint"], col_span=5)
    r += 1

    types = [
        ("①気づき型", "{お客さん}が陥りがちな勘違い。\n「{勘違い}」\n→実は{真実}\n私も同じでした。\n今日も{呼びかけ}🌿"),
        ("②失敗談型", "昔の私の大失敗の話。\n{失敗のシーン1〜2行}\n{気持ち1行}\nそこから学んだのは、\n{学び}ということ。"),
        ("③お役立ち型", "{お客さん}が今すぐできる、{テーマ}のコツ3つ。\n①{コツ1}\n②{コツ2}\n③{コツ3}\n試してみてね🍃"),
        ("④質問型", "{お客さん}に質問。\n{シチュエーション}の時、A派？B派？\n私はBで、理由は{1行}。\nコメントで教えて🌿"),
        ("⑤応援型", "今日もがんばってる{お客さん}へ。\n{労いの言葉}\n今日はもう休んでもいい。\n明日もここで会えますように🍃"),
    ]
    for typ, template in types:
        ws.cell(row=r, column=2, value=typ).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=r, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=5)
        ws.cell(row=r, column=3, value=template).font = Font(name="Noto Sans Mono", size=10)
        ws.cell(row=r, column=3).fill = PatternFill("solid", fgColor=COLORS["yellow"])
        ws.cell(row=r, column=3).alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.row_dimensions[r].height = 110
        r += 1

    r += 1
    section_bar(ws, r, "📅 7日ぶんの投稿スケジュール（Day 15〜21）", color=COLORS["accent_deep"], col_span=5)
    r += 1
    headers = ["Day", "曜日", "おすすめの型", "今日の投稿（書いてからコピペ）", "投稿した?"]
    for i, h in enumerate(headers, start=1):
        cell = ws.cell(row=r, column=i, value=h)
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.fill = PatternFill("solid", fgColor=COLORS["accent_deep"])
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[r].height = 26
    r += 1

    schedule = [
        (15, "月", "①気づき型"),
        (16, "火", "③お役立ち型"),
        (17, "水", "②失敗談型"),
        (18, "木", "④質問型"),
        (19, "金", "③お役立ち型"),
        (20, "土", "⑤応援型"),
        (21, "日", "⑤応援型 or 休み"),
    ]
    for d, day, typ in schedule:
        ws.cell(row=r, column=1, value=f"Day {d}").font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=r, column=1).alignment = Alignment(horizontal="center")
        ws.cell(row=r, column=2, value=day).alignment = Alignment(horizontal="center")
        ws.cell(row=r, column=3, value=typ).alignment = Alignment(horizontal="center")
        ws.cell(row=r, column=3).fill = PatternFill("solid", fgColor=COLORS["accent_soft"])
        ws.cell(row=r, column=4, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
        ws.cell(row=r, column=4).border = THIN
        ws.cell(row=r, column=5, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
        ws.cell(row=r, column=5).border = THIN
        ws.row_dimensions[r].height = 90
        r += 1

    r += 1
    section_bar(ws, r, "💭 不安かもしれないけど…", color=COLORS["pink"], col_span=5)
    r += 1
    fears = [
        ("「いいねが0だったら恥ずかしい」", "最初の30投稿は『土壌づくり』。いいね数を見ない。投稿したらアプリを閉じる。31投稿目から伸びた投稿だけ見る。"),
        ("「家族にバレたくない」", "Threadsは別アカウント作成可能。インスタとは別アカで運用すれば、家族には絶対バレません。"),
        ("「批判コメントが怖い」", "フォロワー1,000人未満は批判コメント来ません。届かないので心配ご無用。"),
        ("「投稿が思いつかない」", "型のテンプレに沿って機械的に書く。10分悩んだら下書きに保存して翌日へ。"),
    ]
    for fear, answer in fears:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
        ws.cell(row=r, column=1, value="💭 " + fear).font = Font(bold=True, color="6B2A22")
        ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=COLORS["pink_soft"])
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.row_dimensions[r].height = 22
        r += 1
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
        ws.cell(row=r, column=1, value="🌿 " + answer).font = Font(color="2F4A3D")
        ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=COLORS["mint_soft"])
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.row_dimensions[r].height = 40
        r += 1

    r += 2
    cheer(ws, r, "毎日5分。種をまく日々です。\n結果が出ない日もあるけれど、続けた人だけが30日後の景色を見られます🌿", col_span=5, height=60)

    ws.freeze_panes = "A4"


# ============================================================
# Tab 09: Day 18-21 つなぐ
# ============================================================
def build_funnel(wb):
    ws = wb.create_sheet("09_つなぐ")
    setup_ws(ws, {"A": 6, "B": 30, "C": 60, "D": 8})

    title(ws, 1, "🔗 Day 18〜21：道をつなぐ")
    subtitle(ws, 2, "Threads → LINE → BASE を、1本の道にする日。お客さんが迷わずたどれるか確認します。")

    why(ws, 4, "Threadsに直接BASEのURLを貼っても売れません。LINEで関係を温めてから案内するのが、5〜10倍売れる方法。")

    section_bar(ws, 6, "🎯 ゴール：自分で全部の道を歩いてみて、迷わずたどれるか確認")

    section_bar(ws, 8, "📋 動線テスト（自分で歩いてみる）", color=COLORS["accent_deep"])
    test_items = [
        "別のスマホ or 友達のスマホで、自分のThreadsプロフィールを開く",
        "プロフィールから公式LINEのリンクをタップ→飛べる？",
        "友だち追加→あいさつメッセージが届く？",
        "「特典」と送信→自動応答PDFが届く？",
        "PDFのリンクからダウンロードできる？",
        "PDFの最終ページに、公式LINEのQRコードが入っている？",
        "BASEのショップURLにLINEから飛べる？",
        "（テスト購入）BASEで自分の商品を買ってみる",
        "購入完了メールが届く？",
        "ダウンロードURLからPDFが取れる？",
    ]
    r = 9
    for item in test_items:
        check_row(ws, r, item)
        r += 1

    r += 1
    gentle(ws, r, "💭 「ぜんぶできるかな…」と不安？\n大丈夫。1箇所ずつ確認すれば大丈夫。詰まったら『11_こまったとき』タブを開いてください。", height=60)

    r += 2
    cheer(ws, r+1, "道がつながりました！\nあとはお客さんを呼ぶだけ🌿", height=50)

    ws.freeze_panes = "A4"


# ============================================================
# Tab 10: Day 22-30 はじめての販売
# ============================================================
def build_sales(wb):
    ws = wb.create_sheet("10_はじめての販売")
    setup_ws(ws, {"A": 6, "B": 30, "C": 60, "D": 8})

    title(ws, 1, "🚀 Day 22〜30：はじめてのお客さんに会いに行く")
    subtitle(ws, 2, "ここからの9日間が0→1の本番。やさしくお客さんに声をかけていきます。")

    why(ws, 4, "「明日販売します！」と1回告知しても売れません。4日かけて物語を語って、心の準備をしてもらいます。")

    section_bar(ws, 6, "📅 4日間の物語スケジュール", color=COLORS["accent_deep"])
    schedule = [
        ("Day 22", "予告編：「ある悩みについて、3年かけて見つけた答えがある」と1投稿"),
        ("Day 23", "共感編：過去の自分の失敗談・どん底だった話を投稿"),
        ("Day 24", "前日告知：「明日、その答えをまとめたものを公開します」"),
        ("Day 25", "販売開始！LINEとThreadsで案内＋48時間限定クーポン"),
        ("Day 26", "リマインド：「あと1日です」LINE配信＋1to1メッセージ5人へ"),
        ("Day 27", "クーポン終了告知＋追加の1to1メッセージ"),
    ]
    r = 7
    for day, desc in schedule:
        ws.cell(row=r, column=1, value=day).font = Font(bold=True, color=COLORS["accent_deep"], size=11)
        ws.cell(row=r, column=1).alignment = Alignment(horizontal="center", vertical="center")
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
        ws.cell(row=r, column=2, value=desc).font = Font(size=11)
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.cell(row=r, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.row_dimensions[r].height = 32
        r += 1

    r += 1
    section_bar(ws, r, "✏️ Day 22 予告投稿（書く欄）", color=COLORS["mint"])
    r += 1
    template1 = """3年前の私は、{過去の悩み}

何をやってもダメで、
泣きながら検索していた夜を
今でも覚えています。

そこから3年、
試行錯誤の末にたどり着いた答えを、
今週、はじめて世に出します。

詳細は、公式LINEでお伝えします。
▶︎LINE登録はプロフィールから

あなたの{お客さんの悩み}が、
1日でも早く軽くなりますように🍃"""
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.cell(row=r, column=1, value="📋ひな型：\n" + template1).font = Font(name="Noto Sans Mono", size=10, italic=True, color="888888")
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="top", indent=1)
    ws.row_dimensions[r].height = 240
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.cell(row=r, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
    ws.cell(row=r, column=1).border = THIN
    ws.row_dimensions[r].height = 200
    r += 1

    r += 1
    section_bar(ws, r, "✏️ Day 25 販売開始LINE（書く欄）", color=COLORS["mint"])
    r += 1
    template2 = """{お客さんへの呼びかけ}さん、こんばんは🌿

今日、ついに完成した
{商品名}を公開します。

▼商品ページ
{BASEのURL}

▼{締切日}までの限定特典
✅ LINE登録者さま限定 {YY}円OFFクーポン
   コード：{COUPON_CODE}

▼今すぐ受け取る
{BASEのURL}

ご質問はこのトークから🍃
{ニックネーム}より"""
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.cell(row=r, column=1, value="📋ひな型：\n" + template2).font = Font(name="Noto Sans Mono", size=10, italic=True, color="888888")
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="top", indent=1)
    ws.row_dimensions[r].height = 280
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.cell(row=r, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
    ws.cell(row=r, column=1).border = THIN
    ws.row_dimensions[r].height = 200
    r += 1

    r += 1
    section_bar(ws, r, "💌 1to1メッセージを送る相手リスト（5人）", color=COLORS["accent_deep"])
    r += 1
    warm_box(ws, r, "売り込みじゃなく『気にかけ』。スルーされてOKです。", col_span=4, height=30, fill=COLORS["bg_soft"])
    r += 1
    headers = ["No", "送る相手", "やりとりメモ", "送った?"]
    for i, h in enumerate(headers, start=1):
        cell = ws.cell(row=r, column=i, value=h)
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.fill = PatternFill("solid", fgColor=COLORS["accent_deep"])
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[r].height = 24
    r += 1
    for i in range(1, 6):
        ws.cell(row=r, column=1, value=i).alignment = Alignment(horizontal="center")
        for col in [2, 3, 4]:
            ws.cell(row=r, column=col, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
            ws.cell(row=r, column=col).border = THIN
        ws.row_dimensions[r].height = 28
        r += 1

    r += 1
    section_bar(ws, r, "🎉 もし買ってくれたら：お礼メッセージのひな型", color=COLORS["mint"])
    r += 1
    template3 = """{お名前}さん、

{商品名}をご購入いただき、
本当にありがとうございます🌿

実は、{お名前}さんが
私にとっての初めてのお客様です。

ずっとずっと、{お客さん}の方の
役に立ちたくて、
3年かけて作ってきたものでした。

それを最初に手に取ってくださったこと、
一生忘れません。

PDFのご感想や、
読んで「ここがわからない」など、
このトークで気軽にお聞かせください🍃

{ニックネーム}"""
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.cell(row=r, column=1, value=template3).font = Font(name="Noto Sans Mono", size=10)
    ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=COLORS["yellow"])
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="top", indent=1)
    ws.row_dimensions[r].height = 320
    r += 1

    r += 1
    section_bar(ws, r, "📝 30日ふりかえり（Day 30）", color=COLORS["accent_deep"])
    r += 1
    review = [
        "30日前の自分と比べて、変わったことを5つ書く",
        "Threadsのフォロワー数（30日後）",
        "公式LINEの登録者数（30日後）",
        "BASEの商品ページ閲覧数",
        "販売件数（0でもOK）",
        "売上（0円でもOK）",
        "1番うまくいったこと（1つだけ）",
        "1番うまくいかなかったこと（1つだけ）",
        "次の30日でやりたいこと（3つだけ）",
        "30日前の自分にかける言葉",
    ]
    for q in review:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        ws.cell(row=r, column=1, value="📝 " + q).font = Font(bold=True, color=COLORS["accent_deep"], size=11)
        ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="center", indent=1)
        ws.row_dimensions[r].height = 24
        r += 1
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        ws.cell(row=r, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
        ws.cell(row=r, column=1).border = THIN
        ws.row_dimensions[r].height = 60
        r += 1

    r += 2
    cheer(ws, r, "30日、本当におつかれさまでした。\n0→1ができても・できなくても、\nここまで進んだあなたは、もう昨日とは違います🌿", height=80)

    ws.freeze_panes = "A4"


# ============================================================
# Tab 11: こまったとき相談室
# ============================================================
def build_help(wb):
    ws = wb.create_sheet("11_こまったとき")
    setup_ws(ws, {"A": 6, "B": 35, "C": 60})

    title(ws, 1, "🌿 こまったときの相談室")
    subtitle(ws, 2, "進めなくなったとき、不安になったとき、ここを開いてください。", col_span=3)

    headers = ["カテゴリ", "💭 こんな気持ちのとき", "🌿 こうしてみて"]
    for i, h in enumerate(headers, start=1):
        cell = ws.cell(row=4, column=i, value=h)
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.fill = PatternFill("solid", fgColor=COLORS["accent_deep"])
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[4].height = 28

    helps = [
        ("商品", "「自分のスキルじゃ商品にならない気がする」", "スキルじゃなく『3ヶ月前の自分が困ってたこと』を商品に。3ヶ月分の試行錯誤で十分。"),
        ("商品", "「テーマが10個浮かんで絞れない」", "全部やらない。『友達3人から相談されたテーマ』を1つだけ選ぶ。残り9個は3ヶ月後の候補に。"),
        ("商品", "「同じテーマの人がいて、私が出る意味ある？」", "市場が大きい証拠。あなた個人の物語と言葉が、同じテーマでも違う角度を作る。"),
        ("商品", "「価格をいくらにすればいいか分からない」", "迷ったら2,980円。1,000〜5,000円が0→1の最適価格ゾーン。"),
        ("発信", "「投稿ボタンが押せない」", "誤字を1つ入れて投稿してみる。完璧じゃない投稿を意図的に出すと、次が楽になる。"),
        ("発信", "「フォロワーゼロから誰に向けて？」", "3ヶ月前の自分に向けて書く。1人に向けた言葉が未来の100人に届く。"),
        ("発信", "「批判コメントが怖い」", "フォロワー1,000人未満は来ません。来るなら影響力が育った証拠。今は心配無用。"),
        ("発信", "「いいねが0で恥ずかしい」", "見えていないだけ。投稿後はSNSを開かない。最初の30投稿は土壌づくり。"),
        ("発信", "「自分の投稿、つまらない気がする」", "つまらないと感じるのはあなただけ。下手でいい、本音だけ書く。"),
        ("販売", "「商品ページに来てるのに買われない」", "最初の3行と最後の3行を書き直す。中間は読まれてない。頭と尻尾だけ磨く。"),
        ("販売", "「LINE登録は増えるのに買われない」", "ステップ配信を見直す。商品予告→案内の感情の盛り上がりを作れているか。"),
        ("販売", "「先行案内したのに反応なし」", "1to1メッセージを5人に送る。個別のひとこえがない販売は初心者には難しい。"),
        ("販売", "「価格が高いから売れないのかも」", "値下げは最後の手段。先に得られるもの5個→8個に増やす。"),
        ("販売", "「30日経ったのに0→1できなかった」", "平均は60〜90日。違いは『あと60日続けるか』だけ。Day 5〜21をループ。"),
        ("こころ", "「他のママと比べて落ち込む」", "比較対象は1ヶ月前の自分だけ。他人と比べたい衝動が来たら『1ヶ月前の自分vs今』を書く。"),
        ("こころ", "「私には才能がない気がする」", "才能で0→1する人は1%以下。99%は『淡々と続けただけ』。続ければ達成できる。"),
        ("こころ", "「やる気が出ない日が3日続いてる」", "休んでOK。休む日も計画の一部。週1の『サボる日』を最初から組み込む。"),
        ("こころ", "「成功してる人を見ると苦しくなる」", "その人をミュート/アンフォロー。比較で奮い立つはあなたには毒。"),
        ("こころ", "「もうやめたい」", "2週間完全休止。やめるかは2週間後に決める。即決でやめると後悔する。"),
        ("時間", "「子どもが体調崩して1週間進まなかった」", "1週間ぶん『やらない』を許可。罪悪感が次のさぼりを呼ぶ。再開日だけ決める。"),
        ("時間", "「家事と育児で副業時間ゼロ」", "30分の塊を諦めて、3分×10回に切り替える。スマホ完結タスクから消化。"),
        ("時間", "「やることが多すぎて何から」", "今日のDayだけ見る。それ以外は明日以降。情報遮断が前進の鍵。"),
        ("時間", "「夜は眠すぎて進まない」", "朝にずらす。子どもが起きる15分前。集中力は朝が3倍。"),
        ("時間", "「3週間続けたけど飽きた」", "型を変える。Threadsの5型を1週間ごとにローテ。飽きはサインじゃなく刺激不足。"),
        ("家族", "「夫に話したら反対されそう」", "家族に話すのは初販売の後。実績ゼロでの相談は反対されやすい。結果を持って報告。"),
        ("家族", "「親に『主婦が副業なんて』と言われた」", "説得しない。結果で見せる。納税できる収入になったとき親は黙る。"),
        ("家族", "「ママ友に副業のこと知られたくない」", "Threadsはニックネーム＋顔出しなしOK。インスタと完全分離（別アカ）。"),
        ("家族", "「相談できる人が周りにいない」", "このシートが相談相手。詰まったら『11_こまったとき』を毎回開けばOK。"),
        ("家族", "「友達がもっと稼いでて惨め」", "友達はあなたの過去、SNSは表面を見せている。比較対象が不公平。"),
    ]
    r = 5
    last_cat = None
    for cat, stuck, escape in helps:
        ws.cell(row=r, column=1, value=cat if cat != last_cat else "").font = Font(size=10, italic=True, color="888888")
        ws.cell(row=r, column=1).alignment = Alignment(vertical="top", horizontal="center")
        ws.cell(row=r, column=2, value=stuck).fill = PatternFill("solid", fgColor=COLORS["pink_soft"])
        ws.cell(row=r, column=2).font = Font(bold=True, color="6B2A22", size=11)
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.cell(row=r, column=3, value=escape).fill = PatternFill("solid", fgColor=COLORS["mint_soft"])
        ws.cell(row=r, column=3).font = Font(color="2F4A3D", size=11)
        ws.cell(row=r, column=3).alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.row_dimensions[r].height = 50
        r += 1
        last_cat = cat

    r += 1
    cheer(ws, r, "ぜんぶ『あるある』です。\nあなただけじゃない。明日もまた、ここで会えますように🌿", col_span=3, height=60)

    ws.freeze_panes = "A5"


# ============================================================
# Tab 12: ひとりごとメモ
# ============================================================
def build_diary(wb):
    ws = wb.create_sheet("12_ひとりごとメモ")
    setup_ws(ws, {"A": 12, "B": 70})

    title(ws, 1, "📝 ひとりごとメモ（自由に書く場所）")
    subtitle(ws, 2, "気持ちの吐き出し・気づき・ぐち・なんでも。誰にも見られない、あなただけの場所です。", col_span=2)

    warm_box(ws, 4, "副業を進める中で、心がざわつくことが必ずあります。そんなときはここに書いて、気持ちを整理してください。", col_span=2, height=44, fill=COLORS["bg_soft"])

    headers = ["日付", "今日のひとりごと"]
    for i, h in enumerate(headers, start=1):
        cell = ws.cell(row=6, column=i, value=h)
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.fill = PatternFill("solid", fgColor=COLORS["accent_deep"])
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[6].height = 26

    for r in range(7, 47):  # 40行ぶん
        ws.cell(row=r, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
        ws.cell(row=r, column=1).border = THIN
        ws.cell(row=r, column=1).alignment = Alignment(horizontal="center", vertical="top")
        ws.cell(row=r, column=2, value="").fill = PatternFill("solid", fgColor=COLORS["input"])
        ws.cell(row=r, column=2).border = THIN
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top", indent=1)
        ws.row_dimensions[r].height = 50

    ws.freeze_panes = "A7"


# ============================================================
# メイン
# ============================================================
def main():
    wb = Workbook()
    default = wb["Sheet"]
    wb.remove(default)

    build_welcome(wb)
    build_glossary(wb)
    build_calendar(wb)
    build_day0(wb)
    build_mindset(wb)
    build_find_product(wb)
    build_line(wb)
    build_base(wb)
    build_threads(wb)
    build_funnel(wb)
    build_sales(wb)
    build_help(wb)
    build_diary(wb)

    out = "/home/user/meal-coach/spreadsheet/0to1_workbook_yasashii.xlsx"
    wb.save(out)
    print(f"✅ 保存しました：{out}")
    print(f"   タブ数：{len(wb.sheetnames)}")
    for name in wb.sheetnames:
        print(f"   - {name}")


if __name__ == "__main__":
    main()
