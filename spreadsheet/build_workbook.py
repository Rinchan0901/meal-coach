"""
副業初心者ママ 0→1 ロードマップワークブック
======================================================
1ファイルに講座・ワークシート・進捗管理がすべて入った
「これさえあれば迷わない」スプレッドシート生成スクリプト
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.dimensions import ColumnDimension


# ============================================================
# カラーパレット（くすみ系・ママ向け）
# ============================================================
COLORS = {
    "bg_main": "FBF7F2",       # ベージュ背景
    "bg_soft": "F5EFE6",       # ソフトベージュ
    "accent": "C28E6E",        # テラコッタ
    "accent_deep": "A06F50",   # ダークテラコッタ
    "accent_soft": "F2DFD1",   # 薄テラコッタ
    "pink": "E8B7B0",          # ダスティピンク
    "pink_soft": "FBE9E5",     # 薄ピンク
    "mint": "A8C3B5",          # セージグリーン
    "mint_soft": "DCE8E1",     # 薄ミント
    "warn": "D9A441",          # ウォームイエロー
    "warn_soft": "FAF1DC",     # 薄イエロー
    "input_yellow": "FFF8E1",  # 入力欄
    "white": "FFFFFF",
    "text_dark": "3A3530",
    "line": "E8DFD2",
}


def hex(color):
    return color.lstrip("#")


# ============================================================
# 共通スタイル
# ============================================================
THIN_BORDER = Border(
    left=Side(style="thin", color=COLORS["line"]),
    right=Side(style="thin", color=COLORS["line"]),
    top=Side(style="thin", color=COLORS["line"]),
    bottom=Side(style="thin", color=COLORS["line"]),
)

THICK_BOTTOM = Border(
    bottom=Side(style="medium", color=COLORS["accent"]),
)


def style_title(cell):
    cell.font = Font(name="Noto Sans JP", size=20, bold=True, color=COLORS["accent_deep"])
    cell.alignment = Alignment(vertical="center", horizontal="left")


def style_subtitle(cell):
    cell.font = Font(name="Noto Sans JP", size=13, bold=True, color=COLORS["text_dark"])
    cell.alignment = Alignment(vertical="center", horizontal="left", wrap_text=True)


def style_section(cell, color=None):
    cell.font = Font(name="Noto Sans JP", size=14, bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor=color or COLORS["accent"])
    cell.alignment = Alignment(vertical="center", horizontal="left", indent=1)


def style_label(cell):
    cell.font = Font(name="Noto Sans JP", size=11, bold=True, color=COLORS["accent_deep"])
    cell.alignment = Alignment(vertical="top", horizontal="left", wrap_text=True)
    cell.fill = PatternFill("solid", fgColor=COLORS["bg_soft"])


def style_body(cell):
    cell.font = Font(name="Noto Sans JP", size=11, color=COLORS["text_dark"])
    cell.alignment = Alignment(vertical="top", horizontal="left", wrap_text=True)


def style_input(cell):
    cell.font = Font(name="Noto Sans JP", size=11, color=COLORS["text_dark"])
    cell.alignment = Alignment(vertical="top", horizontal="left", wrap_text=True)
    cell.fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
    cell.border = THIN_BORDER


def style_checklist(cell):
    cell.font = Font(name="Noto Sans JP", size=11, color=COLORS["text_dark"])
    cell.alignment = Alignment(vertical="center", horizontal="left", wrap_text=True)


def style_stuck(cell):
    cell.font = Font(name="Noto Sans JP", size=11, color="6B2A22", bold=True)
    cell.fill = PatternFill("solid", fgColor=COLORS["pink_soft"])
    cell.alignment = Alignment(vertical="top", horizontal="left", wrap_text=True)


def style_escape(cell):
    cell.font = Font(name="Noto Sans JP", size=11, color="2F4A3D")
    cell.fill = PatternFill("solid", fgColor=COLORS["mint_soft"])
    cell.alignment = Alignment(vertical="top", horizontal="left", wrap_text=True)


def style_tip(cell):
    cell.font = Font(name="Noto Sans JP", size=11, color=COLORS["text_dark"])
    cell.fill = PatternFill("solid", fgColor=COLORS["warn_soft"])
    cell.alignment = Alignment(vertical="top", horizontal="left", wrap_text=True)


def style_cheer(cell):
    cell.font = Font(name="Noto Sans JP", size=12, bold=True, italic=True, color=COLORS["accent_deep"])
    cell.fill = PatternFill("solid", fgColor=COLORS["pink_soft"])
    cell.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)


def add_row(ws, row, data, styler=None, height=None):
    """data: list of (col_letter, value) or single value (col A)"""
    if isinstance(data, str):
        cell = ws.cell(row=row, column=1, value=data)
        if styler:
            styler(cell)
        if height:
            ws.row_dimensions[row].height = height
        return
    for col_letter, value in data:
        col_idx = ord(col_letter.upper()) - ord("A") + 1
        cell = ws.cell(row=row, column=col_idx, value=value)
        if styler:
            styler(cell)
    if height:
        ws.row_dimensions[row].height = height


def set_col_widths(ws, widths):
    """widths: dict like {'A': 10, 'B': 30}"""
    for col, w in widths.items():
        ws.column_dimensions[col].width = w


def merge_and_style(ws, range_str, value, styler=None, height=None, color=None):
    ws.merge_cells(range_str)
    first_cell = ws[range_str.split(":")[0]]
    first_cell.value = value
    if styler:
        if color and styler == style_section:
            # Apply section style with custom color
            first_cell.font = Font(name="Noto Sans JP", size=14, bold=True, color="FFFFFF")
            first_cell.fill = PatternFill("solid", fgColor=color)
            first_cell.alignment = Alignment(vertical="center", horizontal="left", indent=1)
        else:
            styler(first_cell)
    if height:
        first_row = int("".join(c for c in range_str.split(":")[0] if c.isdigit()))
        ws.row_dimensions[first_row].height = height


# ============================================================
# Tab 1: 使い方ガイド
# ============================================================
def build_tab_howto(wb):
    ws = wb.create_sheet("00_使い方")
    set_col_widths(ws, {"A": 4, "B": 20, "C": 60, "D": 30})

    add_row(ws, 1, "🌿 副業ママ 0→1 ロードマップワークブック", style_title, height=36)
    add_row(ws, 2, "完璧主義の長子長女ママでも、迷わずゼロイチを達成するための1冊。", style_subtitle, height=24)
    add_row(ws, 3, "")

    merge_and_style(ws, "A4:D4", "📖 このワークブックで手に入るもの", style_section, height=28)

    items = [
        ("✅", "30日間の手順", "1日30分でも進む設計。Day 0〜Day 30まで毎日のやることが決まっています。"),
        ("✅", "講座エッセンス", "各章の要点を凝縮。長子長女が詰まる「7つの罠」と抜け方も全部入り。"),
        ("✅", "ワークシート", "埋めるだけで商品・ペルソナ・LP文・LINE文が完成する空欄テンプレ。"),
        ("✅", "コピペテンプレ50点以上", "Threads投稿5型／LINEあいさつ／販売LP7ブロック／1to1メッセージ。"),
        ("✅", "詰まったとき辞典", "30の「あるある」と抜け方。困ったときに開くお守りページ。"),
        ("✅", "進捗管理＆数字ダッシュボード", "毎日のチェック・KPI記録で、続けられる仕組みに。"),
    ]
    for i, (mark, label, desc) in enumerate(items, start=5):
        ws.cell(row=i, column=1, value=mark).font = Font(size=14)
        ws.cell(row=i, column=2, value=label).font = Font(size=11, bold=True, color=COLORS["accent_deep"])
        ws.cell(row=i, column=3, value=desc).font = Font(size=11, color=COLORS["text_dark"])
        ws.cell(row=i, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[i].height = 30

    add_row(ws, 12, "")
    merge_and_style(ws, "A13:D13", "🌿 進め方の3ルール（必読）", style_section, height=28)

    rules = [
        ("ルール①", "迷ったらタブ「01_30日カレンダー」に戻る", "毎日のやることが書いてあります。今日のDayの行だけ見ればOK。先のDayは見ないこと。"),
        ("ルール②", "ワークシート（黄色のセル）は必ず埋める", "読むだけでは0→1は来ません。埋めて、はじめて自分のビジネスになります。"),
        ("ルール③", "完璧じゃなくていい。今日のぶん、終わらせる", "「ちゃんとやろう」を「今日のぶん終わらせよう」に。これがこのワークブックの最大のルール。"),
    ]
    for i, (num, head, body) in enumerate(rules, start=14):
        ws.cell(row=i, column=1, value=num).font = Font(size=11, bold=True, color=COLORS["accent"])
        ws.cell(row=i, column=2, value=head).font = Font(size=11, bold=True)
        ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True)
        ws.cell(row=i, column=3, value=body).font = Font(size=11)
        ws.cell(row=i, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[i].height = 38

    add_row(ws, 18, "")
    merge_and_style(ws, "A19:D19", "📑 各タブの役割（順番に進める）", style_section, height=28)

    tabs_overview = [
        ("01", "30日カレンダー", "毎日のやることリスト。ここで進捗チェック。"),
        ("02", "Day0-3 マインド準備", "完璧主義→完了主義。罪悪感の正体。続ける時間設計。"),
        ("03", "Day4-7 商品設計", "種掘り3質問・ペルソナ・4タイプ選択・価格決定までやる。"),
        ("04", "Day8-10 公式LINE", "あいさつ・自動応答・タグ設計のテンプレと埋める欄。"),
        ("05", "Day11-14 BASE", "ショップ開設＋7ブロック商品ページのワーク。"),
        ("06", "Day15-21 Threads", "5つの投稿型と毎日の投稿ストック欄。"),
        ("07", "Day18-21 動線設計", "Threads→LINE→BASEの動線テスト。"),
        ("08", "Day22-30 初販売", "4日間ストーリーローンチ＋1to1メッセージ。"),
        ("09", "詰まり辞典", "30の「あるある」と抜け方。困ったとき開く。"),
        ("10", "テンプレ集", "コピペで使える全テンプレ50点超。"),
        ("11", "数字ダッシュボード", "Threads・LINE・BASEのKPIを毎日記録。"),
    ]
    for i, (num, name, desc) in enumerate(tabs_overview, start=20):
        ws.cell(row=i, column=1, value=num).font = Font(size=11, bold=True, color=COLORS["accent"])
        ws.cell(row=i, column=2, value=name).font = Font(size=11, bold=True)
        ws.cell(row=i, column=3, value=desc).font = Font(size=11)
        ws.cell(row=i, column=3).alignment = Alignment(wrap_text=True)
        ws.row_dimensions[i].height = 24

    add_row(ws, 32, "")
    merge_and_style(ws, "A33:D35",
        "30日後、あなたのスマホに「ご購入ありがとうございます」の通知が鳴る。\nその瞬間まで、私はずっとこのワークブックの中にいます。\n— あなたなら、必ず大丈夫です。",
        style_cheer, height=24)
    ws.row_dimensions[33].height = 28
    ws.row_dimensions[34].height = 28
    ws.row_dimensions[35].height = 28

    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"


# ============================================================
# Tab 2: 30日カレンダー
# ============================================================
def build_tab_calendar(wb):
    ws = wb.create_sheet("01_30日カレンダー")
    set_col_widths(ws, {"A": 6, "B": 12, "C": 12, "D": 50, "E": 12, "F": 30})

    add_row(ws, 1, "🗺 30日マスタープラン", style_title, height=36)
    add_row(ws, 2, "毎日このタブに戻ってきて、今日のDayをチェック。完了したらD列を「完了」に変更。", style_subtitle, height=22)
    add_row(ws, 3, "")

    headers = [("A", "Day"), ("B", "日付"), ("C", "章"), ("D", "今日のやること"), ("E", "ステータス"), ("F", "メモ")]
    for col, val in headers:
        cell = ws[f"{col}4"]
        cell.value = val
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.fill = PatternFill("solid", fgColor=COLORS["accent_deep"])
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[4].height = 28

    days = [
        (0, "Ch.00", "🗺 7つの罠を読む / 30日カレンダーに「初販売日(仮)」を書く", COLORS["pink_soft"]),
        (1, "Ch.01", "💭 完璧主義 → 完了主義の書き換え（口グセ1つ書き換える）", COLORS["pink_soft"]),
        (2, "Ch.01", "💭 罪悪感ワーク4問を紙に書く / 「ありがとう」を10回声に出す", COLORS["pink_soft"]),
        (3, "Ch.01", "💭 If-Thenプラン1つ決める / 30日カレンダーに副業30分のブロック", COLORS["pink_soft"]),
        (4, "Ch.02", "🌱 3つの質問で商品の種を3つ書き出す", COLORS["mint_soft"]),
        (5, "Ch.02", "🌱 ペルソナシートを1人ぶん埋める（過去の自分推奨）", COLORS["mint_soft"]),
        (6, "Ch.02", "🌱 4タイプから1つ選ぶ（迷ったらワークシート型）", COLORS["mint_soft"]),
        (7, "Ch.02", "🌱 コンセプト1行・タイトル・価格・表紙(Canva)", COLORS["mint_soft"]),
        (8, "Ch.03", "💚 LINE公式アカウント開設・基本情報・ステータス設定", COLORS["bg_soft"]),
        (9, "Ch.03", "💚 あいさつ作成 / 特典PDF作成 / 自動応答キーワード設定 / リッチメニュー", COLORS["bg_soft"]),
        (10, "Ch.03", "💚 タグ5つ作成 / 配信曜日固定 / 自分でテスト追加", COLORS["bg_soft"]),
        (11, "Ch.04", "🛍 BASEショップ開設 / テーマ選択 / 支払い方法ON / Apps3つ", COLORS["bg_soft"]),
        (12, "Ch.04", "🛍 特商法情報を入力 / 振込口座・本人確認", COLORS["bg_soft"]),
        (13, "Ch.04", "🛍 商品ページ7ブロック作成 / Canvaで画像3枚", COLORS["bg_soft"]),
        (14, "Ch.04", "🛍 デジタルコンテンツとしてPDF登録 / テスト購入 / 公開", COLORS["bg_soft"]),
        (15, "Ch.05", "🧵 Threadsアカウント作成 / プロフィール / アイコン / リンク", COLORS["accent_soft"]),
        (16, "Ch.05", "🧵 5つの型から1つ選んで初投稿 / 同テーマ50人フォロー開始", COLORS["accent_soft"]),
        (17, "Ch.05", "🧵 1日1投稿 / 5件コメント実践", COLORS["accent_soft"]),
        (18, "Ch.05+06", "🔗 LINE誘導投稿1本目 / 動線テスト開始", COLORS["accent_soft"]),
        (19, "Ch.05+06", "🔗 1日1投稿 / コメント / 戻り動線（PDF最終ページのQR）作成", COLORS["accent_soft"]),
        (20, "Ch.05+06", "🔗 LINE誘導投稿2本目 / ステップ配信を組み込む", COLORS["accent_soft"]),
        (21, "Ch.05+06", "🔗 動線テスト完了（家族や友人1人にチェック依頼）", COLORS["accent_soft"]),
        (22, "Ch.07", "🚀 予告投稿（Threads＋LINE）", COLORS["warn_soft"]),
        (23, "Ch.07", "🚀 共感ストーリー投稿", COLORS["warn_soft"]),
        (24, "Ch.07", "🚀 販売前日告知 / クーポンコード作成", COLORS["warn_soft"]),
        (25, "Ch.07", "🚀 販売開始LINE配信 / Threads投稿", COLORS["warn_soft"]),
        (26, "Ch.07", "🚀 リマインドLINE / 1to1メッセージ5人へ", COLORS["warn_soft"]),
        (27, "Ch.07", "🚀 クーポン終了告知 / 1to1メッセージ追加", COLORS["warn_soft"]),
        (28, "Ch.07", "🚀 初購入があれば即お礼メッセージ", COLORS["warn_soft"]),
        (29, "Ch.07", "🚀 1to1メッセージ／Threads継続", COLORS["warn_soft"]),
        (30, "Ch.07", "🚀 振り返りシートを記入 / 次の30日プランを書く", COLORS["warn_soft"]),
    ]

    for i, (day, ch, task, color) in enumerate(days, start=5):
        ws.cell(row=i, column=1, value=f"Day {day}").font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=i, column=1).alignment = Alignment(horizontal="center")
        ws.cell(row=i, column=2, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=i, column=2).border = THIN_BORDER
        ws.cell(row=i, column=3, value=ch).alignment = Alignment(horizontal="center")
        ws.cell(row=i, column=4, value=task)
        ws.cell(row=i, column=4).alignment = Alignment(wrap_text=True, vertical="center")
        for col in ["A", "C", "D"]:
            ws[f"{col}{i}"].fill = PatternFill("solid", fgColor=color)
            ws[f"{col}{i}"].border = THIN_BORDER
        # ステータス（プルダウン）
        ws.cell(row=i, column=5, value="未着手").alignment = Alignment(horizontal="center")
        ws.cell(row=i, column=5).fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=i, column=5).border = THIN_BORDER
        ws.cell(row=i, column=6, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=i, column=6).border = THIN_BORDER
        ws.row_dimensions[i].height = 30

    # ステータスのプルダウン
    from openpyxl.worksheet.datavalidation import DataValidation
    dv = DataValidation(type="list", formula1='"未着手,進行中,完了,休み"', allow_blank=True)
    dv.add(f"E5:E{4+len(days)}")
    ws.add_data_validation(dv)

    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A5"


# ============================================================
# Tab 3: Day0-3 マインド準備
# ============================================================
def build_tab_mindset(wb):
    ws = wb.create_sheet("02_Day0-3_マインド")
    set_col_widths(ws, {"A": 6, "B": 38, "C": 50, "D": 25})

    add_row(ws, 1, "💭 Day 0〜3 マインド準備編", style_title, height=36)
    add_row(ws, 2, "完璧主義を「完了主義」にスライドする3日間。手は動かさなくていい、考え方のOS入れ替えだけ。", style_subtitle, height=22)
    add_row(ws, 3, "")

    # SECTION 1: 7つの罠
    merge_and_style(ws, "A4:D4", "📚 講座：長子長女が詰まる「7つの罠」（Day 0で読む）", style_section, height=26)
    traps = [
        ("罠①「ちゃんと準備してから」病", "全部完璧にしてからスタートしたい。結果、3ヶ月たっても何もない。"),
        ("罠②「お金をいただくのが申し訳ない」病", "値段を決めようとすると手が止まる。「私なんかが…」が口グセ。"),
        ("罠③「全部ひとりでやらなきゃ」病", "聞けない、検索沼、情報集めすぎで動けない。"),
        ("罠④「批判されたらどうしよう」病", "投稿ボタンが押せない。顔出し怖い。"),
        ("罠⑤「他のママと比べてしまう」病", "SNSを見るたびに落ち込む。「私には無理」が一日3回。"),
        ("罠⑥「家族にバレたら反対される」病", "黙って始める罪悪感。応援されない不安。"),
        ("罠⑦「結果が出ないと意味がない」病", "1週間で売れないと「向いてない」と思う。実際は平均60〜90日。"),
    ]
    row = 5
    for trap, desc in traps:
        ws.cell(row=row, column=1, value="✓").font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2, value=trap).font = Font(bold=True, size=11, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=3, value=desc).font = Font(size=11)
        ws.cell(row=row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 36
        row += 1

    row += 1
    # SECTION 2: 完璧主義書き換え表
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク①：完璧主義 → 完了主義 書き換え（Day 1）", style_section, height=26)
    row += 1
    headers = [("A", "No"), ("B", "完璧主義の声（自分が言いがち）", style_label), ("C", "完了主義への書き換え", style_label), ("D", "メモ", style_label)]
    for col, val, *st in headers:
        cell = ws[f"{col}{row}"]
        cell.value = val
        if st:
            st[0](cell)
    ws.row_dimensions[row].height = 24
    row += 1

    examples = [
        ("もっと勉強してから出そう", "今ある知識でDay 7までに1つ作る"),
        ("商品が完璧になってから売ろう", "未完成でも売って、声をもらって直す"),
        ("プロフィールを完璧に作りたい", "3行書いたら公開、3日後に直す"),
    ]
    for i, (perf, done) in enumerate(examples, start=1):
        ws.cell(row=row, column=1, value=f"例{i}").font = Font(color=COLORS["accent"], italic=True)
        ws.cell(row=row, column=2, value=perf).font = Font(italic=True, color="999999")
        ws.cell(row=row, column=3, value=done).font = Font(italic=True, color="999999")
        ws.row_dimensions[row].height = 24
        row += 1
    for i in range(1, 6):
        ws.cell(row=row, column=1, value=i).alignment = Alignment(horizontal="center")
        ws.cell(row=row, column=2, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=2).border = THIN_BORDER
        ws.cell(row=row, column=3, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=3).border = THIN_BORDER
        ws.cell(row=row, column=4, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=4).border = THIN_BORDER
        ws.row_dimensions[row].height = 28
        row += 1

    row += 1
    # SECTION 3: 罪悪感ワーク
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク②：お金の罪悪感ワーク（Day 2）", style_section, height=26)
    row += 1
    questions = [
        "Q1. 「お金をいただくのは申し訳ない」と感じる場面を3つ書く",
        "Q2. その場面で、お客様は本当に「申し訳なく感じてほしい」と思っている？",
        "Q3. もし親友が同じことで悩んでいたら、なんと声をかける？",
        "Q4. その言葉を、自分にも使う。今、自分にかける言葉は？",
    ]
    for q in questions:
        ws.merge_cells(f"A{row}:D{row}")
        ws.cell(row=row, column=1, value=q).font = Font(bold=True, size=11, color=COLORS["accent_deep"])
        ws.cell(row=row, column=1).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        row += 1
        ws.merge_cells(f"A{row}:D{row}")
        ws.cell(row=row, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=1).border = THIN_BORDER
        ws.row_dimensions[row].height = 50
        row += 1

    row += 1
    # SECTION 4: If-Thenプラン
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク③：If-Thenプランニング（Day 3）", style_section, height=26)
    row += 1
    ws.merge_cells(f"A{row}:D{row}")
    ws.cell(row=row, column=1, value="例：もし朝、子どもが起きる前に目が覚めたら、Threadsを1つ投稿する。").font = Font(italic=True, color="999999")
    row += 1

    if_then_headers = [("A", "No"), ("B", "もし___（トリガー）したら"), ("C", "___（アクション）する"), ("D", "頻度の目安")]
    for col, val in if_then_headers:
        cell = ws[f"{col}{row}"]
        cell.value = val
        style_label(cell)
    ws.row_dimensions[row].height = 24
    row += 1
    for i in range(1, 6):
        ws.cell(row=row, column=1, value=i).alignment = Alignment(horizontal="center")
        for col in ["B", "C", "D"]:
            ws.cell(row=row, column=ord(col) - ord("A") + 1, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
            ws.cell(row=row, column=ord(col) - ord("A") + 1).border = THIN_BORDER
        ws.row_dimensions[row].height = 28
        row += 1

    row += 1
    # SECTION 5: チェックリスト
    merge_and_style(ws, f"A{row}:D{row}", "✅ Day 0〜3 完了チェック", style_section, height=26)
    row += 1
    checks = [
        "Day 0：このページをブックマーク",
        "Day 0：30日後の手帳に「初販売日(仮)」を書き込む",
        "Day 1：完璧主義書き換え表を埋めた",
        "Day 2：罪悪感ワーク4問を埋めた",
        "Day 2：「ありがとう」を10回声に出した",
        "Day 3：If-Thenプランを最低1つ決めた",
        "Day 3：30日カレンダーに「副業30分」のブロックを入れた",
    ]
    for c in checks:
        ws.cell(row=row, column=1, value="☐").font = Font(size=14, color=COLORS["accent"])
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="center")
        ws.merge_cells(f"B{row}:D{row}")
        ws.cell(row=row, column=2, value=c)
        ws.row_dimensions[row].height = 24
        row += 1

    row += 1
    ws.merge_cells(f"A{row}:D{row+1}")
    ws.cell(row=row, column=1, value="準備ができたかどうかは、気分ではなくカレンダーが決めます。\n3日たったら、気持ちはまだ準備中でも、Day 4へ進んでください。")
    style_cheer(ws.cell(row=row, column=1))
    ws.row_dimensions[row].height = 28
    ws.row_dimensions[row+1].height = 28

    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"


# ============================================================
# Tab 4: Day4-7 商品設計
# ============================================================
def build_tab_product(wb):
    ws = wb.create_sheet("03_Day4-7_商品")
    set_col_widths(ws, {"A": 6, "B": 30, "C": 65, "D": 25})

    add_row(ws, 1, "🌱 Day 4〜7 商品設計編", style_title, height=36)
    add_row(ws, 2, "万人向けは誰にも刺さらない。たった1人の「過去の自分」に向けて作る4日間。", style_subtitle, height=22)
    add_row(ws, 3, "")

    merge_and_style(ws, "A4:D4", "📚 講座エッセンス", style_section, height=26)
    points = [
        ("商品の種は「3ヶ月前の自分」", "プロ vs アマチュアの二択をやめる。3ヶ月先輩には3ヶ月先輩の市場がある。"),
        ("ペルソナは1人だけ", "「30代女性、子育て中」はNG。知り合いの誰か1人を浮かべる。"),
        ("初心者ママに最強なのはワークシート型", "答えを書かなくていい・顔出し不要・Canvaで作れる。"),
        ("価格は1,980〜4,980円", "迷ったら2,980円。これより安いと価値が低そう、高いと初購入のハードル。"),
        ("ボリューム≠価値", "7ページのワークシートで悩み解決＝3,980円の価値。最大15ページに上限設定。"),
    ]
    row = 5
    for k, v in points:
        ws.cell(row=row, column=2, value=k).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=3, value=v).font = Font(size=11)
        ws.cell(row=row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 36
        row += 1

    row += 1
    merge_and_style(ws, f"A{row}:D{row}", "💭 詰まりポイント＆抜け方", style_section, height=26, color=COLORS["pink"])
    row += 1
    stuck_points = [
        ("「私のスキルじゃ商品にならない」", "スキルじゃなく『3ヶ月前の自分が困ってたこと』を商品に。3ヶ月分の試行錯誤で十分。"),
        ("「30ページPDFを作らなきゃと思うともう無理」", "ボリューム=価値の勘違い。最大15ページ上限。削るほうが商品はシャープに。"),
        ("「2,980円も…ほんとに払ってもらえる？」", "ランチ2回分。3ヶ月の悩みが消えるなら安い。価格の壁は売り手側だけが見ている幻。"),
    ]
    for stuck, escape in stuck_points:
        ws.merge_cells(f"A{row}:D{row}")
        ws.cell(row=row, column=1, value="💭 " + stuck)
        style_stuck(ws.cell(row=row, column=1))
        ws.row_dimensions[row].height = 24
        row += 1
        ws.merge_cells(f"A{row}:D{row}")
        ws.cell(row=row, column=1, value="🌿 " + escape)
        style_escape(ws.cell(row=row, column=1))
        ws.row_dimensions[row].height = 28
        row += 1

    row += 1
    # ワーク①：3つの質問
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク①：商品の種を3つの質問で掘り当てる（Day 4）", style_section, height=26)
    row += 1
    qa = [
        ("Q1", "過去の自分が「これさえ知っていれば3ヶ月助かったのに」と思うことは？", "例：寝かしつけのコツ／離乳食段取り／在宅集中法／お小遣い管理 …"),
        ("Q2", "友達やママ友から、よく相談されることは？", "「○○さんに聞きたかったの」と言われた話題"),
        ("Q3", "「これは詳しい」「気がついたら何時間でも調べてた」テーマは？", "仕事・趣味・育児・家計・健康・美容・人間関係 …"),
    ]
    for qid, question, hint in qa:
        ws.cell(row=row, column=1, value=qid).font = Font(bold=True, color=COLORS["accent"])
        ws.cell(row=row, column=2, value=question).font = Font(bold=True)
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
        ws.cell(row=row, column=3, value=hint).font = Font(italic=True, size=10, color="888888")
        ws.cell(row=row, column=3).alignment = Alignment(wrap_text=True)
        ws.row_dimensions[row].height = 30
        row += 1
        ws.merge_cells(f"A{row}:D{row}")
        ws.cell(row=row, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=1).border = THIN_BORDER
        ws.row_dimensions[row].height = 50
        row += 1

    ws.merge_cells(f"A{row}:D{row}")
    ws.cell(row=row, column=1, value="🌟 3つの交差点が、あなたの最初の商品テーマです。下に書き出してください：")
    style_label(ws.cell(row=row, column=1))
    ws.row_dimensions[row].height = 24
    row += 1
    ws.merge_cells(f"A{row}:D{row}")
    ws.cell(row=row, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
    ws.cell(row=row, column=1).border = THIN_BORDER
    ws.row_dimensions[row].height = 50
    row += 1

    row += 1
    # ワーク②：ペルソナシート
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク②：たった1人のお客様（ペルソナ）（Day 5）", style_section, height=26)
    row += 1
    persona_fields = [
        ("名前（仮名OK・実在モデル推奨）", ""),
        ("年齢・職業", ""),
        ("家族構成", ""),
        ("今いちばん困っていること（言葉そのまま）", "例：「夜泣きで自分の時間がない」"),
        ("それを解決するために今やっていること", ""),
        ("それでも解決しない理由", ""),
        ("「こういう商品があったら絶対買うのに」と言いそうなセリフ", ""),
        ("ペルソナが過去の自分かどうか", "Yes / No"),
    ]
    for field, hint in persona_fields:
        ws.cell(row=row, column=2, value=field).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.merge_cells(f"C{row}:D{row}")
        ws.cell(row=row, column=3, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=3).border = THIN_BORDER
        if hint:
            ws.cell(row=row, column=3).comment = None
        ws.row_dimensions[row].height = 36
        row += 1

    row += 1
    # ワーク③：4タイプ選択
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク③：デジタル商品4タイプから選ぶ（Day 6）", style_section, height=26)
    row += 1
    types_headers = [("A", "選択"), ("B", "タイプ"), ("C", "形式・特徴"), ("D", "価格目安")]
    for col, val in types_headers:
        cell = ws[f"{col}{row}"]
        cell.value = val
        style_label(cell)
    ws.row_dimensions[row].height = 22
    row += 1
    types_data = [
        ("①ノウハウPDF", "10〜30ページ／文章が得意な人向け", "1,980〜3,980円"),
        ("②テンプレ・ワークシート ★おすすめ", "埋めるだけPDF・Canva／顔出し不要", "2,980〜5,980円"),
        ("③ミニ動画講座", "3〜5本×10分／話すのが得意な人", "4,980〜9,800円"),
        ("④チェックリスト集", "1〜5枚／とにかく早く0→1したい人", "980〜1,980円"),
    ]
    for typ, feat, price in types_data:
        ws.cell(row=row, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=1).border = THIN_BORDER
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="center")
        ws.cell(row=row, column=2, value=typ).font = Font(bold=True)
        ws.cell(row=row, column=3, value=feat).alignment = Alignment(wrap_text=True)
        ws.cell(row=row, column=4, value=price).alignment = Alignment(horizontal="center")
        ws.row_dimensions[row].height = 28
        row += 1

    row += 1
    # ワーク④：商品確定
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク④：商品コンセプト・タイトル・価格決定（Day 7）", style_section, height=26)
    row += 1
    final_fields = [
        ("コンセプト1行（誰が・何の悩みを・何で解決）", "「___（誰）が___（状況）で___（悩み）を___（手段）で解決する商品」"),
        ("タイトル（誰に・結果・方法・形式）", "例：「離乳食ママの月3,000円・15分で作る4週間献立PDF」"),
        ("価格（迷ったら 2,980円）", "1,980 / 2,980 / 3,980 / 4,980"),
        ("商品ファイル名（v1.pdfを推奨）", "例：rinyusyoku_4week_v1.pdf"),
    ]
    for label, hint in final_fields:
        ws.cell(row=row, column=2, value=label).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.merge_cells(f"C{row}:D{row}")
        ws.cell(row=row, column=3, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=3).border = THIN_BORDER
        ws.row_dimensions[row].height = 40
        row += 1
        ws.cell(row=row, column=2, value=f"💡ヒント：{hint}").font = Font(italic=True, size=10, color="888888")
        ws.merge_cells(f"B{row}:D{row}")
        ws.row_dimensions[row].height = 20
        row += 1

    row += 1
    # チェックリスト
    merge_and_style(ws, f"A{row}:D{row}", "✅ Day 4〜7 完了チェック", style_section, height=26)
    row += 1
    checks = [
        "Day 4：3つの質問に答えて、商品の種を3つ書き出した",
        "Day 5：ペルソナシートを1人ぶん埋めた",
        "Day 6：4タイプから1つ選んだ",
        "Day 7：コンセプト・タイトル・価格を確定（仮でOK）",
        "Day 7：Canvaで表紙だけ作った",
        "Day 7：商品ファイル名を決めた",
    ]
    for c in checks:
        ws.cell(row=row, column=1, value="☐").font = Font(size=14, color=COLORS["accent"])
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="center")
        ws.merge_cells(f"B{row}:D{row}")
        ws.cell(row=row, column=2, value=c)
        ws.row_dimensions[row].height = 24
        row += 1

    row += 1
    ws.merge_cells(f"A{row}:D{row+1}")
    ws.cell(row=row, column=1, value="完成度30%でOK。残り70%はお客様の声で磨きます。\nここはぐっとこらえて、Day 8へ。")
    style_cheer(ws.cell(row=row, column=1))
    ws.row_dimensions[row].height = 28
    ws.row_dimensions[row+1].height = 28

    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"


# ============================================================
# Tab 5: Day8-10 公式LINE
# ============================================================
def build_tab_line(wb):
    ws = wb.create_sheet("04_Day8-10_LINE")
    set_col_widths(ws, {"A": 6, "B": 30, "C": 65, "D": 25})

    add_row(ws, 1, "💚 Day 8〜10 公式LINE構築編", style_title, height=36)
    add_row(ws, 2, "「届く相手」を育てる箱をつくる3日間。あいさつ・自動応答・タグ設計まで全部。", style_subtitle, height=22)
    add_row(ws, 3, "")

    merge_and_style(ws, "A4:D4", "📚 講座エッセンス", style_section, height=26)
    points = [
        ("公式LINEを使う理由は『到達率』", "Threads/Instagramの到達率5〜20%に対し、公式LINEは60〜80%。0→1の生命線。"),
        ("初心者ママは1媒体集客＋1リード管理＋1販売だけで足りる", "Threads → 公式LINE → BASE。インスタもブログもYouTubeも要らない。"),
        ("あいさつメッセージは短く・親しみやすく・1つの行動を促す", "長文NG。30秒で第一印象が決まる。"),
        ("登録特典(無料プレゼント)は必須", "有料商品の縮小版でOK。販売商品との一貫性を持たせる。"),
        ("タグ設計が運用の心臓部", "#新規 #特典DL済 #興味あり #購入済 #リピーター の5つから始める。"),
        ("配信頻度は週1〜2回・比率は7:2:1", "役立ち情報7：自分の話2：商品案内1。これでブロック率激減。"),
    ]
    row = 5
    for k, v in points:
        ws.cell(row=row, column=2, value=k).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=3, value=v).font = Font(size=11)
        ws.cell(row=row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 36
        row += 1

    row += 1
    merge_and_style(ws, f"A{row}:D{row}", "💭 詰まりポイント＆抜け方", style_section, height=26, color=COLORS["pink"])
    row += 1
    stuck_points = [
        ("「アカウント名、本名にすべき？」", "ニックネーム＋下の名前(あさみ｜離乳食コーチ)が最強。本名は後から判断OK。"),
        ("「リッチメニューのデザイン作れない」", "Canvaで「LINE リッチメニュー」検索→無料テンプレ→色と文字を変えるだけ15分。"),
        ("「住所を出したくない」", "バーチャルオフィス(月990円〜)＋特商法は「請求があれば開示」を選択可。"),
    ]
    for stuck, escape in stuck_points:
        ws.merge_cells(f"A{row}:D{row}")
        ws.cell(row=row, column=1, value="💭 " + stuck)
        style_stuck(ws.cell(row=row, column=1))
        ws.row_dimensions[row].height = 24
        row += 1
        ws.merge_cells(f"A{row}:D{row}")
        ws.cell(row=row, column=1, value="🌿 " + escape)
        style_escape(ws.cell(row=row, column=1))
        ws.row_dimensions[row].height = 28
        row += 1

    row += 1
    # ワーク①：基本情報
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク①：LINE基本情報を埋める（Day 8）", style_section, height=26)
    row += 1
    line_fields = [
        ("アカウント名（ニックネーム｜何の人か）", "例：あさみ｜離乳食コーチ"),
        ("ステータスメッセージ（20字以内）", "例：3,000円で離乳食を回す献立配信中"),
        ("プロフィール画像（用意した？）", "Yes / No"),
        ("カバー画像（用意した？）", "Yes / No"),
        ("登録特典（無料プレゼント）の名前", "例：離乳食7日分ミニ献立PDF"),
        ("登録特典の保存先URL（Googleドライブ等）", ""),
    ]
    for label, hint in line_fields:
        ws.cell(row=row, column=2, value=label).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
        ws.merge_cells(f"C{row}:D{row}")
        ws.cell(row=row, column=3, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=3).border = THIN_BORDER
        ws.row_dimensions[row].height = 32
        row += 1
        if hint:
            ws.cell(row=row, column=2, value=f"💡{hint}").font = Font(italic=True, size=10, color="888888")
            ws.merge_cells(f"B{row}:D{row}")
            ws.row_dimensions[row].height = 18
            row += 1

    row += 1
    # ワーク②：あいさつメッセージ
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク②：あいさつメッセージを書く（Day 9）", style_section, height=26)
    row += 1
    ws.merge_cells(f"A{row}:D{row}")
    ws.cell(row=row, column=1, value="📋 テンプレ：はじめまして、{名前}と申します🌿 / ▼してきたこと（1〜3行）/ このLINEでは{テーマ}を配信 / 🎁登録特典は「{特典}」と送信 / ご質問お気軽に🍃")
    style_tip(ws.cell(row=row, column=1))
    ws.row_dimensions[row].height = 50
    row += 1
    ws.cell(row=row, column=2, value="あなたのあいさつメッセージ（下書き）").font = Font(bold=True, color=COLORS["accent_deep"])
    ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
    ws.merge_cells(f"C{row}:D{row}")
    ws.cell(row=row, column=3, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
    ws.cell(row=row, column=3).border = THIN_BORDER
    ws.row_dimensions[row].height = 200
    row += 1

    row += 1
    # ワーク③：自動応答キーワード
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク③：自動応答キーワード設定（Day 9）", style_section, height=26)
    row += 1
    auto_fields = [
        ("キーワード（複数OK・カンマ区切り）", "例：特典, プレゼント, 受け取る"),
        ("返信メッセージ（特典DL案内）", "🎁プレゼントをお届けします！▼ダウンロードはこちら {URL} ▼使い方のコツ {1〜2行}"),
    ]
    for label, hint in auto_fields:
        ws.cell(row=row, column=2, value=label).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
        ws.merge_cells(f"C{row}:D{row}")
        ws.cell(row=row, column=3, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=3).border = THIN_BORDER
        ws.row_dimensions[row].height = 80
        row += 1
        ws.cell(row=row, column=2, value=f"💡{hint}").font = Font(italic=True, size=10, color="888888")
        ws.merge_cells(f"B{row}:D{row}")
        ws.row_dimensions[row].height = 22
        row += 1

    row += 1
    # ワーク④：タグ設計
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク④：タグを5つ作成（Day 10）", style_section, height=26)
    row += 1
    tag_headers = [("A", "選択"), ("B", "タグ名"), ("C", "つけるタイミング"), ("D", "用途")]
    for col, val in tag_headers:
        cell = ws[f"{col}{row}"]
        cell.value = val
        style_label(cell)
    ws.row_dimensions[row].height = 22
    row += 1
    tags = [
        ("#新規", "友だち追加直後（自動）", "あいさつメッセージ送信対象"),
        ("#特典DL済", "キーワード「特典」を送信時", "本気度高め。商品案内対象。"),
        ("#興味あり", "「気になる」など反応時", "先行案内の最優先対象"),
        ("#購入済", "BASEで購入完了後（手動）", "感想依頼／継続商品案内"),
        ("#リピーター", "2回目以降の購入時", "VIP扱い／お得な案内優先"),
    ]
    for tag, when, use in tags:
        ws.cell(row=row, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=1).border = THIN_BORDER
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="center")
        ws.cell(row=row, column=2, value=tag).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=3, value=when).alignment = Alignment(wrap_text=True)
        ws.cell(row=row, column=4, value=use).alignment = Alignment(wrap_text=True)
        ws.row_dimensions[row].height = 28
        row += 1

    row += 1
    # チェックリスト
    merge_and_style(ws, f"A{row}:D{row}", "✅ Day 8〜10 完了チェック", style_section, height=26)
    row += 1
    checks = [
        "Day 8：LINE公式アカウントを開設",
        "Day 8：プロフィール画像・カバー・ステータス設定",
        "Day 9：あいさつメッセージを作成・登録",
        "Day 9：登録特典PDFを作成・Googleドライブにアップ",
        "Day 9：自動応答キーワード「特典」を設定",
        "Day 9：リッチメニューを作成（文字だけでOK）",
        "Day 10：タグを5つ作成",
        "Day 10：配信スケジュールを週1で固定",
        "Day 10：自分のスマホで友だち追加してテスト",
    ]
    for c in checks:
        ws.cell(row=row, column=1, value="☐").font = Font(size=14, color=COLORS["accent"])
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="center")
        ws.merge_cells(f"B{row}:D{row}")
        ws.cell(row=row, column=2, value=c)
        ws.row_dimensions[row].height = 24
        row += 1

    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"


# ============================================================
# Tab 6: Day11-14 BASE
# ============================================================
def build_tab_base(wb):
    ws = wb.create_sheet("05_Day11-14_BASE")
    set_col_widths(ws, {"A": 6, "B": 28, "C": 67, "D": 25})

    add_row(ws, 1, "🛍 Day 11〜14 BASE構築編", style_title, height=36)
    add_row(ws, 2, "売れる商品ページの型と、公開までの全手順。3日でレジが完成します。", style_subtitle, height=22)
    add_row(ws, 3, "")

    merge_and_style(ws, "A4:D4", "📚 講座エッセンス", style_section, height=26)
    points = [
        ("BASE = 初期費用無料・月額無料・売れた時だけ手数料", "デジタル商品もBASEだけで配信完結（デジタルコンテンツApp）。"),
        ("必須Apps3つ", "デジタルコンテンツApp／商品レビューApp／クーポンApp"),
        ("特商法は絶対スキップ不可", "「請求があれば開示」を選択可。バーチャルオフィスでも対応可。"),
        ("商品ページは7ブロック構成", "①キャッチ ②悩み ③共感ストーリー ④得られるもの ⑤目次 ⑥価格と保証 ⑦作者メッセージ"),
        ("商品画像は最低3枚（最大20枚）", "①表紙メイン ②中身スクショ ③こんな人におすすめリスト"),
        ("公開ボタンは怖くない", "Threadsで誘導しないかぎり、誰も見にこない。安心して押す。"),
    ]
    row = 5
    for k, v in points:
        ws.cell(row=row, column=2, value=k).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=3, value=v).font = Font(size=11)
        ws.cell(row=row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 36
        row += 1

    row += 1
    # ワーク①：基本情報
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク①：BASE基本情報（Day 11-12）", style_section, height=26)
    row += 1
    base_fields = [
        ("ショップURL（後から変更不可・慎重に）", "例：asami-rinyusyoku（→.base.shop）"),
        ("ショップ名（公式LINEと揃える）", "例：あさみの離乳食ノート"),
        ("テーマ選択（Simple系推奨）", ""),
        ("販売事業者（本名）", ""),
        ("所在地（自宅 or バーチャルオフィス）", "「請求があれば開示」を選択も可"),
        ("連絡用メールアドレス", ""),
        ("振込口座（登録済？）", "Yes / No"),
        ("本人確認書類（アップロード済？）", "Yes / No"),
    ]
    for label, hint in base_fields:
        ws.cell(row=row, column=2, value=label).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
        ws.merge_cells(f"C{row}:D{row}")
        ws.cell(row=row, column=3, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=3).border = THIN_BORDER
        ws.row_dimensions[row].height = 30
        row += 1
        if hint:
            ws.cell(row=row, column=2, value=f"💡{hint}").font = Font(italic=True, size=10, color="888888")
            ws.merge_cells(f"B{row}:D{row}")
            ws.row_dimensions[row].height = 18
            row += 1

    row += 1
    # ワーク②：商品ページ7ブロック
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク②：商品ページ7ブロックを書く（Day 13）", style_section, height=26)
    row += 1
    blocks = [
        ("ブロック1：キャッチコピー（最初の3行）", "こんにちは、{ペルソナ}さん。「{本音セリフ}」そんなあなたに届けたい商品ができました。"),
        ("ブロック2：こんな悩みありませんか（5つ）", "□ 悩み1 / □ 悩み2 / □ 悩み3 / □ 悩み4 / □ 悩み5"),
        ("ブロック3：私もそうでした（共感ストーリー）", "私自身、{過去}でした。{エピソード3〜5行}そこで{気づき}。今は{現在の姿}。"),
        ("ブロック4：このPDFで得られるもの（5〜8個）", "✅ 結果1 ✅ 結果2 ✅ 結果3 ✅ 結果4"),
        ("ブロック5：内容（目次の見せ方）", "全{X}ページ／PDF形式 ▼目次 P1 表紙 P2-3 はじめに …"),
        ("ブロック6：価格と保証", "通常価格{X,XXX}円 ▼ご購入後すぐにダウンロード ▼ご満足いただけなければ{保証}"),
        ("ブロック7：作者からのメッセージ", "最後までお読みいただきありがとうございます。このPDFは{想い}。{ニックネーム}より🌿"),
    ]
    for i, (label, template) in enumerate(blocks, start=1):
        ws.cell(row=row, column=1, value=str(i)).font = Font(bold=True, color=COLORS["accent"])
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="center")
        ws.cell(row=row, column=2, value=label).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=3, value=f"📋{template}").font = Font(italic=True, size=10, color="888888")
        ws.cell(row=row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 60
        row += 1
        ws.merge_cells(f"A{row}:D{row}")
        ws.cell(row=row, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=1).border = THIN_BORDER
        ws.row_dimensions[row].height = 80
        row += 1

    row += 1
    # チェックリスト
    merge_and_style(ws, f"A{row}:D{row}", "✅ Day 11〜14 完了チェック", style_section, height=26)
    row += 1
    checks = [
        "Day 11：BASEショップ開設・テーマ選択・支払い方法ON",
        "Day 11：3つのApps追加（デジタル/レビュー/クーポン）",
        "Day 12：特商法情報を入力",
        "Day 12：振込口座・本人確認書類アップロード",
        "Day 13：商品ページを7ブロックで作成",
        "Day 13：商品サムネイル3枚（Canva）",
        "Day 14：デジタルコンテンツとしてPDF登録",
        "Day 14：自分でテスト購入して動作確認",
        "Day 14：公開！ショップURLを公式LINEに反映",
    ]
    for c in checks:
        ws.cell(row=row, column=1, value="☐").font = Font(size=14, color=COLORS["accent"])
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="center")
        ws.merge_cells(f"B{row}:D{row}")
        ws.cell(row=row, column=2, value=c)
        ws.row_dimensions[row].height = 24
        row += 1

    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"


# ============================================================
# Tab 7: Day15-21 Threads
# ============================================================
def build_tab_threads(wb):
    ws = wb.create_sheet("06_Day15-21_Threads")
    set_col_widths(ws, {"A": 6, "B": 16, "C": 20, "D": 60, "E": 12})

    add_row(ws, 1, "🧵 Day 15〜21 Threads集客編", style_title, height=36)
    add_row(ws, 2, "1日10分の発信でファンが育つ。プロフィール → 5つの投稿型 → LINE誘導の7日間。", style_subtitle, height=22)
    add_row(ws, 3, "")

    merge_and_style(ws, "A4:E4", "📚 講座エッセンス", style_section, height=26)
    points = [
        ("Threadsが最強な理由", "テキスト主体・アルゴリズムが優しい・1投稿1〜2分で書ける。"),
        ("プロフィールは3秒で伝わる構成", "名前欄＋150字以内＋公式LINEリンク。長文NG。"),
        ("5つの投稿型でローテ", "①気づき型 ②失敗談型 ③ノウハウ型 ④問いかけ型 ⑤応援型"),
        ("初期に絶対やる行動", "①50人フォロー ②具体感想コメント1日5件 ③1日1投稿×3週間 ④反応分析 ⑤自分のリプ補足"),
        ("最強の投稿時間", "夜21:00〜23:00（寝かしつけ後の自分時間）が最もブレずに続く。"),
        ("最初の30投稿は反応を見ない", "投稿したらアプリを閉じる。31投稿目から伸びた型だけ静かに見る。"),
    ]
    row = 5
    for k, v in points:
        ws.cell(row=row, column=2, value=k).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(f"C{row}:E{row}")
        ws.cell(row=row, column=3, value=v).font = Font(size=11)
        ws.cell(row=row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 32
        row += 1

    row += 1
    # ワーク①：プロフィール
    merge_and_style(ws, f"A{row}:E{row}", "📝 ワーク①：Threadsプロフィールを作る（Day 15）", style_section, height=26)
    row += 1
    profile_fields = [
        ("名前欄（ニックネーム｜何の人か・10〜15字）", "例：あさみ｜離乳食ラクするコーチ"),
        ("自己紹介1行目（誰のための発信か）", "例：離乳食はじめたてママのためのラク献立"),
        ("自己紹介2行目（実績や経験）", "例：元管理栄養士／2児育児中／レシピ歴3年"),
        ("自己紹介3行目（発信内容）", "例：毎日21時に時短献立を配信中"),
        ("自己紹介4行目（オファー）", "🎁無料プレゼント受付中→プロフ下のリンク"),
        ("リンク欄（公式LINEのURL）", ""),
    ]
    for label, hint in profile_fields:
        ws.merge_cells(f"B{row}:C{row}")
        ws.cell(row=row, column=2, value=label).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
        ws.merge_cells(f"D{row}:E{row}")
        ws.cell(row=row, column=4, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=4).border = THIN_BORDER
        ws.row_dimensions[row].height = 30
        row += 1
        if hint:
            ws.merge_cells(f"B{row}:E{row}")
            ws.cell(row=row, column=2, value=f"💡{hint}").font = Font(italic=True, size=10, color="888888")
            ws.row_dimensions[row].height = 18
            row += 1

    row += 1
    # ワーク②：投稿ストック
    merge_and_style(ws, f"A{row}:E{row}", "📝 ワーク②：投稿ストック（30投稿ぶん／毎日埋める）", style_section, height=26)
    row += 1
    headers = [("A", "Day"), ("B", "投稿日"), ("C", "型"), ("D", "投稿文（本文）"), ("E", "投稿済?")]
    for col, val in headers:
        cell = ws[f"{col}{row}"]
        cell.value = val
        style_label(cell)
        cell.alignment = Alignment(horizontal="center")
    ws.row_dimensions[row].height = 24
    row += 1

    type_rotation = ["気づき型", "ノウハウ型", "失敗談型", "問いかけ型", "ノウハウ型", "応援型", "応援型"]
    for d in range(15, 31):
        type_idx = (d - 15) % 7
        ws.cell(row=row, column=1, value=f"Day{d}").alignment = Alignment(horizontal="center")
        ws.cell(row=row, column=1).font = Font(bold=True, color=COLORS["accent"])
        ws.cell(row=row, column=2, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=2).border = THIN_BORDER
        ws.cell(row=row, column=3, value=type_rotation[type_idx]).fill = PatternFill("solid", fgColor=COLORS["accent_soft"])
        ws.cell(row=row, column=3).alignment = Alignment(horizontal="center")
        ws.cell(row=row, column=4, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=4).border = THIN_BORDER
        ws.cell(row=row, column=5, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=5).border = THIN_BORDER
        ws.row_dimensions[row].height = 60
        row += 1

    from openpyxl.worksheet.datavalidation import DataValidation
    dv2 = DataValidation(type="list", formula1='"気づき型,失敗談型,ノウハウ型,問いかけ型,応援型,LINE誘導"', allow_blank=True)
    dv2.add(f"C{row-16}:C{row-1}")
    ws.add_data_validation(dv2)

    dv3 = DataValidation(type="list", formula1='"☐,✅"', allow_blank=True)
    dv3.add(f"E{row-16}:E{row-1}")
    ws.add_data_validation(dv3)

    row += 1
    # チェックリスト
    merge_and_style(ws, f"A{row}:E{row}", "✅ Day 15〜21 完了チェック", style_section, height=26)
    row += 1
    checks = [
        "Day 15：Threadsアカウント作成（副業用に新規）",
        "Day 15：プロフィール記入完了・アイコン設定",
        "Day 15：プロフィールリンクに公式LINEのURL",
        "Day 16：5つの型から1つ選んで初投稿",
        "Day 16〜21：1日1投稿（曜日ローテ）",
        "Day 17：同テーマの発信者を50人フォロー",
        "Day 17〜21：毎日5件のコメント実践",
        "Day 18〜21：週2本のLINE誘導投稿を組み込む",
        "Day 21：投稿数20以上・LINE登録1人以上",
    ]
    for c in checks:
        ws.cell(row=row, column=1, value="☐").font = Font(size=14, color=COLORS["accent"])
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="center")
        ws.merge_cells(f"B{row}:E{row}")
        ws.cell(row=row, column=2, value=c)
        ws.row_dimensions[row].height = 24
        row += 1

    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"


# ============================================================
# Tab 8: Day18-21 動線設計
# ============================================================
def build_tab_funnel(wb):
    ws = wb.create_sheet("07_Day18-21_動線")
    set_col_widths(ws, {"A": 6, "B": 30, "C": 65, "D": 25})

    add_row(ws, 1, "🔗 Day 18〜21 動線設計編", style_title, height=36)
    add_row(ws, 2, "Threads → LINE → BASE → LINE戻り。1本の道として接続するフェーズ。", style_subtitle, height=22)
    add_row(ws, 3, "")

    merge_and_style(ws, "A4:D4", "📚 講座エッセンス", style_section, height=26)
    points = [
        ("動線は必ず3段（Threads→LINE→BASE）", "Threadsに直接BASEのURLを貼ると売れない。LINEで温める段階を必ず挟む。"),
        ("LINEステップ配信は0/1/3/7/10/14日", "あいさつ→特典使い方→経験ストーリー→アンケート→予告→販売案内"),
        ("BASE→LINE戻り動線でリピーター化", "PDF最終ページにQR／購入完了メールにLINE URL／商品ページ末尾に登録特典"),
        ("「購入済」キーワードでタグ自動付与", "VIPリストとして次商品の優先案内。"),
    ]
    row = 5
    for k, v in points:
        ws.cell(row=row, column=2, value=k).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=3, value=v).font = Font(size=11)
        ws.cell(row=row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 36
        row += 1

    row += 1
    # 動線テスト
    merge_and_style(ws, f"A{row}:D{row}", "🧪 ワーク：動線テストチェック（Day 21）", style_section, height=26)
    row += 1
    ws.merge_cells(f"A{row}:D{row}")
    ws.cell(row=row, column=1, value="自分が初めての人になりきって、迷わずたどれるかチェック。1箇所でも「あれ？」があればそこをお客様も詰まる。家族や友人1人に頼んでフィードバックをもらうのも◎。")
    style_tip(ws.cell(row=row, column=1))
    ws.row_dimensions[row].height = 50
    row += 1
    test_items = [
        "別アカウントor友人のスマホで自分のThreadsプロフを見る",
        "プロフから公式LINEに飛べる",
        "友だち追加→あいさつメッセージが届く",
        "「特典」と送って自動応答PDFが届く",
        "PDFをダウンロードできる",
        "PDF最終ページのQRが読み取れる",
        "BASEのショップURLにLINEから飛べる",
        "BASEで購入したら、購入完了メールにLINEのURLがある",
        "商品PDFの最終ページから公式LINEに戻れる",
    ]
    for t in test_items:
        ws.cell(row=row, column=1, value="☐").font = Font(size=14, color=COLORS["accent"])
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="center")
        ws.merge_cells(f"B{row}:D{row}")
        ws.cell(row=row, column=2, value=t)
        ws.row_dimensions[row].height = 24
        row += 1

    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"


# ============================================================
# Tab 9: Day22-30 初販売
# ============================================================
def build_tab_launch(wb):
    ws = wb.create_sheet("08_Day22-30_販売")
    set_col_widths(ws, {"A": 6, "B": 28, "C": 67, "D": 25})

    add_row(ws, 1, "🚀 Day 22〜30 初販売編", style_title, height=36)
    add_row(ws, 2, "0→1の本番。4日間ストーリーローンチ＋1to1メッセージで、最初の1人に届ける。", style_subtitle, height=22)
    add_row(ws, 3, "")

    merge_and_style(ws, "A4:D4", "📚 講座エッセンス", style_section, height=26)
    points = [
        ("人は知らない人からは買わない", "「買わない理由」5個（不安・効果不明・恥・必要性・他社比較）を1つずつ崩す。"),
        ("4日間のストーリーローンチ", "予告 → 共感ストーリー → 翌日告知 → 販売開始＋クーポン"),
        ("1to1メッセージは売り込みじゃなく『気にかけ』", "嫌がられる確率1%以下。「スルーOK」を必ず添える。"),
        ("初販売の通知が来たらまず深呼吸", "5分自分のために時間を取ってから返信。一生忘れない人になる。"),
        ("お客様の声をもらう最適タイミング", "購入2〜4週間後。「2-3行・匿名OK・ご無理なく」とハードルを下げる。"),
        ("30日で売れなくても焦らない", "平均は60〜90日。やめずにCh.5〜7をループするだけで達成できる。"),
    ]
    row = 5
    for k, v in points:
        ws.cell(row=row, column=2, value=k).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=3, value=v).font = Font(size=11)
        ws.cell(row=row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 36
        row += 1

    row += 1
    # ワーク①：4日間スケジュール
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク①：4日間ストーリーローンチを書く（Day 22-25）", style_section, height=26)
    row += 1
    launch_days = [
        ("Day 22 予告編（Threads + LINE）", "3年前の私は、{過去の悩み}…そこからたどり着いた答えを、今週世に出します。詳細は公式LINEで。"),
        ("Day 23 共感ストーリー編", "昨日の続き。3年前のどん底だった話。{エピソード5〜7行}{転機}でぜんぶ変わりました。明日公開。"),
        ("Day 24 翌日告知編", "明日、その答えをまとめたものを公開します。LINE登録者さま限定クーポンあり。"),
        ("Day 25 販売開始LINE", "今日ついに完成した{商品名}を公開します。▼商品ページ {URL} ▼{締切}までの限定特典 …"),
    ]
    for label, template in launch_days:
        ws.cell(row=row, column=2, value=label).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=3, value=f"📋{template}").font = Font(italic=True, size=10, color="888888")
        ws.cell(row=row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 60
        row += 1
        ws.merge_cells(f"A{row}:D{row}")
        ws.cell(row=row, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=1).border = THIN_BORDER
        ws.row_dimensions[row].height = 100
        row += 1

    row += 1
    # ワーク②：1to1メッセージ送信リスト
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク②：1to1メッセージ送信リスト（Day 26-27）", style_section, height=26)
    row += 1
    one2one_headers = [("A", "No"), ("B", "送る相手（ニックネーム）"), ("C", "過去のやりとり・反応メモ"), ("D", "送信済?")]
    for col, val in one2one_headers:
        cell = ws[f"{col}{row}"]
        cell.value = val
        style_label(cell)
        cell.alignment = Alignment(horizontal="center")
    ws.row_dimensions[row].height = 24
    row += 1
    for i in range(1, 11):
        ws.cell(row=row, column=1, value=i).alignment = Alignment(horizontal="center")
        for col in ["B", "C", "D"]:
            ws[f"{col}{row}"].fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
            ws[f"{col}{row}"].border = THIN_BORDER
        ws.row_dimensions[row].height = 28
        row += 1

    row += 1
    # 30日振り返り
    merge_and_style(ws, f"A{row}:D{row}", "📝 ワーク③：30日後の振り返り（Day 30）", style_section, height=26)
    row += 1
    review_fields = [
        ("1. 30日前の自分と比べて、変わったこと（5つ）", ""),
        ("2-1. Threadsフォロワー数", ""),
        ("2-2. 公式LINE登録者数", ""),
        ("2-3. 商品ページ閲覧数", ""),
        ("2-4. 販売数", ""),
        ("2-5. 売上", ""),
        ("3. 1番うまくいったこと（1つだけ）", ""),
        ("4. 1番うまくいかなかったこと（1つだけ）", ""),
        ("5. 次の30日でやること（3つ）", ""),
    ]
    for label, hint in review_fields:
        ws.cell(row=row, column=2, value=label).font = Font(bold=True, color=COLORS["accent_deep"])
        ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
        ws.merge_cells(f"C{row}:D{row}")
        ws.cell(row=row, column=3, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=row, column=3).border = THIN_BORDER
        ws.row_dimensions[row].height = 50
        row += 1

    row += 2
    ws.merge_cells(f"A{row}:D{row+1}")
    ws.cell(row=row, column=1, value="この本のロードマップは、ここで終わります。\nでも、あなたのビジネスはここから始まります。")
    style_cheer(ws.cell(row=row, column=1))
    ws.row_dimensions[row].height = 28
    ws.row_dimensions[row+1].height = 28

    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"


# ============================================================
# Tab 10: 詰まり辞典
# ============================================================
def build_tab_stuck_dict(wb):
    ws = wb.create_sheet("09_詰まり辞典")
    set_col_widths(ws, {"A": 6, "B": 18, "C": 36, "D": 60})

    add_row(ws, 1, "🌿 詰まったとき辞典：30のあるあると抜け方", style_title, height=36)
    add_row(ws, 2, "順番に読まなくてOK。困ったときだけ開くお守りページ。", style_subtitle, height=22)
    add_row(ws, 3, "")

    headers = [("A", "ID"), ("B", "カテゴリ"), ("C", "💭 詰まりポイント"), ("D", "🌿 抜け方")]
    for col, val in headers:
        cell = ws[f"{col}4"]
        cell.value = val
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.fill = PatternFill("solid", fgColor=COLORS["accent_deep"])
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[4].height = 28

    entries = [
        ("A-1", "商品が決まらない", "自分のスキルじゃ商品にならない気がする", "スキルじゃなく『3ヶ月前の自分が困ってたこと』を商品に。3ヶ月分の試行錯誤で十分。"),
        ("A-2", "商品が決まらない", "テーマが10個浮かんで絞れない", "全部やらない。『友達3人から相談されたテーマ』を1つだけ選ぶ。残り9個は3ヶ月後候補に。"),
        ("A-3", "商品が決まらない", "同じテーマの人が多くて、私が出る意味ある？", "市場が大きい証拠。あなた個人の物語と言葉が、同じテーマでも違う角度を作る。"),
        ("A-4", "商品が決まらない", "中身を作っているうちに自信がなくなる", "目次だけ完成させてから中身。中身で止まる人は目次から作り直す。"),
        ("A-5", "商品が決まらない", "価格をいくらにすればいいか分からない", "迷ったら2,980円。1,000〜5,000円が0→1の最適価格。"),
        ("B-1", "発信が怖い", "投稿ボタンが押せない", "誤字を1つ含めて投稿する。完璧じゃない投稿を意図的に出すと次が楽になる。"),
        ("B-2", "発信が怖い", "フォロワー0で誰に向けて？", "3ヶ月前の自分に向けて書く。1人に向けた言葉が未来の100人に届く。"),
        ("B-3", "発信が怖い", "批判コメントが来たらどうしよう", "フォロワー1,000人未満は批判コメント来ない。来るなら影響力が育った証拠。"),
        ("B-4", "発信が怖い", "いいねが0で恥ずかしい", "いいね0は見えていないだけ。投稿後はSNSを開かない。最初の30投稿は土壌づくり。"),
        ("B-5", "発信が怖い", "自分の投稿、つまらない気がする", "つまらないと感じるのはあなただけ。下手でいい、本音だけ書く。"),
        ("C-1", "売れない", "商品ページに来てるのに買われない", "最初の3行と最後の3行を書き直す。中間は読まれてない。頭と尻尾だけ磨く。"),
        ("C-2", "売れない", "LINE登録は増えるのに買われない", "ステップ配信が機能してない。Ch.6の14日ステップを見直す。"),
        ("C-3", "売れない", "先行案内したのに反応なし", "1to1メッセージを5人に送る。個別のひとこえがない販売は初心者ママに成立しない。"),
        ("C-4", "売れない", "価格が高いから売れない、安くしたい", "値下げは最後の手段。先に得られるもの5個→8個に増やす。仮の声を1つ載せる(自分の感想可)。"),
        ("C-5", "売れない", "30日経ったのに0→1できなかった", "平均は60〜90日。違いは能力じゃなく『あと60日続けるか』だけ。Ch.5〜7をループ。"),
        ("D-1", "メンタル", "他のママと比べて落ち込む", "比較対象は1ヶ月前の自分だけ。他人と比べたい衝動が来たら『1ヶ月前の自分vs今』を書く。"),
        ("D-2", "メンタル", "私には才能がない気がする", "才能で0→1する人は1%以下。99%は『淡々と続けただけ』。続ければ達成できる。"),
        ("D-3", "メンタル", "やる気が出ない日が3日続いてる", "休んでOK。休む日も計画の一部。週1の『サボる日』を最初から組み込む。"),
        ("D-4", "メンタル", "成功してる人を見ると苦しくなる", "その人をミュート/アンフォロー。比較で奮い立つは長子長女には毒。"),
        ("D-5", "メンタル", "もうやめたい", "2週間完全休止。やめるかは2週間後に決める。即決でやめると後悔する。"),
        ("E-1", "時間・継続", "子どもが体調崩して1週間進まなかった", "1週間ぶん『やらない』を許可。罪悪感が次のさぼりを呼ぶ。再開日だけ決める。"),
        ("E-2", "時間・継続", "家事と育児で副業時間ゼロ", "スマホ完結タスクから消化。30分の塊を諦めて、3分×10回に切り替える。"),
        ("E-3", "時間・継続", "やることが多すぎて何から", "ロードマップの『今日のDay』だけ見る。それ以外は明日以降。情報遮断が前進の鍵。"),
        ("E-4", "時間・継続", "夜は眠すぎて進まない", "朝にずらす。子どもが起きる15分前に起きる。長子長女の集中力は朝が3倍。"),
        ("E-5", "時間・継続", "3週間続けたけど飽きた", "型を変える。Threadsの5型を1週間ごとにローテ。飽きはサインじゃなく刺激不足。"),
        ("F-1", "家族・人間関係", "夫に話したら反対されそう", "家族に話すのは初販売の後。実績ゼロでの相談は反対されやすい。結果を持って報告。"),
        ("F-2", "家族・人間関係", "親に『主婦が副業なんて』と言われた", "説得しない。結果で見せる。納税できる収入になったとき親は黙る。"),
        ("F-3", "家族・人間関係", "ママ友に副業のこと知られたくない", "Threadsはニックネーム＋顔出しなしOK。Instagramと完全分離(別アカ)。"),
        ("F-4", "家族・人間関係", "相談できる人が周りにいない", "このロードマップは相談しなくても進める設計。SNS上に同志を作る。"),
        ("F-5", "家族・人間関係", "友達がもっと稼いでいて惨め", "友達はあなたの過去、SNSは表面を見せている。比較対象が不公平。"),
    ]
    row = 5
    last_cat = None
    for eid, cat, stuck, escape in entries:
        ws.cell(row=row, column=1, value=eid).font = Font(bold=True, color=COLORS["accent"])
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="center", vertical="top")
        ws.cell(row=row, column=2, value=cat if cat != last_cat else "").font = Font(size=10, italic=True, color="888888")
        ws.cell(row=row, column=2).alignment = Alignment(vertical="top")
        ws.cell(row=row, column=3, value=stuck).fill = PatternFill("solid", fgColor=COLORS["pink_soft"])
        ws.cell(row=row, column=3).font = Font(bold=True, color="6B2A22")
        ws.cell(row=row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=4, value=escape).fill = PatternFill("solid", fgColor=COLORS["mint_soft"])
        ws.cell(row=row, column=4).font = Font(color="2F4A3D")
        ws.cell(row=row, column=4).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 50
        row += 1
        last_cat = cat

    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A5"


# ============================================================
# Tab 11: テンプレ集
# ============================================================
def build_tab_templates(wb):
    ws = wb.create_sheet("10_テンプレ集")
    set_col_widths(ws, {"A": 6, "B": 25, "C": 90})

    add_row(ws, 1, "📝 テンプレ集（コピペで使える50点超）", style_title, height=36)
    add_row(ws, 2, "C列の文章を選択 → コピー → SNSやLINEにそのまま貼り付け。{ }内を自分の言葉に置き換えるだけ。", style_subtitle, height=22)
    add_row(ws, 3, "")

    headers = [("A", "No"), ("B", "用途"), ("C", "テンプレ")]
    for col, val in headers:
        cell = ws[f"{col}4"]
        cell.value = val
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.fill = PatternFill("solid", fgColor=COLORS["accent_deep"])
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[4].height = 28

    templates = [
        # LINE系
        ("LINE", "あいさつメッセージ", "はじめまして、{名前}と申します🌿\n\n▼してきたこと\n・{実績や経験を1〜3行}\n・{ペルソナの悩みに共感する一言}\n\nこのLINEでは、{商品テーマ}についてのちょっとしたコツや、{価値ある何か}をゆるっと配信しています。\n\n🎁登録いただいた方限定プレゼント\n「{特典キーワード}」と送ってください\n\nご感想や質問は、このトークから気軽に送ってくださいね。\n1通1通、必ず読んでいます🍃"),
        ("LINE", "自動応答（特典）", "🎁プレゼントをお届けします！\n\n▼ダウンロードはこちら\n{URL}\n\n▼使い方のコツ\n{1〜2行のミニアドバイス}\n\nこのまま気軽にご質問など送ってくださいね🌿"),
        ("LINE", "Day 1ステップ配信", "{ペルソナ}さん、こんばんは🌿\n昨日の特典PDFは届きましたか？\n\nもしまだの方は『特典』と送ってくださいね。\n\n今日は、特典の使い方のコツをひとつ。\n{コツ1〜2行}\n\n明日もお送りしますね🍃"),
        ("LINE", "Day 3 経験ストーリー", "今日は私の話を少しだけ。\n\n3年前、私は{過去のどん底}でした。\n{エピソード3〜5行}\n\nそのとき、{転機}があって、すべてが変わりました。\n\n同じ悩みを抱える方の力になれたら嬉しいです🌿"),
        ("LINE", "Day 7 アンケート", "{ペルソナ}さん、いつもありがとうございます🌿\n\nもし良ければ、教えてほしいことがあります。\n\n今いちばん困っていることって、なんですか？\n\n一言でも大丈夫です。お返事お待ちしています🍃"),
        ("LINE", "Day 10 商品予告", "{ペルソナ}さんに、来週ご報告があります。\n\nずっと作ってきた{商品名}が、ついに完成します。\n\n公開日：{日付} {時刻}\n登録者さま限定クーポンも準備中です🎁\n\n楽しみに待っていてくださいね🍃"),
        ("LINE", "Day 14/25 販売開始", "{ペルソナ}さん、こんばんは🌿\n\n今日、ついに完成した{商品名}を公開します。\n\n▼商品ページ\n{URL}\n\n▼{締切日}までの限定特典\n✅ 公式LINE登録者さま限定 {YY}円OFFクーポン\n   コード：{COUPON_CODE}\n\n▼今すぐ受け取る\n{URL}\n\nご質問はこのトークから🍃"),
        ("LINE", "リマインドLINE", "{ペルソナ}さん、リマインドです🍃\n\n限定クーポン、今夜{時刻}までです。\n コード：{COUPON_CODE}\n\nもしご検討中なら、ぜひこのチャンスを🌿\n\n▼商品ページ\n{URL}"),
        ("LINE", "1to1メッセージ", "{お名前}さん、こんにちは🌿\n\n突然のメッセージ、失礼します。\n\nいつもLINEを読んでくださっているのを見るたびに、ありがとうございます。\n\nもしご迷惑でなければ、1つだけお伝えしたくて。\n\n今回の{商品名}、{お名前}さんの{過去のお悩み}を思い浮かべながら作りました。\n\nクーポンの締切が明日{XX}時です。ご検討の参考まで🍃\n\nスルーしていただいて大丈夫です。\n\n{ニックネーム}"),
        ("LINE", "初購入お礼", "{お名前}さん、\n\n{商品名}をご購入いただき、本当にありがとうございます🌿\n\n実は、{お名前}さんのご購入が、私にとっての初めてのご購入です。\nずっとずっと、{ペルソナ}の方の役に立ちたくて、3年かけて作ってきたものでした。\n\nそれを最初に手に取ってくださったこと、一生忘れません。\n\nPDFの感想など、このトークで気軽にお聞かせください🍃\n\n{ニックネーム}"),
        ("LINE", "お客様の声依頼", "{お名前}さん、こんにちは🌿\n\n{商品名}をご購入いただいてから{X}週間が経ちましたが、お試しいただけましたか？\n\nもし少しでもお役に立てたところがあれば、2〜3行のご感想をこのトークでお聞かせいただけたら嬉しいです。\n\n▼お聞きしたいこと（ご無理のない範囲で）\n①購入前のお悩み\n②使ってみての変化\n③同じ悩みの方におすすめする一言\n\n匿名OK、ご無理なくお返事くださいね🍃"),
        # Threads系
        ("Threads", "プロフィール構成", "【名前欄】{ニックネーム}｜{何の人か}（10〜15字）\n\n【自己紹介】\n1行目：{ペルソナ}のための{テーマ}\n2行目：元{職業}／{年数}育児中／{経験}\n3行目：{頻度}で{内容}を発信中\n4行目：🎁無料プレゼント受付中→プロフ下のリンク\n\n【リンク欄】公式LINEのURL"),
        ("Threads", "型①気づき型", "{ペルソナ}が陥りがちな勘違い。\n\n「{勘違い}」\n→ 実は{真実}\n\n私も{過去の自分}でした。\n{気づきのきっかけ1〜2行}\n\n今日も{呼びかけ}🌿"),
        ("Threads", "型②失敗談型", "昔の私の大失敗の話。\n\n{失敗のシーン1〜2行}\n{その時の気持ち1行}\n\nその経験から学んだのは、{学び}ということ。\n\n同じ失敗、しなくていい人が1人でも増えますように。"),
        ("Threads", "型③ノウハウ型", "{ペルソナ}が今すぐできる、{テーマ}のコツ3つ。\n\n①{コツ1}\n②{コツ2}\n③{コツ3}\n\n特に③は{補足}。\n試してみてね🍃"),
        ("Threads", "型④問いかけ型", "{ペルソナ}に質問。\n\n{シチュエーション}の時、あなたはどっち派？\n\nA. {選択肢A}\nB. {選択肢B}\n\n私はBで、理由は{1行}。\nコメントで教えて🌿"),
        ("Threads", "型⑤応援型", "今日もがんばってる{ペルソナ}のあなたへ。\n\n{労いの言葉1〜2行}\n{具体的なシーン}\n\n{呼びかけ：今日はもう休もう／○○していい etc.}\n\n明日もここで会えますように🍃"),
        ("Threads", "LINE誘導投稿", "{ペルソナ}向けに、{特典の名前}を作りました🎁\n\n中身は、\n✅ {特典の中身1}\n✅ {特典の中身2}\n✅ {特典の中身3}\n\nいま公式LINEで無料プレゼント中です。\n\n▶︎{ニックネーム}のLINE\nプロフのリンクから\n\nあなたの{悩み}が少しでもラクになりますように🍃"),
        ("Threads", "固定投稿（自己紹介）", "こんにちは、{ニックネーム}です🌿\n\n{ペルソナ}向けに、{テーマ}についての発信をしています。\n\n▼自己紹介\n・{経歴・実績1行}\n・{経歴・実績1行}\n・{今の活動}\n\n▼公式LINEで無料プレゼント中🎁\n{特典名}（{形式・ボリューム}）\n「{特典}」と送るとお届けします。\n\n▶︎LINE登録はプロフのリンクから\n\n明日も、ここで会えますように🍃"),
        ("Threads", "予告編（Day 22）", "3年前の私は、{ペルソナと同じ過去の悩み}\n\n何をやってもダメで、泣きながら検索していた夜を今でも覚えています。\n\nそこから3年、試行錯誤の末にたどり着いた答えを、今週、はじめて世に出します。\n\n詳細は、公式LINEでお伝えします。\n▶︎LINE登録はプロフィールから\n（{締切日}までの限定特典あり）\n\nあなたの{悩み}が、1日でも早く軽くなりますように🍃"),
        ("Threads", "共感編（Day 23）", "昨日の続きです。\n\n3年前の私が、本当にどん底だった話。\n\n{エピソード5〜7行：具体的なシーン／その時の気持ち／何を試して何がダメだったか}\n\n「もうダメかもしれない」と思った夜があった。\n\nでも、ある日{転機の出来事}で、ぜんぶが変わりました。\n\nその変化のすべてを、明日、公開します。"),
        # BASE / 商品ページ系
        ("BASE", "商品ページ7ブロック", "━━━━━━━━━━━━\n【ブロック1：キャッチコピー】\nこんにちは、{ペルソナ}さん。\n「{ペルソナの本音セリフ}」\nそんなあなたに届けたいPDFができました。\n\n【ブロック2：こんな悩みありませんか】\n□ {悩み1} □ {悩み2} □ {悩み3} □ {悩み4} □ {悩み5}\n1つでも当てはまる方は、ぜひ続きをお読みください。\n\n【ブロック3：私もそうでした】\n私自身、{過去}でした。\n{エピソード3〜5行}\n\n【ブロック4：得られるもの】\n✅ {結果1} ✅ {結果2} ✅ {結果3} ✅ {結果4}\n\n【ブロック5：内容】\n全{X}ページ／PDF形式\n▼目次 P1 表紙 P2-3 はじめに …\n\n【ブロック6：価格と保証】\n通常価格 {X,XXX}円\n▼ご購入後すぐにダウンロード\n▼ご満足いただけなければ{保証}\n\n【ブロック7：作者からのメッセージ】\n最後までお読みいただきありがとうございます。\nこのPDFは、{あなたの想い}\n{ニックネーム}より🌿\n━━━━━━━━━━━━"),
        ("BASE", "特商法 標準テンプレ", "販売事業者：{あなたの本名}\n所在地：{自宅 or バーチャルオフィス}（請求があれば開示）\n電話番号：（請求があれば開示）\nメールアドレス：{連絡用メール}\n販売価格：各商品ページに記載\n送料・手数料：デジタル商品のため無料\nお支払い方法：クレカ・コンビニ・銀行振込・キャリア決済\nお支払い時期：注文時\n商品の引渡し時期：決済確認後すぐにダウンロードURLをお送りします\n返品・交換：デジタル商品の特性上、原則として返品・返金はお受けしておりません。商品に不備があった場合はメールにてご連絡ください。"),
        ("BASE", "PDF最終ページ（戻り動線）", "━━━━━━━━━━━━\nご購入ありがとうございました🌿\n\n▼ご質問・ご感想は公式LINEへ\n{QRコード}\n\n▼公式LINE登録者さま限定の追加特典\n・{特典1}\n・{特典2}\n（LINEで「購入済」と送ると受け取れます）\n\nあなたの{ペルソナの願い}を\nここから一緒に育てていけたら嬉しいです。\n{ニックネーム}🍃\n━━━━━━━━━━━━"),
    ]
    row = 5
    for cat, use, tmpl in templates:
        ws.cell(row=row, column=1, value=cat).font = Font(bold=True, color=COLORS["accent_deep"], size=10)
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="center", vertical="top")
        ws.cell(row=row, column=1).fill = PatternFill("solid", fgColor=COLORS["accent_soft"])
        ws.cell(row=row, column=2, value=use).font = Font(bold=True, color=COLORS["text_dark"])
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=COLORS["bg_soft"])
        ws.cell(row=row, column=3, value=tmpl).font = Font(name="Noto Sans Mono", size=10)
        ws.cell(row=row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row, column=3).border = THIN_BORDER
        # Row height based on length
        line_count = tmpl.count("\n") + 1
        ws.row_dimensions[row].height = max(40, min(line_count * 16, 350))
        row += 1

    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A5"


# ============================================================
# Tab 12: 数字ダッシュボード
# ============================================================
def build_tab_dashboard(wb):
    ws = wb.create_sheet("11_数字ダッシュボード")
    set_col_widths(ws, {"A": 12, "B": 12, "C": 14, "D": 14, "E": 14, "F": 12, "G": 30})

    add_row(ws, 1, "📊 数字ダッシュボード", style_title, height=36)
    add_row(ws, 2, "毎日（または週1回）数字を記録。比較は1ヶ月前の自分とだけ。", style_subtitle, height=22)
    add_row(ws, 3, "")

    # サマリー行（数式）
    merge_and_style(ws, "A4:G4", "📈 30日間サマリー（自動計算）", style_section, height=26, color=COLORS["mint"])
    summary_headers = [("A", "Threadsフォロワー"), ("B", "LINE登録者"), ("C", "商品PV"), ("D", "販売件数"), ("E", "売上(円)"), ("F", "投稿数"), ("G", "")]
    for col, val in summary_headers:
        cell = ws[f"{col}5"]
        cell.value = val
        style_label(cell)
        cell.alignment = Alignment(horizontal="center")
    ws.row_dimensions[5].height = 24

    # 集計行
    ws["A6"] = "=MAX(A9:A38)"
    ws["B6"] = "=MAX(B9:B38)"
    ws["C6"] = "=MAX(C9:C38)"
    ws["D6"] = "=SUM(D9:D38)"
    ws["E6"] = "=SUM(E9:E38)"
    ws["F6"] = "=SUM(F9:F38)"
    for col in "ABCDEF":
        ws[f"{col}6"].font = Font(bold=True, size=14, color=COLORS["accent_deep"])
        ws[f"{col}6"].alignment = Alignment(horizontal="center")
        ws[f"{col}6"].fill = PatternFill("solid", fgColor=COLORS["mint_soft"])
    ws.row_dimensions[6].height = 32

    add_row(ws, 7, "")

    # 日次記録
    merge_and_style(ws, "A8:G8", "📅 日次記録（毎日入力）", style_section, height=26, color=COLORS["accent"])
    daily_headers = [
        ("A", "日付"),
        ("B", "Day"),
        ("C", "Threadsフォロワー"),
        ("D", "LINE登録"),
        ("E", "商品PV"),
        ("F", "販売件数"),
        ("G", "売上(円)"),
    ]

    # ↑ Wait - I have 7 columns but my widths only set A-G. Let me reorder
    # actually let me redo the column widths to match the header
    set_col_widths(ws, {"A": 12, "B": 8, "C": 16, "D": 14, "E": 12, "F": 12, "G": 14, "H": 12, "I": 30})
    daily_headers = [
        ("A", "日付"),
        ("B", "Day"),
        ("C", "Threadsフォロワー"),
        ("D", "LINE登録"),
        ("E", "商品PV"),
        ("F", "販売件数"),
        ("G", "売上(円)"),
        ("H", "投稿数"),
        ("I", "メモ"),
    ]
    for col, val in daily_headers:
        ws.cell(row=9, column=ord(col) - ord("A") + 1, value=val).font = Font(bold=True, color="FFFFFF")
        ws.cell(row=9, column=ord(col) - ord("A") + 1).fill = PatternFill("solid", fgColor=COLORS["accent_deep"])
        ws.cell(row=9, column=ord(col) - ord("A") + 1).alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[9].height = 26

    # Day 0〜30 の行
    for d in range(0, 31):
        r = 10 + d
        ws.cell(row=r, column=1, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        ws.cell(row=r, column=2, value=f"Day {d}").font = Font(bold=True, color=COLORS["accent"])
        ws.cell(row=r, column=2).alignment = Alignment(horizontal="center")
        for col_idx in range(3, 10):
            ws.cell(row=r, column=col_idx, value="").fill = PatternFill("solid", fgColor=COLORS["input_yellow"])
        for col_idx in range(1, 10):
            ws.cell(row=r, column=col_idx).border = THIN_BORDER
        ws.row_dimensions[r].height = 22

    # Update summary formulas to match new ranges (rows 10-40)
    ws["A6"] = "=MAX(C10:C40)"
    ws["B6"] = "=MAX(D10:D40)"
    ws["C6"] = "=MAX(E10:E40)"
    ws["D6"] = "=SUM(F10:F40)"
    ws["E6"] = "=SUM(G10:G40)"
    ws["F6"] = "=SUM(H10:H40)"

    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A10"


# ============================================================
# メイン：すべてのタブを組み立てる
# ============================================================
def main():
    wb = Workbook()
    # デフォルトの "Sheet" を削除
    default = wb["Sheet"]
    wb.remove(default)

    build_tab_howto(wb)
    build_tab_calendar(wb)
    build_tab_mindset(wb)
    build_tab_product(wb)
    build_tab_line(wb)
    build_tab_base(wb)
    build_tab_threads(wb)
    build_tab_funnel(wb)
    build_tab_launch(wb)
    build_tab_stuck_dict(wb)
    build_tab_templates(wb)
    build_tab_dashboard(wb)

    out_path = "/home/user/meal-coach/spreadsheet/0to1_workbook.xlsx"
    wb.save(out_path)
    print(f"✅ Saved: {out_path}")
    print(f"   Tabs: {len(wb.sheetnames)} — {wb.sheetnames}")


if __name__ == "__main__":
    main()

