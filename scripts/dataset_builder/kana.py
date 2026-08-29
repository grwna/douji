"""Romaji to Katakana and Hiragana converters for Unihan readings."""

ROMAJI_KATAKANA = {
    "A": "ア", "I": "イ", "U": "ウ", "E": "エ", "O": "オ",
    "KA": "カ", "KI": "キ", "KU": "ク", "KE": "ケ", "KO": "コ",
    "SA": "サ", "SI": "シ", "SHI": "シ", "SU": "ス", "SE": "セ", "SO": "ソ",
    "TA": "タ", "TI": "チ", "CHI": "チ", "TSU": "ツ", "TU": "ツ", "TE": "テ", "TO": "ト",
    "NA": "ナ", "NI": "ニ", "NU": "ヌ", "NE": "ネ", "NO": "ノ",
    "HA": "ハ", "HI": "ヒ", "HU": "フ", "FU": "フ", "HE": "ヘ", "HO": "ホ",
    "MA": "マ", "MI": "ミ", "MU": "ム", "ME": "メ", "MO": "モ",
    "YA": "ヤ", "YU": "ユ", "YO": "ヨ",
    "RA": "ラ", "RI": "リ", "RU": "ル", "RE": "レ", "RO": "ロ",
    "WA": "ワ", "WI": "ヰ", "WE": "ヱ", "WO": "ヲ",
    "N": "ン",
    "GA": "ガ", "GI": "ギ", "GU": "グ", "GE": "ゲ", "GO": "ゴ",
    "ZA": "ザ", "ZI": "ジ", "JI": "ジ", "ZU": "ズ", "ZE": "ゼ", "ZO": "ゾ",
    "DA": "ダ", "DI": "ヂ", "DU": "ヅ", "DE": "デ", "DO": "ド",
    "BA": "バ", "BI": "ビ", "BU": "ブ", "BE": "ベ", "BO": "ボ",
    "PA": "パ", "PI": "ピ", "PU": "プ", "PE": "ペ", "PO": "ポ",
    "KYA": "キャ", "KYU": "キュ", "KYO": "キョ",
    "SHA": "シャ", "SHU": "シュ", "SHO": "ショ",
    "CHA": "チャ", "CHU": "チュ", "CHO": "チョ",
    "NYA": "ニャ", "NYU": "ニュ", "NYO": "ニョ",
    "HYA": "ヒャ", "HYU": "ヒュ", "HYO": "ヒョ",
    "MYA": "ミャ", "MYU": "ミュ", "MYO": "ミョ",
    "RYA": "リャ", "RYU": "リュ", "RYO": "リョ",
    "GYA": "ギャ", "GYU": "ギュ", "GYO": "ギョ",
    "JA": "ジャ", "JU": "ジュ", "JO": "ジョ",
    "BYA": "ビャ", "BYU": "ビュ", "BYO": "ビョ",
    "PYA": "ピャ", "PYU": "ピュ", "PYO": "ピョ",
}

ROMAJI_HIRAGANA = {
    "a": "あ", "i": "い", "u": "う", "e": "え", "o": "お",
    "ka": "か", "ki": "き", "ku": "く", "ke": "ケ", "ko": "こ",
    "sa": "さ", "si": "し", "shi": "し", "su": "す", "se": "せ", "so": "そ",
    "ta": "た", "ti": "ち", "chi": "ち", "tsu": "つ", "tu": "つ", "te": "て", "to": "と",
    "na": "な", "ni": "に", "nu": "ぬ", "ne": "ね", "no": "の",
    "ha": "は", "hi": "ヒ", "hu": "ふ", "fu": "ふ", "he": "へ", "ho": "ほ",
    "ma": "ま", "mi": "み", "mu": "む", "me": "め", "mo": "も",
    "ya": "や", "yu": "ゆ", "yo": "よ",
    "ra": "ら", "ri": "り", "ru": "る", "re": "れ", "ro": "ろ",
    "wa": "わ", "wi": "ゐ", "we": "ゑ", "wo": "を",
    "n": "ん",
    "ga": "が", "gi": "ぎ", "gu": "ぐ", "ge": "げ", "go": "ご",
    "za": "ざ", "zi": "じ", "ji": "じ", "zu": "ず", "ze": "ぜ", "zo": "ぞ",
    "da": "だ", "di": "ぢ", "du": "づ", "de": "で", "do": "ど",
    "ba": "ば", "bi": "び", "bu": "ぶ", "be": "べ", "bo": "ぼ",
    "pa": "ぱ", "pi": "ぴ", "pu": "ぷ", "pe": "ぺ", "po": "ぽ",
    "kya": "きゃ", "kyu": "きゅ", "kyo": "きょ",
    "sha": "しゃ", "shu": "しゅ", "sho": "しょ",
    "cha": "ちゃ", "chu": "ちゅ", "cho": "ちょ",
    "nya": "にゃ", "nyu": "にゅ", "nyo": "にょ",
    "hya": "ひゃ", "hyu": "ひゅ", "hyo": "ひょ",
    "mya": "みゃ", "myu": "みゅ", "myo": "みょ",
    "rya": "りゃ", "ryu": "りゅ", "ryo": "りょ",
    "gya": "ぎゃ", "gyu": "ぎゅ", "gyo": "ぎょ",
    "ja": "じゃ", "ju": "じゅ", "jo": "じょ",
    "bya": "ビャ", "byu": "びゅ", "byo": "びょ",
    "pya": "ぴゃ", "pyu": "ぴゅ", "pyo": "ぴょ",
}


def romaji_to_katakana(romaji: str) -> str:
    romaji = romaji.upper()
    result = []
    i = 0
    while i < len(romaji):
        matched = False
        for length in (3, 2, 1):
            chunk = romaji[i:i + length]
            if chunk in ROMAJI_KATAKANA:
                result.append(ROMAJI_KATAKANA[chunk])
                i += length
                matched = True
                break
        if not matched:
            if i + 1 < len(romaji) and romaji[i] == romaji[i + 1] and romaji[i] not in "AEIOUN":
                result.append("ッ")
                i += 1
            else:
                i += 1
    return "".join(result)


def romaji_to_hiragana(romaji: str) -> str:
    parts = romaji.split(".")
    converted_parts = []
    for part in parts:
        result = []
        text = part.lower()
        idx = 0
        while idx < len(text):
            matched = False
            for length in (3, 2, 1):
                chunk = text[idx:idx + length]
                if chunk in ROMAJI_HIRAGANA:
                    result.append(ROMAJI_HIRAGANA[chunk])
                    idx += length
                    matched = True
                    break
            if not matched:
                if idx + 1 < len(text) and text[idx] == text[idx + 1] and text[idx] not in "aeioun":
                    result.append("っ")
                    idx += 1
                else:
                    result.append(text[idx])
                    idx += 1
        converted_parts.append("".join(result))
    return ".".join(converted_parts)
