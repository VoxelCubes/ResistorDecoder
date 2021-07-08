import re



def parse_code(code, short_underline, long_underline):
    # Top line is irrelevant, as it marks the same cases as the milli marker.
    # Return type tuple: value, tolerance, is_standardized_tolerance
    # For many codes there is no standardized tolerance value. Refer to the part's spec sheet in those cases.

    tolerance_is_standardized = False
    tolerance = 5
    if short_underline:
        tolerance = 1
        tolerance_is_standardized = True

    if len(code) > 3:
        tolerance = 1

    if long_underline:
        code = "R" + code

    # Test Length. Reject anything under 3 if it isn't a jumper
    # Try to parse jumper
    if re.fullmatch(r"0+", code):
        return 0, tolerance, tolerance_is_standardized
    elif not (2 < len(code) < 5):
        return None

    # Try to parse EIA-96
    if match := re.fullmatch(r"([0][1-9]|[1-8][0-9]|[9][0-6])([ZYRXSABHCDEF])", code, re.IGNORECASE):
        # Return value and tolerance, eia-96 codes prescribe 1% tolerance
        return parse_eia(match), 1, True
    # Try to parse regular code
    elif match := re.fullmatch(r"(\d+)(\d)", code):
        return parse_regular_code(match), tolerance, tolerance_is_standardized
    # Try to parse decimal marker
    elif match := re.fullmatch(r"(\d*)[R](\d*)", code, re.IGNORECASE):
        return parse_decimal_code(match), tolerance, tolerance_is_standardized
    # Try to parse milli decimal marker
    elif match := re.fullmatch(r"(\d*)[ML](\d*)", code, re.IGNORECASE):
        return parse_milli_code(match), tolerance, tolerance_is_standardized
    else:
        return None



def parse_regular_code(match):
    digits = int(match.group(1))
    multiplier = 10 ** int(match.group(2))
    value = digits * multiplier
    return value



def parse_eia(match):
    digits = eia_digit_lookup(match.group(1))
    multiplier = eia_letter_lookup(match.group(2))
    value = digits * multiplier
    return value



def parse_decimal_code(match):
    if match.group(1):
        digits_left = match.group(1)
    else:
        digits_left = 0

    if match.group(2):
        digits_right = match.group(2)
    else:
        digits_right = 0

    value = float(f"{digits_left}.{digits_right}")
    return value



def parse_milli_code(match):
    value = parse_decimal_code(match)
    return value * 0.001



def eia_letter_lookup(key):
    table = {
        "Z": 0.001,
        "Y": 0.01,
        "R": 0.01,
        "X": 0.1,
        "S": 0.1,
        "A": 1,
        "B": 10,
        "H": 10,
        "C": 100,
        "D": 1000,
        "E": 10000,
        "F": 100000
    }
    return table[key]



def eia_digit_lookup(key):
    table = {
        "01": 100,
        "02": 102,
        "03": 105,
        "04": 107,
        "05": 110,
        "06": 113,
        "07": 115,
        "08": 118,
        "09": 121,
        "10": 124,
        "11": 127,
        "12": 130,
        "13": 133,
        "14": 137,
        "15": 140,
        "16": 143,
        "17": 147,
        "18": 150,
        "19": 154,
        "20": 158,
        "21": 162,
        "22": 165,
        "23": 169,
        "24": 174,
        "25": 178,
        "26": 182,
        "27": 187,
        "28": 191,
        "29": 196,
        "30": 200,
        "31": 205,
        "32": 210,
        "33": 215,
        "34": 221,
        "35": 226,
        "36": 232,
        "37": 237,
        "38": 243,
        "39": 249,
        "40": 255,
        "41": 261,
        "42": 267,
        "43": 274,
        "44": 280,
        "45": 287,
        "46": 294,
        "47": 301,
        "48": 309,
        "49": 316,
        "50": 324,
        "51": 332,
        "52": 340,
        "53": 348,
        "54": 357,
        "55": 365,
        "56": 374,
        "57": 383,
        "58": 392,
        "59": 402,
        "60": 412,
        "61": 422,
        "62": 432,
        "63": 442,
        "64": 453,
        "65": 464,
        "66": 475,
        "67": 487,
        "68": 499,
        "69": 511,
        "70": 523,
        "71": 536,
        "72": 549,
        "73": 562,
        "74": 576,
        "75": 590,
        "76": 604,
        "77": 619,
        "78": 634,
        "79": 649,
        "80": 665,
        "81": 681,
        "82": 698,
        "83": 715,
        "84": 732,
        "85": 750,
        "86": 768,
        "87": 787,
        "88": 806,
        "89": 825,
        "90": 845,
        "91": 866,
        "92": 887,
        "93": 909,
        "94": 931,
        "95": 953,
        "96": 976
    }
    return table[key]
