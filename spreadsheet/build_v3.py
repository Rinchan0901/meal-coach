"""
副業ゼロイチ ワークブック v3（清書版）
========================================
絵文字なし／整ったデザイン／迷わない構成。
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, NamedStyle
from openpyxl.worksheet.datavalidation import DataValidation


# ============================================================
# カラー（くすみ・落ち着き・上品）
# ============================================================
C = {
    "bg":         "FAF7F2",
    "paper":      "FFFFFF",
    "ink":        "2E2A26",   # 本文
    "ink_soft":   "5C544C",   # サブ本文
    "ink_pale":   "9A8F82",   # キャプション
    "accent":     "B07854",   # メインアクセント（テラコッタ）
    "accent_dk":  "8C5A3A",   # 濃いアクセント
    "accent_lt":  "EDDDCB",   # 薄いアクセント
    "rule_pink":  "F1E2DD",   # 詰まり用ピンク（うすめ）
    "rule_pink_dk": "B5715F", # 詰まり強調
    "rule_mint":  "DCE5DD",   # 抜け方ミント
    "rule_mint_dk":"4F7565",  # 抜け方強調
    "rule_sand":  "F1E9D5",   # ヒント
    "rule_sand_dk":"8B7841",  # ヒント強調
    "input":      "FFF8E5",   # 入力欄
    "input_bd":   "E5DCC4",   # 入力欄ボーダー
    "line":       "E5DCD0",   # 区切り線
    "panel":      "F4EEE5",   # パネル
}

# ============================================================
# 共通スタイル
# ============================================================
def thin(color=None):
    return Side(style="thin", color=color or C["line"])

def thick(color=None):
    return Side(style="medium", color=color or C["accent"])

BORDER_ALL = Border(left=thin(), right=thin(), top=thin(), bottom=thin())
BORDER_INPUT = Border(left=thin(C["input_bd"]), right=thin(C["input_bd"]),
                     top=thin(C["input_bd"]), bottom=thin(C["input_bd"]))
BORDER_TOP = Border(top=Side(style="thin", color=C["line"]))
BORDER_BOTTOM = Border(bottom=Side(style="thin", color=C["line"]))
BORDER_ACCENT_TOP = Border(top=Side(style="thin", color=C["accent"]))


def font(size=11, bold=False, color=None, italic=False):
    key = ("f", size, bold, color or C["ink"], italic)
    if key not in _STYLE_CACHE:
        _STYLE_CACHE[key] = Font(name="Noto Sans JP", size=size, bold=bold,
                                  color=color or C["ink"], italic=italic)
    return _STYLE_CACHE[key]


def align(h="left", v="center", wrap=True, indent=0):
    key = ("a", h, v, wrap, indent)
    if key not in _STYLE_CACHE:
        _STYLE_CACHE[key] = Alignment(horizontal=h, vertical=v,
                                       wrap_text=wrap, indent=indent)
    return _STYLE_CACHE[key]


def fill(color):
    key = ("fl", color)
    if key not in _STYLE_CACHE:
        _STYLE_CACHE[key] = PatternFill("solid", fgColor=color)
    return _STYLE_CACHE[key]


_STYLE_CACHE = {}


# ============================================================
# ヘルパー
# ============================================================
def setup(ws, widths):
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    ws.sheet_view.showGridLines = False


def merge(ws, row, col_start, col_end, value="", f=None, a=None, fl=None,
          border=None, height=None):
    ws.merge_cells(start_row=row, start_column=col_start,
                   end_row=row, end_column=col_end)
    cell = ws.cell(row=row, column=col_start, value=value)
    if f: cell.font = f
    if a: cell.alignment = a
    if fl: cell.fill = fl
    if border: cell.border = border
    if height: ws.row_dimensions[row].height = height
    return cell


def write(ws, row, col, value="", f=None, a=None, fl=None, border=None):
    cell = ws.cell(row=row, column=col, value=value)
    if f: cell.font = f
    if a: cell.alignment = a
    if fl: cell.fill = fl
    if border: cell.border = border
    return cell


# ----------- 標準ブロック -----------

def page_title(ws, row, label, title_text, sub_text=None, col_end=4):
    """ページの大見出し（ラベル＋タイトル＋サブ）"""
    write(ws, row, 1, label,
          f=font(10, color=C["accent_dk"]),
          a=align("left", "bottom"))
    ws.row_dimensions[row].height = 16
    merge(ws, row+1, 1, col_end, title_text,
          f=font(22, bold=True, color=C["ink"]),
          a=align("left", "center"),
          height=36)
    if sub_text:
        merge(ws, row+2, 1, col_end, sub_text,
              f=font(11, color=C["ink_soft"]),
              a=align("left", "center"),
              height=24)
    # 下線
    for c in range(1, col_end+1):
        last = row+2 if sub_text else row+1
        ws.cell(row=last+1, column=c).border = Border(top=Side(style="thin", color=C["accent"]))
    return row+4 if sub_text else row+3


def section(ws, row, num, title, col_end=4, color=None):
    """セクション見出し"""
    write(ws, row, 1, str(num),
          f=font(13, bold=True, color="FFFFFF"),
          a=align("center", "center"),
          fl=fill(color or C["accent"]))
    merge(ws, row, 2, col_end, title,
          f=font(13, bold=True, color=C["ink"]),
          a=align("left", "center", indent=1),
          fl=fill(C["panel"]),
          height=30)
    ws.row_dimensions[row].height = 30
    return row+1


def lead(ws, row, text, col_end=4, height=44):
    """セクションリード文"""
    merge(ws, row, 1, col_end, text,
          f=font(11, color=C["ink_soft"]),
          a=align("left", "center", indent=1),
          fl=fill(C["bg"]),
          height=height)
    return row+1


def reason(ws, row, text, col_end=4, height=42):
    """『なぜやるか』ボックス（ミント）"""
    merge(ws, row, 1, col_end, "[なぜこれをやるの？]   " + text,
          f=font(11, color=C["rule_mint_dk"]),
          a=align("left", "center", indent=1),
          fl=fill(C["rule_mint"]),
          height=height)
    return row+1


def fear(ws, row, q, ans, col_end=4):
    """不安と回答（ピンク→ミント）"""
    merge(ws, row, 1, col_end, "[不安かも]   " + q,
          f=font(11, bold=True, color=C["rule_pink_dk"]),
          a=align("left", "center", indent=1),
          fl=fill(C["rule_pink"]),
          height=24)
    merge(ws, row+1, 1, col_end, "[だいじょうぶ]   " + ans,
          f=font(11, color=C["rule_mint_dk"]),
          a=align("left", "center", indent=1),
          fl=fill(C["rule_mint"]),
          height=40)
    return row+2


def tip(ws, row, text, col_end=4, height=44):
    """ヒント（サンド）"""
    merge(ws, row, 1, col_end, "[ヒント]   " + text,
          f=font(11, color=C["rule_sand_dk"]),
          a=align("left", "center", indent=1),
          fl=fill(C["rule_sand"]),
          height=height)
    return row+1


def question_block(ws, row, q, examples_str=None, height_q=28, height_input=70, col_end=4):
    """質問＋例＋入力欄"""
    merge(ws, row, 1, col_end, q,
          f=font(11, bold=True, color=C["accent_dk"]),
          a=align("left", "center", indent=1),
          fl=fill(C["accent_lt"]),
          height=height_q)
    next_row = row + 1
    if examples_str:
        merge(ws, next_row, 1, col_end, "例：" + examples_str,
              f=font(10, italic=True, color=C["ink_pale"]),
              a=align("left", "center", indent=2),
              height=20)
        next_row += 1
    merge(ws, next_row, 1, col_end, "",
          fl=fill(C["input"]),
          border=BORDER_INPUT,
          a=align("left", "top", indent=1),
          height=height_input)
    return next_row + 1


def step_item(ws, row, num, text, col_end=4, height=34):
    """番号付きステップ"""
    write(ws, row, 1, str(num),
          f=font(12, bold=True, color="FFFFFF"),
          a=align("center", "center"),
          fl=fill(C["accent_dk"]))
    merge(ws, row, 2, col_end, text,
          f=font(11),
          a=align("left", "center", indent=1),
          fl=fill(C["paper"]),
          border=Border(bottom=thin(C["line"])),
          height=height)
    ws.row_dimensions[row].height = height
    return row+1


def check_item(ws, row, text, col_end=4, height=26):
    """チェックリスト項目"""
    write(ws, row, 1, "□",
          f=font(14, color=C["accent"]),
          a=align("center", "center"))
    merge(ws, row, 2, col_end, text,
          f=font(11),
          a=align("left", "center", indent=1),
          height=height)
    ws.row_dimensions[row].height = height
    return row+1


def closing(ws, row, text, col_end=4, height=70):
    """締めの応援文"""
    merge(ws, row, 1, col_end, text,
          f=font(12, bold=True, italic=True, color=C["accent_dk"]),
          a=align("center", "center"),
          fl=fill(C["accent_lt"]),
          height=height)
    return row+1


def footer_nav(ws, row, prev_text=None, next_text=None, col_end=4):
    """ページ末のナビゲーション"""
    parts = []
    if prev_text:
        parts.append("← 前：" + prev_text)
    if next_text:
        parts.append("次：" + next_text + " →")
    text = "    |    ".join(parts) if parts else ""
    merge(ws, row, 1, col_end, text,
          f=font(10, color=C["ink_pale"]),
          a=align("center", "center"),
          height=28)
    # 上線
    for c in range(1, col_end+1):
        ws.cell(row=row, column=c).border = Border(top=Side(style="thin", color=C["line"]))
    return row+1


def template_box(ws, row, content, col_end=4, height=200):
    """ひな型ボックス（コピペ用）"""
    merge(ws, row, 1, col_end, content,
          f=font(10, color=C["ink"]),
          a=align("left", "top", indent=1),
          fl=fill(C["accent_lt"]),
          height=height)
    return row+1


# ============================================================
# Tab 00: ようこそ
# ============================================================
def t_welcome(wb):
    ws = wb.create_sheet("00_ようこそ")
    setup(ws, {"A": 6, "B": 24, "C": 60, "D": 18})

    r = page_title(ws, 1, "WELCOME",
                   "副業ゼロイチ ワークブック",
                   "ビジネスを一度もしたことがない人のための、30日間の伴走シート")

    r = section(ws, r, "01", "このシートでできること")
    items = [
        "副業に興味があるけど何から始めればいいかわからない人へ。",
        "30日で「初めての売上1件」を目指します。",
        "毎日のやることが「1つだけ」なので、迷いません。",
        "わからない言葉が出てきたら、いつでもタブ「01_ことば辞典」を開いてください。",
        "「ちゃんとやる」ではなく「今日のぶん終わらせる」で進めます。",
    ]
    for it in items:
        write(ws, r, 1, "・", f=font(11, color=C["accent"]), a=align("center", "center"))
        merge(ws, r, 2, 4, it, f=font(11), a=align("left", "center", indent=1), height=26)
        ws.row_dimensions[r].height = 26
        r += 1

    r += 1
    r = section(ws, r, "02", "進め方の3つのお願い", color=C["rule_mint_dk"])
    rules = [
        ("1日5分でいい",
         "5分やったら今日はOK。続けることだけ大事。続かない日は休むのも計画のうち。"),
        ("黄色のセルだけ埋める",
         "白いセルは説明、黄色いセルがあなたが書く場所。読むだけのページもあります。"),
        ("わからない言葉は飛ばしていい",
         "あとでタブ「01_ことば辞典」を見れば全部書いてあります。今は止まらないで進む。"),
    ]
    for head, body in rules:
        merge(ws, r, 1, 4, head,
              f=font(12, bold=True, color=C["accent_dk"]),
              a=align("left", "center", indent=1),
              fl=fill(C["panel"]),
              height=26)
        r += 1
        merge(ws, r, 1, 4, body,
              f=font(11),
              a=align("left", "center", indent=1),
              fl=fill(C["paper"]),
              border=Border(bottom=thin(C["line"])),
              height=40)
        r += 1

    r += 1
    r = section(ws, r, "03", "タブの順番（上から下へ進むだけ）", color=C["accent_dk"])
    tabs = [
        ("00", "ようこそ", "今ここ。読んだらOK。"),
        ("01", "ことば辞典", "わからない言葉が出てきたらここ。"),
        ("02", "30日カレンダー", "毎日ここに戻って、今日のDayを確認。"),
        ("03", "Day0 自分メモ", "副業を始める前の気持ちを書く。"),
        ("04", "こころの準備", "Day1〜3。読むだけ。"),
        ("05", "売るものを見つける", "Day4〜7。5問の質問で商品決定。"),
        ("06", "LINE設定", "Day8〜10。お知らせを送る場所を作る。"),
        ("07", "BASE設定", "Day11〜14。お店を開く。"),
        ("08", "Threads発信", "Day15〜21。1日1つ投稿する。"),
        ("09", "つなぐ", "Day18〜21。Threads→LINE→BASEを1本道に。"),
        ("10", "はじめての販売", "Day22〜30。お客さんに届ける。"),
        ("11", "こまったとき", "進めなくなったら開く。29個のあるある。"),
        ("12", "ひとりごとメモ", "気持ちや気づきの自由記述欄。"),
    ]
    # ヘッダー
    for c, val in enumerate(["No", "タブ名", "内容"], start=1):
        write(ws, r, c if c < 3 else c, val,
              f=font(10, bold=True, color="FFFFFF"),
              a=align("center", "center"),
              fl=fill(C["ink_soft"]))
    merge(ws, r, 3, 4, "内容",
          f=font(10, bold=True, color="FFFFFF"),
          a=align("center", "center"),
          fl=fill(C["ink_soft"]))
    ws.row_dimensions[r].height = 24
    r += 1
    for num, name, desc in tabs:
        write(ws, r, 1, num, f=font(10, color=C["accent_dk"]), a=align("center", "center"))
        write(ws, r, 2, name, f=font(11, bold=True), a=align("left", "center", indent=1))
        merge(ws, r, 3, 4, desc, f=font(11, color=C["ink_soft"]),
              a=align("left", "center", indent=1))
        for c in range(1, 5):
            ws.cell(row=r, column=c).border = Border(bottom=thin(C["line"]))
        ws.row_dimensions[r].height = 24
        r += 1

    r += 2
    r = closing(ws, r,
        "副業は、特別な人がやるものではありません。\n"
        "このシートを開いた今、あなたはもう始まっています。",
        height=70)
    r = closing(ws, r+1,
        "1日5分でいい。今日のぶんが終わったら、閉じてOK。\n"
        "また明日、ここで会いましょう。",
        height=70)

    ws.freeze_panes = "A5"


# ============================================================
# Tab 01: ことば辞典
# ============================================================
def t_glossary(wb):
    ws = wb.create_sheet("01_ことば辞典")
    setup(ws, {"A": 5, "B": 22, "C": 70})

    r = page_title(ws, 1, "GLOSSARY",
                   "ことば辞典",
                   "副業の本やSNSによく出てくる言葉を、ふつうの日本語にしました（Ctrl+Fで検索可）",
                   col_end=3)

    # ヘッダー
    headers = [("A", "No"), ("B", "こんな言葉"), ("C", "やさしい意味")]
    for col, val in headers:
        write(ws, r, ord(col) - ord("A") + 1, val,
              f=font(10, bold=True, color="FFFFFF"),
              a=align("center", "center"),
              fl=fill(C["ink_soft"]))
    ws.row_dimensions[r].height = 26
    r += 1

    glossary = [
        ("副業", "本業以外でやるお仕事。お小遣い稼ぎから始めればOK。"),
        ("ゼロイチ（0→1）", "初めての売上1件のこと。0円→1円になるその瞬間。"),
        ("商品", "あなたが売るもの。PDF・テンプレート・ノウハウ集など、形がなくてもOK。"),
        ("デジタル商品", "PDFや動画など、ネットで送るだけで届けられる商品。在庫なし・送料なし。"),
        ("ペルソナ", "「あなたが届けたいたった1人のお客さん」のこと。専門用語だけど中身はそれだけ。"),
        ("コンセプト", "売るものの一言説明。「○○な人の△△な悩みを□□で解決する」式の1行。"),
        ("ターゲット", "ペルソナとほぼ同じ意味。お客さんになりそうな人のこと。"),
        ("LP（ランディングページ）", "売るための1枚のWebページ。BASEの商品ページもLPの一種。"),
        ("セールスページ", "LPと同じ意味。商品を売るページ。"),
        ("BASE（ベース）", "無料でネットショップが作れるサービス。thebase.com で開く。"),
        ("Threads（スレッズ）", "Instagramが作った文字メインのSNS。Twitter（X）に似ている。"),
        ("公式LINE", "LINEで「お店からのお知らせ」を送れる仕組み。お友達追加してもらって配信。"),
        ("LINE公式アカウント", "公式LINEと同じ意味。正式名称はこちら。"),
        ("リード", "お客さんになりそうな人のこと。連絡先（LINEなど）を持っている人。"),
        ("リード管理", "お客さんになりそうな人のリストを整える作業。"),
        ("リスト", "公式LINEに登録してくれた人の集まり。"),
        ("集客", "お客さんを集めること。SNSで発信して人を呼ぶこと。"),
        ("動線（どうせん）", "お客さんが歩く道。Threads → LINE → BASE のように、つながりを作ること。"),
        ("ファネル", "動線の英語版。漏斗の形にお客さんが流れていくイメージ。"),
        ("ステップ配信", "LINEで決めた順に「1日後・3日後…」と自動で送る仕組み。"),
        ("リッチメニュー", "公式LINEのトーク画面下に出るボタン。タップでお店に飛ばせる。"),
        ("特商法（とくしょうほう）", "ネット販売で住所など事業者情報を公表する法律。"),
        ("バーチャルオフィス", "本当の住所を出したくない人が借りる「書類用の住所」。月990円〜。"),
        ("プロフィール", "SNSの自己紹介欄。あなたが何の人かを書く場所。"),
        ("インプレッション", "投稿が表示された回数。見られた数。"),
        ("リーチ", "投稿を見た人数。"),
        ("エンゲージメント", "いいね・コメント・保存・シェアなどリアクションされた数。"),
        ("コンバージョン（CV）", "目的が達成された数。販売が完了した数。"),
        ("CV率", "ページを見た人のうち、買ってくれた人の割合。"),
        ("PV", "ページが見られた回数。"),
        ("KPI", "目標数値。フォロワー数や登録数など追いかける数字。"),
        ("コピー", "宣伝の文章。キャッチコピーは「つかみの一言」。"),
        ("クロージング", "最後の一押し。「買ってください」のメッセージのこと。"),
        ("オファー", "「これで○○円ですよ」と提案すること。"),
        ("ローンチ", "新商品を売り出すこと。"),
        ("ストーリーローンチ", "数日かけて物語を語りながら売り出すやり方。"),
        ("先行案内", "「もうすぐ販売します」の予告。期待を作る。"),
        ("クーポン", "BASEで使える割引コード。"),
        ("マネタイズ", "お金にする・稼ぐこと。"),
        ("パッシブインカム", "寝ていても入る収入。デジタル商品なら作れば自動販売。"),
        ("プラットフォーム", "ネットの場所。BASE・Threads・LINEもプラットフォーム。"),
        ("コンテンツ", "中身。記事・動画・PDFなど作ったもの全般。"),
        ("ブランディング", "「あなたっぽさ」を作ること。色・言葉・雰囲気を統一すること。"),
        ("ニッチ", "せまい市場。特定の人向けに絞ること。"),
        ("マインドセット", "考え方の基本姿勢。「完璧主義はやめよう」のような心がけ。"),
        ("レバレッジ", "てこの原理。1つを大勢に届けて稼ぐこと。"),
        ("Canva（キャンバ）", "無料で画像が作れるサービス。canva.com。テンプレ豊富。"),
        ("Notion（ノーション）", "メモ・整理ができる無料アプリ。商品作りに便利。"),
    ]
    for i, (term, defi) in enumerate(glossary, start=1):
        write(ws, r, 1, i,
              f=font(9, color=C["ink_pale"]),
              a=align("center", "top"))
        write(ws, r, 2, term,
              f=font(11, bold=True, color=C["accent_dk"]),
              a=align("left", "top", indent=1),
              fl=fill(C["panel"]))
        write(ws, r, 3, defi,
              f=font(11),
              a=align("left", "top", indent=1))
        for c in range(1, 4):
            ws.cell(row=r, column=c).border = Border(bottom=thin(C["line"]))
        ws.row_dimensions[r].height = 36
        r += 1

    ws.freeze_panes = "A5"


# ============================================================
# Tab 02: 30日カレンダー
# ============================================================
def t_calendar(wb):
    ws = wb.create_sheet("02_30日カレンダー")
    setup(ws, {"A": 7, "B": 11, "C": 50, "D": 11, "E": 28})

    r = page_title(ws, 1, "30-DAY MAP",
                   "30日カレンダー",
                   "毎日ここに戻って、今日のDayを確認。終わったらD列を「できた」に変更。",
                   col_end=5)

    headers = [("A", "Day"), ("B", "日付"), ("C", "今日のひとこと（やること）"),
               ("D", "ステータス"), ("E", "ひとことメモ")]
    for col, val in headers:
        write(ws, r, ord(col) - ord("A") + 1, val,
              f=font(10, bold=True, color="FFFFFF"),
              a=align("center", "center"),
              fl=fill(C["ink_soft"]))
    ws.row_dimensions[r].height = 26
    r += 1

    days = [
        (0, "タブ「03_Day0_自分メモ」を開いて、気持ちを書く（10分）", C["rule_pink"]),
        (1, "タブ「04_こころの準備」のDay1部分を読む。書かなくていい（5分）", C["rule_pink"]),
        (2, "タブ「04_こころの準備」のDay2部分を読む（5分）", C["rule_pink"]),
        (3, "タブ「04_こころの準備」のDay3部分を読む（5分）", C["rule_pink"]),
        (4, "タブ「05_売るものを見つける」のQ1〜Q3を埋める（15分）", C["rule_mint"]),
        (5, "タブ「05_売るものを見つける」のQ4を埋める（10分）", C["rule_mint"]),
        (6, "タブ「05_売るものを見つける」のQ5を埋める（10分）", C["rule_mint"]),
        (7, "タブ「05_売るものを見つける」のまとめ欄を埋める（10分）", C["rule_mint"]),
        (8, "タブ「06_LINE設定」のステップ1〜3を進める（15分）", C["accent_lt"]),
        (9, "タブ「06_LINE設定」のステップ4〜6を進める（20分）", C["accent_lt"]),
        (10, "タブ「06_LINE設定」のステップ7〜9を進める（15分）", C["accent_lt"]),
        (11, "タブ「07_BASE設定」のステップ1〜3を進める（20分）", C["rule_sand"]),
        (12, "タブ「07_BASE設定」のステップ4〜5を進める（15分）", C["rule_sand"]),
        (13, "タブ「07_BASE設定」のステップ6（商品ページ）を進める（30分）", C["rule_sand"]),
        (14, "タブ「07_BASE設定」のステップ7〜8（公開）を進める（20分）", C["rule_sand"]),
        (15, "タブ「08_Threads発信」のプロフィールを書く（15分）", C["bg"]),
        (16, "タブ「08_Threads発信」の今日の投稿を1つ書く（5分）", C["bg"]),
        (17, "今日の投稿を1つ書く（5分）", C["bg"]),
        (18, "投稿1つ＋公式LINEに誘う投稿を1つ（10分）", C["bg"]),
        (19, "投稿1つ。タブ「09_つなぐ」もチラ見（10分）", C["bg"]),
        (20, "投稿1つ＋LINE誘導投稿を1つ（10分）", C["bg"]),
        (21, "タブ「09_つなぐ」のテストを自分でやる（20分）", C["bg"]),
        (22, "タブ「10_はじめての販売」のDay22の予告を書く（15分）", C["rule_pink"]),
        (23, "Day23の自分の話を書いて投稿（15分）", C["rule_pink"]),
        (24, "Day24の予告＋クーポンコード準備（15分）", C["rule_pink"]),
        (25, "Day25：販売開始。LINEとThreadsで案内（20分）", C["rule_pink"]),
        (26, "1to1メッセージを5人に送ってみる（30分）", C["rule_pink"]),
        (27, "「あと1日」のリマインドを送る（10分）", C["rule_pink"]),
        (28, "もし買ってもらえたら、お礼メッセージを書く（5分）", C["rule_pink"]),
        (29, "投稿を続ける／お休みしてもOK（5分）", C["rule_pink"]),
        (30, "30日ふりかえりを書く（タブ10の最後）（15分）", C["rule_pink"]),
    ]

    for d, task, color in days:
        write(ws, r, 1, "Day " + str(d),
              f=font(11, bold=True, color=C["accent_dk"]),
              a=align("center", "center"),
              fl=fill(color),
              border=BORDER_ALL)
        write(ws, r, 2, "",
              fl=fill(C["input"]),
              border=BORDER_INPUT)
        write(ws, r, 3, task,
              f=font(11),
              a=align("left", "center", indent=1),
              fl=fill(color),
              border=BORDER_ALL)
        write(ws, r, 4, "まだ",
              f=font(11),
              a=align("center", "center"),
              fl=fill(C["input"]),
              border=BORDER_INPUT)
        write(ws, r, 5, "",
              fl=fill(C["input"]),
              border=BORDER_INPUT)
        ws.row_dimensions[r].height = 30
        r += 1

    dv = DataValidation(type="list",
                       formula1='"まだ,進行中,できた,休み"',
                       allow_blank=True)
    dv.add(f"D6:D{5+len(days)}")
    ws.add_data_validation(dv)

    ws.freeze_panes = "A6"


# ============================================================
# Tab 03: Day0 自分メモ
# ============================================================
def t_day0(wb):
    ws = wb.create_sheet("03_Day0_自分メモ")
    setup(ws, {"A": 6, "B": 70, "C": 6})

    r = page_title(ws, 1, "DAY 0",
                   "副業を始める前の自分メモ",
                   "30日後、ここを読み返すために。気持ちを残しておく日です。",
                   col_end=3)

    r = lead(ws, r, "今日は書くだけ。難しいこと何もありません。10分で終わります。", col_end=3)

    r = section(ws, r+1, "Q", "10個の質問に答える", col_end=3)

    questions = [
        ("Q1. なぜ副業を始めたい？", "理由は何でもOK。お金・自信・趣味・将来の不安など"),
        ("Q2. 30日後、自分がどうなっていたら嬉しい？", "小さくてOK。「1人にありがとうと言われる」でも◎"),
        ("Q3. 今いちばん不安なことは？", "「失敗したらどうしよう」など、何でも"),
        ("Q4. 今いちばんワクワクすることは？", None),
        ("Q5. 自分が好きなことを3つ書く", "仕事と関係なくてOK。コーヒー・散歩・寝かしつけなど"),
        ("Q6. 「○○について教えて」とよく聞かれることはある？", None),
        ("Q7. 過去の自分が「これさえ知ってたらラクだったのに」ってある？", None),
        ("Q8. 30日のうち、1日にどのくらい時間が取れそう？", "5分／15分／30分／1時間"),
        ("Q9. 家族や周りに副業のこと話す？話さない？", "話さなくてOK"),
        ("Q10. 今の自分に「がんばってる」と一言かけるなら？", None),
    ]
    for q, ex in questions:
        r = question_block(ws, r, q, ex, col_end=3, height_input=70)

    r += 1
    r = closing(ws, r,
        "ぜんぶ書けなくてOK。1個でも書いたあなたが偉い。\n"
        "明日からは、考え方の準備をしていきます。",
        col_end=3, height=60)

    r = footer_nav(ws, r+1, "00_ようこそ", "04_こころの準備", col_end=3)
    ws.freeze_panes = "A5"


# ============================================================
# Tab 04: こころの準備（読むだけ）
# ============================================================
def t_mindset(wb):
    ws = wb.create_sheet("04_こころの準備")
    setup(ws, {"A": 6, "B": 72, "C": 6})

    r = page_title(ws, 1, "DAY 1-3",
                   "こころの準備",
                   "副業を始める前に、これだけ知っておけば大丈夫。書く欄はありません。",
                   col_end=3)

    r = section(ws, r, "01", "Day 1：完璧主義をやめる", col_end=3)
    r = lead(ws, r,
        "副業で詰まる人の99%は「ちゃんと準備してから出したい」と思って半年経ちます。",
        col_end=3, height=44)
    msgs1 = [
        "副業の準備に「100点」はありません。出してみないと、何が必要かわからないからです。",
        "覚えてほしいのは、たったひとつ。「今日のぶん、終わらせる」です。",
        "「ちゃんと」を「とりあえず」に置き換えてみてください。",
        "例：「ちゃんと商品を作ろう」→「とりあえず1ページ書いてみる」",
        "未完成のまま出すのは、失礼ではありません。放置するほうが失礼です。",
    ]
    for m in msgs1:
        merge(ws, r, 1, 3, "・　" + m,
              f=font(11),
              a=align("left", "center", indent=1),
              fl=fill(C["paper"]),
              border=Border(bottom=thin(C["line"])),
              height=34)
        r += 1

    r += 1
    r = section(ws, r, "02", "Day 2：お金をいただくのは申し訳ない？", col_end=3)
    r = lead(ws, r,
        "「お金を取るのは申し訳ない」と感じる人は優しい人。でも、その優しさが副業のブレーキになります。",
        col_end=3, height=44)
    msgs2 = [
        "事実：お金を払って買った人ほど、本気で取り組みます。無料だと適当に消費されます。",
        "つまり、お金をもらうことは「お客さんの本気を引き出すサービス」でもあります。",
        "値段は迷ったら2,980円から始めてOK。これがいちばん買いやすい金額です。",
        "ガッカリされたら？→「ご満足いただけなければ全額返金」と書けば解決。返金は1%以下。",
        "「申し訳ない」の反対は「傲慢」ではなく、「ありがとう」です。",
    ]
    for m in msgs2:
        merge(ws, r, 1, 3, "・　" + m,
              f=font(11),
              a=align("left", "center", indent=1),
              fl=fill(C["paper"]),
              border=Border(bottom=thin(C["line"])),
              height=34)
        r += 1

    r += 1
    r = section(ws, r, "03", "Day 3：時間がない人ほど続けられる方法", col_end=3)
    r = lead(ws, r,
        "「1日2時間取れたら本気でやる」と思う人は、いつまでも始められません。",
        col_end=3, height=44)
    msgs3 = [
        "解決策：「1日5分でも進む設計」に変える。このシートはそのために作ってあります。",
        "おすすめ：朝の3分＋夜の2分でもOK。連続してなくていい。",
        "子どもが寝た後の静かな15分が、いちばん集中できます。",
        "週に1日「何もしない日」を最初から決めておく。罪悪感ループを防ぐ。",
        "続けられる人の共通点：同じ時間・同じ場所・同じきっかけで作業すること。",
        "例：子どもが寝たら、ソファでスマホを開いて、Threadsを1つ投稿する。",
    ]
    for m in msgs3:
        merge(ws, r, 1, 3, "・　" + m,
              f=font(11),
              a=align("left", "center", indent=1),
              fl=fill(C["paper"]),
              border=Border(bottom=thin(C["line"])),
              height=34)
        r += 1

    r += 1
    r = closing(ws, r,
        "読むだけのDayは、これで終わりです。\n"
        "明日から、いよいよ「売るもの」を見つけにいきます。",
        col_end=3, height=60)

    r = footer_nav(ws, r+1, "03_Day0_自分メモ", "05_売るものを見つける", col_end=3)
    ws.freeze_panes = "A5"


# ============================================================
# Tab 05: 売るものを見つける
# ============================================================
def t_product(wb):
    ws = wb.create_sheet("05_売るものを見つける")
    setup(ws, {"A": 6, "B": 30, "C": 60, "D": 8})

    r = page_title(ws, 1, "DAY 4-7",
                   "売るものを見つける",
                   "難しく考えなくて大丈夫。あなたの「当たり前」が、誰かの「ありがたい」になります。")

    r = reason(ws, r, "副業の最初は「何を売るか」が9割。先に決めれば、あとはラクです。")

    # Q1〜Q3
    r = section(ws, r+1, "Q1", "あなたが過去に乗り越えた「悩み」はなに？")
    r = reason(ws, r, "過去のあなたが解決したことは、今同じ悩みの人にとっての宝物です。")
    r = question_block(ws, r,
        "下の入力欄に書いてください",
        "寝かしつけのコツがわからなかった／お金の管理が下手だった／在宅ワークで集中できなかった",
        height_input=80)

    r += 1
    r = section(ws, r, "Q2", "友達やママ友からよく聞かれることは？")
    r = reason(ws, r, "聞かれること=他の人も困っていること。商品の種は誰かの質問の中にあります。")
    r = question_block(ws, r,
        "下の入力欄に書いてください",
        "離乳食どうしてる？／おむつ卒業のタイミング教えて／在宅ワーク何してるの？",
        height_input=80)

    r += 1
    r = section(ws, r, "Q3", "つい何時間でも調べてしまうテーマは？")
    r = reason(ws, r, "好きなテーマは続けられる。続けられるテーマは商品になります。")
    r = question_block(ws, r,
        "下の入力欄に書いてください",
        "時短レシピ／片付け・収納／家計管理アプリ",
        height_input=80)

    r += 1
    r = section(ws, r, "Q4", "Q1〜Q3を見て、いちばん「これだ」と感じたテーマは？", color=C["rule_mint_dk"])
    r = reason(ws, r, "ここで決めるのは「テーマ」だけ。商品の中身は後で決めます。")
    r = question_block(ws, r,
        "1つだけ選んで書いてください",
        "離乳食の段取り／ワーママの家計管理／片付けの初級コツ",
        height_input=60)

    r += 1
    r = section(ws, r, "Q5", "そのテーマで、3ヶ月前のあなたが3,000円払ってでも欲しかったものは？", color=C["rule_mint_dk"])
    r = reason(ws, r, "3ヶ月前の自分が買いたいもの=同じ場所にいる人が買いたいものです。")
    r = question_block(ws, r,
        "下の入力欄に書いてください",
        "離乳食4週間ぶんの献立PDF／ワーママ用の月3万円貯金ワークシート／10分でできる片付けチェックリスト",
        height_input=80)

    r += 1
    r = section(ws, r, "★", "まとめ：あなたの最初の商品", color=C["accent_dk"])
    matome_fields = [
        ("1. 商品の名前（タイトル）", "離乳食ママの月3,000円・15分献立PDF"),
        ("2. 誰のため？（1人だけ思い浮かべる）", "1歳の息子をもつ友人のあやかさん"),
        ("3. その人のいちばんの悩みは？", "毎日メニューを考えるのに疲れている"),
        ("4. その悩みをどう解決する？", "4週間ぶんの献立を渡せば、考えなくて済む"),
        ("5. いくらで売る？", "1,980 / 2,980 / 3,980 / 4,980 から1つ"),
        ("6. どんな形で渡す？", "PDF / ワークシート / 動画 / チェックリスト から1つ"),
    ]
    for label, ex in matome_fields:
        merge(ws, r, 1, 2, label,
              f=font(11, bold=True, color=C["accent_dk"]),
              a=align("left", "center", indent=1),
              fl=fill(C["panel"]),
              height=30)
        merge(ws, r, 3, 4, "",
              fl=fill(C["input"]),
              border=BORDER_INPUT)
        ws.row_dimensions[r].height = 30
        r += 1
        merge(ws, r, 1, 4, "例：" + ex,
              f=font(10, italic=True, color=C["ink_pale"]),
              a=align("left", "center", indent=2),
              height=18)
        r += 1

    r += 1
    r = fear(ws, r,
        "「私のテーマじゃダメかも」と思った？",
        "大丈夫。商品テーマは、あとから何度でも変えられます。今日決めるのは仮でOK。")

    r += 1
    r = closing(ws, r,
        "売るものが決まりました。\n"
        "次はお客さんとつながる場所（LINE）を作ります。", height=60)

    r = footer_nav(ws, r+1, "04_こころの準備", "06_LINE設定")
    ws.freeze_panes = "A5"


# ============================================================
# Tab 06: LINE設定
# ============================================================
def t_line(wb):
    ws = wb.create_sheet("06_LINE設定")
    setup(ws, {"A": 6, "B": 30, "C": 60, "D": 8})

    r = page_title(ws, 1, "DAY 8-10",
                   "LINE（お知らせを届ける場所）を作る",
                   "公式LINEは「お店からのお知らせを送れる仕組み」。確実にメッセージが届きます。")

    r = reason(ws, r,
        "Threadsの投稿は10〜20%しか見られないが、LINEは60〜80%届く。だからLINEを先に作る。")

    r = section(ws, r+1, "目標", "LINEに「友だち追加してね」と言える状態にする")

    r = section(ws, r+1, "01", "やることリスト（9ステップ）", color=C["accent_dk"])
    steps = [
        "スマホで「LINE Official Account Manager」を検索→アプリをダウンロード（無料）",
        "メールアドレスとパスワードを決めて、新規アカウントを作成",
        "アカウント名を決める。例：「あさみ｜離乳食コーチ」のような「名前｜何の人か」形式",
        "プロフィール画像を設定（顔出しNGならCanvaで作ったロゴでOK）",
        "ステータスメッセージを20字以内で書く（何を配信する人かを一言）",
        "あいさつメッセージを書く（次のセクションのテンプレ参照）",
        "登録特典の無料プレゼントPDFを用意（Canvaで作成）",
        "自動応答で「特典」というキーワードを設定",
        "自分のスマホで友だち追加してテスト→ぜんぶ届くか確認",
    ]
    for i, s in enumerate(steps, start=1):
        r = step_item(ws, r, i, s)

    r += 1
    r = section(ws, r, "02", "あいさつメッセージのひな型", color=C["rule_mint_dk"])
    r = template_box(ws, r,
        "はじめまして、{あなたの名前}と申します。\n\n"
        "このLINEでは、{テーマ}についての\n"
        "ちょっとしたコツや小ネタを\n"
        "ゆるっと配信しています。\n\n"
        "［登録のお礼に、無料プレゼントをご用意しました］\n"
        "下のキーワード「特典」と送ってください。\n"
        "（自動でPDFが届きます）\n\n"
        "ご感想やご質問は、\n"
        "このトークから気軽に送ってくださいね。\n"
        "1通1通、必ず読んでいます。",
        height=240)

    r += 1
    r = section(ws, r, "03", "あなたのあいさつメッセージ（書く欄）", color=C["accent_dk"])
    merge(ws, r, 1, 4, "",
          fl=fill(C["input"]),
          border=BORDER_INPUT,
          a=align("left", "top", indent=1),
          height=240)
    r += 1

    r += 1
    r = section(ws, r, "04", "無料プレゼント（登録特典）の作り方", color=C["rule_mint_dk"])
    gift_msgs = [
        "登録特典＝「LINE登録してくれた人にあげる無料のもの」。あると登録率が3倍に。",
        "中身は「商品の縮小版」でOK。例：商品が4週間献立PDFなら、特典は7日ぶんのミニ版。",
        "作り方：Canvaで「PDF テンプレート」を検索→好きなテンプレを選ぶ→文字を置き換える。",
        "保存：Googleドライブにアップ→「リンクを知っている全員が閲覧可」に設定→URLをコピー。",
        "そのURLを、自動応答メッセージに貼り付ければ完成です。",
    ]
    for m in gift_msgs:
        merge(ws, r, 1, 4, "・　" + m,
              f=font(11),
              a=align("left", "center", indent=1),
              fl=fill(C["paper"]),
              border=Border(bottom=thin(C["line"])),
              height=32)
        r += 1

    r += 1
    r = section(ws, r, "05", "不安かも、と思ったら", color=C["rule_pink_dk"])
    fears = [
        ("本名を出したくない",
         "ニックネームでOK。下の名前だけ（あさみ・まりこ等）が一番信頼されやすい。"),
        ("リッチメニューって作れるかな",
         "最初は文字だけでOK。Canvaで「LINE リッチメニュー」検索→無料テンプレ→15分で完成。"),
        ("住所を公表したくない",
         "バーチャルオフィス（月990円〜）か、特商法の「請求があれば開示」を選択でOK。"),
    ]
    for q, a in fears:
        r = fear(ws, r, q, a)

    r += 1
    r = closing(ws, r,
        "LINE開設、おつかれさまでした。\n"
        "次はお店（BASE）を作ります。", height=60)

    r = footer_nav(ws, r+1, "05_売るものを見つける", "07_BASE設定")
    ws.freeze_panes = "A5"


# ============================================================
# Tab 07: BASE設定
# ============================================================
def t_base(wb):
    ws = wb.create_sheet("07_BASE設定")
    setup(ws, {"A": 6, "B": 30, "C": 60, "D": 8})

    r = page_title(ws, 1, "DAY 11-14",
                   "BASE（お店）を作る",
                   "BASEは無料でネットショップが開ける場所。thebase.com で開設できます。")

    r = reason(ws, r,
        "BASEは初期費用も月額も0円。売れた時に手数料が引かれるだけ。デジタル商品なら配送もありません。")

    r = section(ws, r+1, "目標", "商品ページを作って「公開」ボタンを押す")

    r = section(ws, r+1, "01", "やることリスト（8ステップ）", color=C["accent_dk"])
    steps = [
        "PCかスマホで「thebase.com」を開く（Google検索でも「BASE」でOK）",
        "緑の「無料でネットショップを開設」ボタンを押す",
        "メールアドレス・パスワード・ショップURL（後から変えられない）を決める",
        "テーマ（デザイン）を選ぶ。デジタル商品なら「Simple」系がおすすめ",
        "管理画面の「Apps」をタップ→3つ追加：デジタルコンテンツApp／商品レビューApp／クーポンApp",
        "「設定」→「特定商取引法に基づく表記」を入力（次のセクション参照）",
        "商品ページを作る（次のセクションの7ブロック型を使う）。商品画像3枚も用意",
        "自分のスマホでテスト購入→OKなら「公開」ボタン",
    ]
    for i, s in enumerate(steps, start=1):
        r = step_item(ws, r, i, s)

    r += 1
    r = section(ws, r, "02", "特商法の書き方（ひな型）", color=C["rule_mint_dk"])
    r = template_box(ws, r,
        "販売事業者：{あなたの本名}\n"
        "所在地：{自宅住所 または「請求があれば開示」を選択}\n"
        "電話番号：{電話番号 または「請求があれば開示」を選択}\n"
        "メールアドレス：{連絡用メール}\n"
        "販売価格：各商品ページに記載\n"
        "送料・手数料：デジタル商品のため無料\n"
        "お支払い方法：クレジットカード／コンビニ決済／銀行振込\n"
        "お支払い時期：注文時にお支払い\n"
        "商品の引渡し時期：決済確認後すぐにダウンロードURLをお送りします\n"
        "返品・交換：デジタル商品の特性上、原則として返品・返金はお受けしておりません。\n"
        "ただし商品に不備があった場合はメールにてご連絡ください。",
        height=240)

    r += 1
    r = section(ws, r, "03", "商品ページの作り方（7ブロック）", color=C["accent_dk"])
    r = lead(ws, r,
        "下の7ブロックを順番に書くだけで、売れる商品ページが完成します。下書き欄に書いてからBASEに貼り付けてください。",
        height=44)

    blocks = [
        ("ブロック1：最初の3行（つかみ）",
         "こんにちは、{呼びかけ}さん。「{本音セリフ}」そんなあなたに届けたいPDFができました。"),
        ("ブロック2：こんな悩みありませんか",
         "□ 悩み1 □ 悩み2 □ 悩み3 □ 悩み4 □ 悩み5"),
        ("ブロック3：私もそうでした（過去の話）",
         "私自身、{過去の悩み}でした。{何を試して何がダメか}そこで{気づき}があり、{今の姿}に変わりました。"),
        ("ブロック4：このPDFで得られるもの",
         "○結果1 ○結果2 ○結果3 ○結果4"),
        ("ブロック5：内容（目次）",
         "全{X}ページ／PDF形式　目次：P1表紙 P2-3はじめに …"),
        ("ブロック6：価格と保証",
         "通常価格{X,XXX}円。ご購入後すぐにダウンロードURLが届きます。ご満足いただけなければ全額返金。"),
        ("ブロック7：作者からのメッセージ",
         "最後までお読みいただきありがとうございます。このPDFは、{あなたの想い}。{ニックネーム}より。"),
    ]
    for i, (label, tmpl) in enumerate(blocks, start=1):
        write(ws, r, 1, str(i),
              f=font(13, bold=True, color="FFFFFF"),
              a=align("center", "center"),
              fl=fill(C["accent"]))
        merge(ws, r, 2, 2, label,
              f=font(11, bold=True, color=C["accent_dk"]),
              a=align("left", "top", indent=1),
              fl=fill(C["panel"]))
        merge(ws, r, 3, 4, "ひな型：" + tmpl,
              f=font(10, italic=True, color=C["ink_pale"]),
              a=align("left", "top", indent=1))
        ws.row_dimensions[r].height = 60
        r += 1
        merge(ws, r, 1, 4, "",
              fl=fill(C["input"]),
              border=BORDER_INPUT,
              a=align("left", "top", indent=1),
              height=100)
        r += 1

    r += 1
    r = section(ws, r, "04", "不安かも、と思ったら", color=C["rule_pink_dk"])
    fears = [
        ("公開ボタンが押せない",
         "押した瞬間、99.99%の人はあなたのお店に気づきません。Threadsで誘導するまで、誰も来ません。"),
        ("商品画像が作れない",
         "Canvaで「商品サムネイル」検索→無料テンプレ→文字を変えるだけ。15分で1枚できます。"),
        ("自分の本名を出すのが怖い",
         "BASEで「請求があれば遅滞なく開示する」を選択可。または月990円のバーチャルオフィスで対応可。"),
    ]
    for q, a in fears:
        r = fear(ws, r, q, a)

    r += 1
    r = closing(ws, r,
        "お店ができました。\n"
        "まだお客さんは来ていなくても大丈夫。\n"
        "次はお客さんを呼びにいきます。", height=70)

    r = footer_nav(ws, r+1, "06_LINE設定", "08_Threads発信")
    ws.freeze_panes = "A5"


# ============================================================
# Tab 08: Threads発信
# ============================================================
def t_threads(wb):
    ws = wb.create_sheet("08_Threads発信")
    setup(ws, {"A": 6, "B": 14, "C": 16, "D": 48, "E": 12})

    r = page_title(ws, 1, "DAY 15-21",
                   "Threadsで発信する",
                   "Threadsは文字メインのSNS。1日5分、顔出し不要で続けられます。",
                   col_end=5)

    r = reason(ws, r,
        "1日5分の投稿で、お店に来てくれる人を増やせる場所。最初の30投稿は種まき、収穫はその後です。",
        col_end=5)

    r = section(ws, r+1, "目標", "1日1つ投稿。21日後にLINE登録1人を目指す。", col_end=5)

    r = section(ws, r+1, "01", "プロフィールを書く（Day 15）", color=C["accent_dk"], col_end=5)
    profile_fields = [
        ("名前欄（10〜15字）", "あさみ｜離乳食ラクするコーチ"),
        ("自己紹介1行目：誰のための発信か", "離乳食はじめたてママのためのラク献立"),
        ("自己紹介2行目：あなたのこと", "元保育士／2児のママ／レシピ歴3年"),
        ("自己紹介3行目：いつ何を発信？", "毎日21時にラクできる時短ネタ"),
        ("自己紹介4行目：オファー", "無料プレゼント中→プロフ下のリンクから"),
        ("リンク欄", "公式LINEの友だち追加URL"),
    ]
    for label, ex in profile_fields:
        merge(ws, r, 2, 3, label,
              f=font(11, bold=True, color=C["accent_dk"]),
              a=align("left", "center", indent=1),
              fl=fill(C["panel"]),
              height=28)
        merge(ws, r, 4, 5, "",
              fl=fill(C["input"]),
              border=BORDER_INPUT)
        ws.row_dimensions[r].height = 28
        r += 1
        merge(ws, r, 2, 5, "例：" + ex,
              f=font(10, italic=True, color=C["ink_pale"]),
              a=align("left", "center", indent=2),
              height=18)
        r += 1

    r += 1
    r = section(ws, r, "02", "投稿の5つの型", color=C["rule_mint_dk"], col_end=5)

    types = [
        ("1. 気づき型",
         "{お客さん}が陥りがちな勘違い。\n"
         "「{勘違い}」\n"
         "→実は{真実}\n"
         "私も同じでした。\n"
         "今日も{呼びかけ}。"),
        ("2. 失敗談型",
         "昔の私の大失敗の話。\n"
         "{失敗のシーン1〜2行}\n"
         "{気持ち1行}\n"
         "そこから学んだのは、\n"
         "{学び}ということ。"),
        ("3. お役立ち型",
         "{お客さん}が今すぐできる、{テーマ}のコツ3つ。\n"
         "1. {コツ1}\n"
         "2. {コツ2}\n"
         "3. {コツ3}\n"
         "試してみてね。"),
        ("4. 質問型",
         "{お客さん}に質問。\n"
         "{シチュエーション}の時、A派？B派？\n"
         "私はBで、理由は{1行}。\n"
         "コメントで教えて。"),
        ("5. 応援型",
         "今日もがんばってる{お客さん}へ。\n"
         "{労いの言葉}\n"
         "今日はもう休んでもいい。\n"
         "明日もここで会えますように。"),
    ]
    for typ, tmpl in types:
        merge(ws, r, 2, 2, typ,
              f=font(11, bold=True, color=C["accent_dk"]),
              a=align("left", "top", indent=1),
              fl=fill(C["panel"]))
        merge(ws, r, 3, 5, tmpl,
              f=font(10, color=C["ink"]),
              a=align("left", "top", indent=1),
              fl=fill(C["accent_lt"]))
        ws.row_dimensions[r].height = 110
        r += 1

    r += 1
    r = section(ws, r, "03", "7日ぶんの投稿スケジュール（Day 15〜21）", color=C["accent_dk"], col_end=5)

    headers = ["Day", "曜日", "おすすめの型", "今日の投稿（書く欄）", "投稿した?"]
    for i, h in enumerate(headers, start=1):
        write(ws, r, i, h,
              f=font(10, bold=True, color="FFFFFF"),
              a=align("center", "center"),
              fl=fill(C["ink_soft"]))
    ws.row_dimensions[r].height = 24
    r += 1

    schedule = [
        (15, "月", "1. 気づき型"),
        (16, "火", "3. お役立ち型"),
        (17, "水", "2. 失敗談型"),
        (18, "木", "4. 質問型"),
        (19, "金", "3. お役立ち型"),
        (20, "土", "5. 応援型"),
        (21, "日", "5. 応援型 or 休み"),
    ]
    for d, day, typ in schedule:
        write(ws, r, 1, "Day " + str(d),
              f=font(11, bold=True, color=C["accent_dk"]),
              a=align("center", "center"))
        write(ws, r, 2, day, f=font(11), a=align("center", "center"))
        write(ws, r, 3, typ,
              f=font(11),
              a=align("center", "center"),
              fl=fill(C["accent_lt"]))
        write(ws, r, 4, "",
              fl=fill(C["input"]),
              border=BORDER_INPUT,
              a=align("left", "top", indent=1))
        write(ws, r, 5, "",
              fl=fill(C["input"]),
              border=BORDER_INPUT)
        ws.row_dimensions[r].height = 90
        r += 1

    r += 1
    r = section(ws, r, "04", "不安かも、と思ったら", color=C["rule_pink_dk"], col_end=5)
    fears = [
        ("いいねが0だったら恥ずかしい",
         "最初の30投稿は土壌づくり。投稿したらアプリを閉じる。31投稿目から伸びた投稿だけ見る。"),
        ("家族にバレたくない",
         "Threadsは別アカウント可。インスタとは別アカで運用すれば家族にバレません。"),
        ("批判コメントが怖い",
         "フォロワー1,000人未満は批判コメント来ません。届かないので心配無用。"),
        ("投稿が思いつかない",
         "型のテンプレに沿って機械的に書く。10分悩んだら下書き保存して翌日へ。"),
    ]
    for q, a in fears:
        r = fear(ws, r, q, a, col_end=5)

    r += 1
    r = closing(ws, r,
        "毎日5分。種をまく日々です。\n"
        "結果が出ない日もありますが、続けた人だけが30日後の景色を見られます。",
        col_end=5, height=70)

    r = footer_nav(ws, r+1, "07_BASE設定", "09_つなぐ", col_end=5)
    ws.freeze_panes = "A5"


# ============================================================
# Tab 09: つなぐ
# ============================================================
def t_funnel(wb):
    ws = wb.create_sheet("09_つなぐ")
    setup(ws, {"A": 6, "B": 30, "C": 60, "D": 8})

    r = page_title(ws, 1, "DAY 18-21",
                   "つなぐ",
                   "Threads → LINE → BASE を1本の道にする日。お客さんが迷わずたどれるか確認します。")

    r = reason(ws, r,
        "Threadsに直接BASEのURLを貼っても売れません。LINEで関係を温めてから案内するのが、5〜10倍売れる方法。")

    r = section(ws, r+1, "目標", "自分で全部の道を歩いてみて、迷わずたどれるか確認")

    r = section(ws, r+1, "01", "動線テスト（自分で歩く）", color=C["accent_dk"])
    test_items = [
        "別のスマホ／友達のスマホで、自分のThreadsプロフィールを開く",
        "プロフィールから公式LINEのリンクをタップ→飛べる？",
        "友だち追加→あいさつメッセージが届く？",
        "「特典」と送信→自動応答PDFが届く？",
        "PDFのリンクからダウンロードできる？",
        "PDFの最終ページに公式LINEのQRコードが入っている？",
        "BASEのショップURLにLINEから飛べる？",
        "（テスト購入）BASEで自分の商品を買ってみる",
        "購入完了メールが届く？",
        "ダウンロードURLからPDFが取れる？",
    ]
    for item in test_items:
        r = check_item(ws, r, item)

    r += 1
    r = fear(ws, r,
        "ぜんぶできるかな…",
        "1箇所ずつ確認すれば大丈夫。詰まったらタブ「11_こまったとき」を開いてください。")

    r += 1
    r = closing(ws, r,
        "道がつながりました。\n"
        "あとはお客さんを呼ぶだけです。", height=60)

    r = footer_nav(ws, r+1, "08_Threads発信", "10_はじめての販売")
    ws.freeze_panes = "A5"


# ============================================================
# Tab 10: はじめての販売
# ============================================================
def t_sales(wb):
    ws = wb.create_sheet("10_はじめての販売")
    setup(ws, {"A": 6, "B": 30, "C": 60, "D": 8})

    r = page_title(ws, 1, "DAY 22-30",
                   "はじめてのお客さんに会いに行く",
                   "ここからの9日間がゼロイチの本番。やさしくお客さんに声をかけていきます。")

    r = reason(ws, r,
        "「明日販売します」と1回告知しても売れません。4日かけて物語を語って、心の準備をしてもらいます。")

    r = section(ws, r+1, "01", "9日間のスケジュール", color=C["accent_dk"])
    schedule = [
        ("Day 22", "予告編：「ある悩みについて、3年かけて見つけた答えがある」と1投稿"),
        ("Day 23", "共感編：過去の自分の失敗談・どん底だった話を投稿"),
        ("Day 24", "前日告知：「明日、その答えをまとめたものを公開します」"),
        ("Day 25", "販売開始。LINEとThreadsで案内＋48時間限定クーポン"),
        ("Day 26", "リマインド：「あと1日です」LINE配信＋1to1メッセージ5人へ"),
        ("Day 27", "クーポン終了告知＋追加の1to1メッセージ"),
        ("Day 28", "もし買ってもらえたら、お礼メッセージ即送信"),
        ("Day 29", "投稿を続ける／お休みもOK"),
        ("Day 30", "30日ふりかえりを書く"),
    ]
    for day, desc in schedule:
        write(ws, r, 1, day,
              f=font(11, bold=True, color="FFFFFF"),
              a=align("center", "center"),
              fl=fill(C["accent_dk"]))
        merge(ws, r, 2, 4, desc,
              f=font(11),
              a=align("left", "center", indent=1),
              fl=fill(C["panel"]))
        ws.row_dimensions[r].height = 30
        r += 1

    r += 1
    r = section(ws, r, "02", "Day 22 予告投稿（書く欄）", color=C["rule_mint_dk"])
    r = template_box(ws, r,
        "ひな型：\n"
        "3年前の私は、{過去の悩み}\n\n"
        "何をやってもダメで、\n"
        "泣きながら検索していた夜を\n"
        "今でも覚えています。\n\n"
        "そこから3年、\n"
        "試行錯誤の末にたどり着いた答えを、\n"
        "今週、はじめて世に出します。\n\n"
        "詳細は、公式LINEでお伝えします。\n"
        "→LINE登録はプロフィールから\n\n"
        "あなたの{お客さんの悩み}が、\n"
        "1日でも早く軽くなりますように。",
        height=260)
    merge(ws, r, 1, 4, "",
          fl=fill(C["input"]),
          border=BORDER_INPUT,
          a=align("left", "top", indent=1),
          height=200)
    r += 1

    r += 1
    r = section(ws, r, "03", "Day 25 販売開始LINE（書く欄）", color=C["rule_mint_dk"])
    r = template_box(ws, r,
        "ひな型：\n"
        "{呼びかけ}さん、こんばんは。\n\n"
        "今日、ついに完成した\n"
        "{商品名}を公開します。\n\n"
        "[商品ページ]\n"
        "{BASEのURL}\n\n"
        "[{締切日}までの限定特典]\n"
        "○ LINE登録者さま限定 {YY}円OFFクーポン\n"
        "  コード：{COUPON_CODE}\n\n"
        "[今すぐ受け取る]\n"
        "{BASEのURL}\n\n"
        "ご質問はこのトークから。\n"
        "{ニックネーム}より",
        height=300)
    merge(ws, r, 1, 4, "",
          fl=fill(C["input"]),
          border=BORDER_INPUT,
          a=align("left", "top", indent=1),
          height=200)
    r += 1

    r += 1
    r = section(ws, r, "04", "1to1メッセージを送る相手リスト（5人）", color=C["accent_dk"])
    r = lead(ws, r,
        "売り込みではなく「気にかけ」。スルーされてもOKという気持ちで送ります。",
        height=30)

    headers = ["No", "送る相手", "やりとりメモ", "送った?"]
    for i, h in enumerate(headers, start=1):
        write(ws, r, i, h,
              f=font(10, bold=True, color="FFFFFF"),
              a=align("center", "center"),
              fl=fill(C["ink_soft"]))
    ws.row_dimensions[r].height = 24
    r += 1
    for i in range(1, 6):
        write(ws, r, 1, i,
              f=font(11, color=C["accent"]),
              a=align("center", "center"))
        for col in [2, 3, 4]:
            write(ws, r, col, "",
                  fl=fill(C["input"]),
                  border=BORDER_INPUT)
        ws.row_dimensions[r].height = 28
        r += 1

    r += 1
    r = section(ws, r, "05", "もし買ってくれたら：お礼メッセージのひな型", color=C["rule_mint_dk"])
    r = template_box(ws, r,
        "{お名前}さん、\n\n"
        "{商品名}をご購入いただき、\n"
        "本当にありがとうございます。\n\n"
        "実は、{お名前}さんが\n"
        "私にとっての初めてのお客様です。\n\n"
        "ずっとずっと、{お客さん}の方の\n"
        "役に立ちたくて、\n"
        "3年かけて作ってきたものでした。\n\n"
        "それを最初に手に取ってくださったこと、\n"
        "一生忘れません。\n\n"
        "PDFのご感想や、\n"
        "「ここがわからない」など、\n"
        "このトークで気軽にお聞かせください。\n\n"
        "{ニックネーム}",
        height=340)

    r += 1
    r = section(ws, r, "06", "30日ふりかえり（Day 30）", color=C["accent_dk"])
    review = [
        "30日前の自分と比べて、変わったことを5つ書く",
        "Threadsのフォロワー数（30日後）",
        "公式LINEの登録者数（30日後）",
        "BASEの商品ページ閲覧数",
        "販売件数（0でもOK）",
        "売上（0円でもOK）",
        "1番うまくいったこと（1つ）",
        "1番うまくいかなかったこと（1つ）",
        "次の30日でやりたいこと（3つ）",
        "30日前の自分にかける言葉",
    ]
    for q in review:
        merge(ws, r, 1, 4, q,
              f=font(11, bold=True, color=C["accent_dk"]),
              a=align("left", "center", indent=1),
              fl=fill(C["panel"]),
              height=24)
        r += 1
        merge(ws, r, 1, 4, "",
              fl=fill(C["input"]),
              border=BORDER_INPUT,
              a=align("left", "top", indent=1),
              height=60)
        r += 1

    r += 1
    r = closing(ws, r,
        "30日、本当におつかれさまでした。\n"
        "ゼロイチができても、できなくても、\n"
        "ここまで進んだあなたは、もう昨日とは違います。",
        height=80)

    r = footer_nav(ws, r+1, "09_つなぐ", "11_こまったとき")
    ws.freeze_panes = "A5"


# ============================================================
# Tab 11: こまったとき
# ============================================================
def t_help(wb):
    ws = wb.create_sheet("11_こまったとき")
    setup(ws, {"A": 5, "B": 33, "C": 58})

    r = page_title(ws, 1, "HELP",
                   "こまったときの相談室",
                   "進めなくなったとき、不安になったとき、ここを開いてください。",
                   col_end=3)

    headers = [("A", "カテゴリ"), ("B", "こんな気持ちのとき"), ("C", "こうしてみて")]
    for col, val in headers:
        write(ws, r, ord(col) - ord("A") + 1, val,
              f=font(10, bold=True, color="FFFFFF"),
              a=align("center", "center"),
              fl=fill(C["ink_soft"]))
    ws.row_dimensions[r].height = 26
    r += 1

    helps = [
        ("商品", "自分のスキルじゃ商品にならない気がする",
         "スキルじゃなく「3ヶ月前の自分が困ってたこと」を商品に。3ヶ月分の試行錯誤で十分。"),
        ("商品", "テーマが10個浮かんで絞れない",
         "全部やらない。「友達3人から相談されたテーマ」を1つだけ選ぶ。残りは3ヶ月後の候補に。"),
        ("商品", "同じテーマの人がいて、私が出る意味ある？",
         "市場が大きい証拠。あなた個人の物語と言葉が、同じテーマでも違う角度を作る。"),
        ("商品", "価格をいくらにすればいいか分からない",
         "迷ったら2,980円。1,000〜5,000円がゼロイチの最適価格ゾーン。"),
        ("発信", "投稿ボタンが押せない",
         "誤字を1つ入れて投稿してみる。完璧じゃない投稿を意図的に出すと、次が楽になる。"),
        ("発信", "フォロワーゼロから誰に向けて？",
         "3ヶ月前の自分に向けて書く。1人に向けた言葉が未来の100人に届く。"),
        ("発信", "批判コメントが怖い",
         "フォロワー1,000人未満は来ません。来るなら影響力が育った証拠。今は心配無用。"),
        ("発信", "いいねが0で恥ずかしい",
         "見えていないだけ。投稿後はSNSを開かない。最初の30投稿は土壌づくり。"),
        ("発信", "自分の投稿、つまらない気がする",
         "つまらないと感じるのはあなただけ。下手でいい、本音だけ書く。"),
        ("販売", "商品ページに来てるのに買われない",
         "最初の3行と最後の3行を書き直す。中間は読まれてない。頭と尻尾だけ磨く。"),
        ("販売", "LINE登録は増えるのに買われない",
         "ステップ配信を見直す。商品予告→案内の感情の盛り上がりを作れているか。"),
        ("販売", "先行案内したのに反応なし",
         "1to1メッセージを5人に送る。個別のひとこえがない販売は初心者には難しい。"),
        ("販売", "価格が高いから売れないのかも",
         "値下げは最後の手段。先に得られるもの5個→8個に増やす。"),
        ("販売", "30日経ったのにゼロイチできなかった",
         "平均は60〜90日。違いは「あと60日続けるか」だけ。Day 5〜21をループ。"),
        ("こころ", "他のママと比べて落ち込む",
         "比較対象は1ヶ月前の自分だけ。「1ヶ月前の自分vs今」を書くと楽になる。"),
        ("こころ", "私には才能がない気がする",
         "才能でゼロイチする人は1%以下。99%は淡々と続けただけ。続ければ達成できる。"),
        ("こころ", "やる気が出ない日が3日続いてる",
         "休んでOK。休む日も計画の一部。週1の「サボる日」を最初から組み込む。"),
        ("こころ", "成功してる人を見ると苦しくなる",
         "その人をミュート／アンフォロー。比較で奮い立つはあなたには毒。"),
        ("こころ", "もうやめたい",
         "2週間完全休止。やめるかは2週間後に決める。即決でやめると後悔する。"),
        ("時間", "子どもが体調崩して1週間進まなかった",
         "1週間ぶん「やらない」を許可。罪悪感が次のさぼりを呼ぶ。再開日だけ決める。"),
        ("時間", "家事と育児で副業時間ゼロ",
         "30分の塊を諦めて、3分×10回に切り替える。スマホ完結タスクから消化。"),
        ("時間", "やることが多すぎて何から",
         "今日のDayだけ見る。それ以外は明日以降。情報遮断が前進の鍵。"),
        ("時間", "夜は眠すぎて進まない",
         "朝にずらす。子どもが起きる15分前。集中力は朝が3倍。"),
        ("時間", "3週間続けたけど飽きた",
         "型を変える。Threadsの5型を1週間ごとにローテ。飽きはサインじゃなく刺激不足。"),
        ("家族", "夫に話したら反対されそう",
         "家族に話すのは初販売の後。実績ゼロでの相談は反対されやすい。結果を持って報告。"),
        ("家族", "親に「主婦が副業なんて」と言われた",
         "説得しない。結果で見せる。納税できる収入になったとき親は黙る。"),
        ("家族", "ママ友に副業のこと知られたくない",
         "Threadsはニックネーム＋顔出しなしOK。インスタと完全分離（別アカ）。"),
        ("家族", "相談できる人が周りにいない",
         "このシートが相談相手。詰まったらここを毎回開けばOK。"),
        ("家族", "友達がもっと稼いでて惨め",
         "友達はあなたの過去、SNSは表面を見せている。比較対象が不公平。"),
    ]
    last = None
    for cat, q, a in helps:
        write(ws, r, 1, cat if cat != last else "",
              f=font(10, italic=True, color=C["ink_pale"]),
              a=align("center", "top"))
        write(ws, r, 2, q,
              f=font(11, bold=True, color=C["rule_pink_dk"]),
              a=align("left", "top", indent=1),
              fl=fill(C["rule_pink"]))
        write(ws, r, 3, a,
              f=font(11, color=C["rule_mint_dk"]),
              a=align("left", "top", indent=1),
              fl=fill(C["rule_mint"]))
        for c in range(1, 4):
            ws.cell(row=r, column=c).border = Border(bottom=thin(C["line"]))
        ws.row_dimensions[r].height = 50
        last = cat
        r += 1

    r += 1
    r = closing(ws, r,
        "ぜんぶ「あるある」です。\n"
        "あなただけじゃない。明日もまた、ここで会えますように。",
        col_end=3, height=60)

    ws.freeze_panes = "A5"


# ============================================================
# Tab 12: ひとりごとメモ
# ============================================================
def t_diary(wb):
    ws = wb.create_sheet("12_ひとりごとメモ")
    setup(ws, {"A": 12, "B": 70})

    r = page_title(ws, 1, "DIARY",
                   "ひとりごとメモ",
                   "気持ちの吐き出し・気づき・愚痴、何でも自由に書く場所です。",
                   col_end=2)

    r = lead(ws, r,
        "副業を進める中で、心がざわつくことが必ずあります。そんなときはここに書いて、気持ちを整理してください。",
        col_end=2, height=44)

    headers = ["日付", "今日のひとりごと"]
    for i, h in enumerate(headers, start=1):
        write(ws, r, i, h,
              f=font(10, bold=True, color="FFFFFF"),
              a=align("center", "center"),
              fl=fill(C["ink_soft"]))
    ws.row_dimensions[r].height = 26
    r += 1

    for _ in range(40):
        write(ws, r, 1, "",
              fl=fill(C["input"]),
              border=BORDER_INPUT,
              a=align("center", "top"))
        write(ws, r, 2, "",
              fl=fill(C["input"]),
              border=BORDER_INPUT,
              a=align("left", "top", indent=1))
        ws.row_dimensions[r].height = 50
        r += 1

    ws.freeze_panes = "A6"


# ============================================================
# main
# ============================================================
def main():
    wb = Workbook()
    wb.remove(wb["Sheet"])

    t_welcome(wb)
    t_glossary(wb)
    t_calendar(wb)
    t_day0(wb)
    t_mindset(wb)
    t_product(wb)
    t_line(wb)
    t_base(wb)
    t_threads(wb)
    t_funnel(wb)
    t_sales(wb)
    t_help(wb)
    t_diary(wb)

    out = "/home/user/meal-coach/spreadsheet/0to1_workbook_v3.xlsx"
    wb.save(out)
    print(f"saved: {out}")
    print(f"sheets: {len(wb.sheetnames)}")
    for n in wb.sheetnames:
        print(" -", n)


if __name__ == "__main__":
    main()
