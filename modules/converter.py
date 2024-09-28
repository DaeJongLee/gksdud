import re

ENG_KEY = "rRseEfaqQtTdwWczxvgkoiOjpuPhynbml"
KOR_KEY = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ"
CHO_DATA = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
JUNG_DATA = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
JONG_DATA = "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"

def run(argv):
    query = argv[0] if argv else ""
    try:
        query = query.strip()
        return convert(query)
    except Exception as err:
        print(err)
        return False

def is_upper_string(value):
    return value.isupper()

def convert(query):
    if is_eng(query):
        if is_upper_string(query[0]):
            query = query[0].lower() + query[1:]
        return eng_type_to_kor(query)
    return kor_type_to_eng(query)

def is_eng(query):
    pattern = re.compile(r'^[a-zA-Z]+$')
    return pattern.match(query[0]) is not None

def eng_type_to_kor(src):
    res = ""
    if len(src) == 0:
        return res

    n_cho, n_jung, n_jong = -1, -1, -1

    for ch in src:
        p = ENG_KEY.find(ch)
        if p == -1:  # 영자판이 아님
            if n_cho != -1:
                if n_jung != -1:
                    res += make_hangul(n_cho, n_jung, n_jong)
                else:
                    res += CHO_DATA[n_cho]
            elif n_jung != -1:
                res += JUNG_DATA[n_jung]
            elif n_jong != -1:
                res += JONG_DATA[n_jong]
            n_cho, n_jung, n_jong = -1, -1, -1
            res += ch
        elif p < 19:  # 자음
            if n_jung != -1:
                if n_cho == -1:
                    res += JUNG_DATA[n_jung]
                    n_cho = CHO_DATA.find(KOR_KEY[p])
                    n_jung = -1
                else:
                    if n_jong == -1:
                        n_jong = JONG_DATA.find(KOR_KEY[p])
                        if n_jong == -1:
                            res += make_hangul(n_cho, n_jung, n_jong)
                            n_cho = CHO_DATA.find(KOR_KEY[p])
                            n_jung = -1
                    elif n_jong == 0 and p == 9:
                        n_jong = 2
                    elif n_jong == 3 and p == 12:
                        n_jong = 4
                    elif n_jong == 3 and p == 18:
                        n_jong = 5
                    elif n_jong == 7 and p == 0:
                        n_jong = 8
                    elif n_jong == 7 and p == 6:
                        n_jong = 9
                    elif n_jong == 7 and p == 7:
                        n_jong = 10
                    elif n_jong == 7 and p == 9:
                        n_jong = 11
                    elif n_jong == 7 and p == 16:
                        n_jong = 12
                    elif n_jong == 7 and p == 17:
                        n_jong = 13
                    elif n_jong == 7 and p == 18:
                        n_jong = 14
                    elif n_jong == 16 and p == 9:
                        n_jong = 17
                    else:
                        res += make_hangul(n_cho, n_jung, n_jong)
                        n_cho = CHO_DATA.find(KOR_KEY[p])
                        n_jung, n_jong = -1, -1
            else:
                if n_cho == -1:
                    if n_jong != -1:
                        res += JONG_DATA[n_jong]
                        n_jong = -1
                    n_cho = CHO_DATA.find(KOR_KEY[p])
                elif n_cho == 0 and p == 9:
                    n_cho, n_jong = -1, 2
                elif n_cho == 2 and p == 12:
                    n_cho, n_jong = -1, 4
                elif n_cho == 2 and p == 18:
                    n_cho, n_jong = -1, 5
                elif n_cho == 5 and p == 0:
                    n_cho, n_jong = -1, 8
                elif n_cho == 5 and p == 6:
                    n_cho, n_jong = -1, 9
                elif n_cho == 5 and p == 7:
                    n_cho, n_jong = -1, 10
                elif n_cho == 5 and p == 9:
                    n_cho, n_jong = -1, 11
                elif n_cho == 5 and p == 16:
                    n_cho, n_jong = -1, 12
                elif n_cho == 5 and p == 17:
                    n_cho, n_jong = -1, 13
                elif n_cho == 5 and p == 18:
                    n_cho, n_jong = -1, 14
                elif n_cho == 7 and p == 9:
                    n_cho, n_jong = -1, 17
                else:
                    res += CHO_DATA[n_cho]
                    n_cho = CHO_DATA.find(KOR_KEY[p])
        else:  # 모음
            if n_jong != -1:
                if n_jong == 2:
                    n_jong, new_cho = 0, 9
                elif n_jong == 4:
                    n_jong, new_cho = 3, 12
                elif n_jong == 5:
                    n_jong, new_cho = 3, 18
                elif n_jong == 8:
                    n_jong, new_cho = 7, 0
                elif n_jong == 9:
                    n_jong, new_cho = 7, 6
                elif n_jong == 10:
                    n_jong, new_cho = 7, 7
                elif n_jong == 11:
                    n_jong, new_cho = 7, 9
                elif n_jong == 12:
                    n_jong, new_cho = 7, 16
                elif n_jong == 13:
                    n_jong, new_cho = 7, 17
                elif n_jong == 14:
                    n_jong, new_cho = 7, 18
                elif n_jong == 17:
                    n_jong, new_cho = 16, 9
                else:
                    new_cho = CHO_DATA.find(JONG_DATA[n_jong])
                    n_jong = -1
                if n_cho != -1:
                    res += make_hangul(n_cho, n_jung, n_jong)
                else:
                    res += JONG_DATA[n_jong]
                n_cho = new_cho
                n_jung, n_jong = -1, -1
            if n_jung == -1:
                n_jung = JUNG_DATA.find(KOR_KEY[p])
            elif n_jung == 8 and p == 19:
                n_jung = 9
            elif n_jung == 8 and p == 20:
                n_jung = 10
            elif n_jung == 8 and p == 32:
                n_jung = 11
            elif n_jung == 13 and p == 23:
                n_jung = 14
            elif n_jung == 13 and p == 24:
                n_jung = 15
            elif n_jung == 13 and p == 32:
                n_jung = 16
            elif n_jung == 18 and p == 32:
                n_jung = 19
            else:
                if n_cho != -1:
                    res += make_hangul(n_cho, n_jung, n_jong)
                    n_cho = -1
                else:
                    res += JUNG_DATA[n_jung]
                n_jung = -1
                res += KOR_KEY[p]

    if n_cho != -1:
        if n_jung != -1:
            res += make_hangul(n_cho, n_jung, n_jong)
        else:
            res += CHO_DATA[n_cho]
    elif n_jung != -1:
        res += JUNG_DATA[n_jung]
    elif n_jong != -1:
        res += JONG_DATA[n_jong]

    return res

def make_hangul(n_cho, n_jung, n_jong):
    return chr(0xac00 + n_cho * 21 * 28 + n_jung * 28 + n_jong + 1)

def kor_type_to_eng(src):
    res = ""
    if len(src) == 0:
        return res

    for ch in src:
        n_code = ord(ch)
        n_cho = CHO_DATA.find(ch)
        n_jung = JUNG_DATA.find(ch)
        n_jong = JONG_DATA.find(ch)
        arr_key_index = [-1] * 5

        if 0xac00 <= n_code <= 0xd7a3:
            n_code -= 0xac00
            arr_key_index[0] = n_code // (21 * 28)
            arr_key_index[1] = (n_code // 28) % 21
            arr_key_index[3] = n_code % 28 - 1
        elif n_cho != -1:
            arr_key_index[0] = n_cho
        elif n_jung != -1:
            arr_key_index[1] = n_jung
        elif n_jong != -1:
            arr_key_index[3] = n_jong
        else:
            res += ch

        if arr_key_index[1] != -1:
            if arr_key_index[1] == 9:
                arr_key_index[1:3] = [27, 19]
            elif arr_key_index[1] == 10:
                arr_key_index[1:3] = [27, 20]
            elif arr_key_index[1] == 11:
                arr_key_index[1:3] = [27, 32]
            elif arr_key_index[1] == 14:
                arr_key_index[1:3] = [29, 23]
            elif arr_key_index[1] == 15:
                arr_key_index[1:3] = [29, 24]
            elif arr_key_index[1] == 16:
                arr_key_index[1:3] = [29, 32]
            elif arr_key_index[1] == 19:
                arr_key_index[1:3] = [31, 32]
            else:
                arr_key_index[1] = KOR_KEY.find(JUNG_DATA[arr_key_index[1]])
                arr_key_index[2] = -1

        if arr_key_index[3] != -1:
            if arr_key_index[3] == 2:
                arr_key_index[3:5] = [0, 9]
            elif arr_key_index[3] == 4:
                arr_key_index[3:5] = [2, 12]
            elif arr_key_index[3] == 5:
                arr_key_index[3:5] = [2, 18]
            elif arr_key_index[3] == 8:
                arr_key_index[3:5] = [5, 0]
            elif arr_key_index[3] == 9:
                arr_key_index[3:5] = [5, 6]
            elif arr_key_index[3] == 10:
                arr_key_index[3:5] = [5, 7]
            elif arr_key_index[3] == 11:
                arr_key_index[3:5] = [5, 9]
            elif arr_key_index[3] == 12:
                arr_key_index[3:5] = [5, 16]
            elif arr_key_index[3] == 13:
                arr_key_index[3:5] = [5, 17]
            elif arr_key_index[3] == 14:
                arr_key_index[3:5] = [5, 18]
            elif arr_key_index[3] == 17:
                arr_key_index[3:5] = [7, 9]
            else:
                arr_key_index[3] = KOR_KEY.find(JONG_DATA[arr_key_index[3]])
                arr_key_index[4] = -1

        for j in arr_key_index:
            if j != -1:
                res += ENG_KEY[j]

    return res

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(run(sys.argv[1:]))
    else:
        print("Usage: python script.py <text_to_convert>")