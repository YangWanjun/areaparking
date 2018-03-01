hiragana = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをん"
katakana = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴ"
hankana = ""
suuji = "0123456789０１２３４５６７８９"


# 日本語文字列のソート
def sort_str(string, reverse=False):
    return "".join(sorted(string, reverse=reverse))


# ひらがなだけの文字列ならTrue
def ishira(strj):
    return all([ch in hiragana for ch in strj])


# カタカナだけの文字列ならTrue
def iskata(strj):
    return all([ch in katakana for ch in strj])


# カタカナ・ひらがなだけの文字列ならTrue
def iskatahira(strj):
    return all([ch in katakana or ch in hiragana for ch in strj])


# 漢字だけの文字列ならTrue
def iskanji(strj):
    return all(["一" <= ch <= "龥" for ch in strj])


# ひらがなをカタカナに直す
def kata_to_hira(strj):
    return "".join([chr(ord(ch) - 96) if ("ァ" <= ch <= "ン") else ch for ch in strj])


# ひらがなをカタカナに直す
def hira_to_kata(strj):
    return "".join([chr(ord(ch) + 96) if ("ぁ" <= ch <= "ん") else ch for ch in strj])


# 全角数字を半角数字に直す
def hankaku_suuji(strj):
    dic2 = str.maketrans("０１２３４５６７８９", "0123456789")
    return strj.translate(dic2)
