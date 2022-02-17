from ..language import Language
from ..rule import Rule

de = Language(
    lang="de",
    units={
        "Y": ["Jahr", "Jahre", "Jahren"],
        "M": ["Monat", "Monate", "Monaten"],
        "W": ["Wochen", "Wochen"],
        "D": ["Tag", "Tage", "Tagen"],
    },
    num_words=[
        "null",
        "ein",
        "zwei",
        "drei",
        "vier",
        "fünf",
        "sechs",
        "sieben",
        "acht",
        "neun",
        "zehn",
        "elf",
        "zwölf",
        "dreizehn",
        "vierzehn",
        "fünfzehn",
        "sechszehn",
        "siebzehn",
        "achtzehn",
        "neunzehn",
        "zwanzig",
    ],
    months=[
        ["Januar", "Jan"],
        ["Februar", "Feb"],
        ["März", "Mär"],
        ["April", "Apr"],
        ["Mai"],
        ["Juni", "Jun"],
        ["Juli", "Jul"],
        ["August", "Aug"],
        ["September", "Sep", "Sept"],
        ["Oktober", "Okt"],
        ["November", "Nov"],
        ["Dezember", "Dez"],
    ],
)
de.rules = [
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)\\.(1[0-2]|0?\\d)\\.([12]\\d{3})",
        pattern="%d.%m.%Y",
        tests=[("Heute ist 03.10.1999", 10, 20)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)\\.(1[0-2]|0?\\d)\\.(\\d{2})",
        pattern="%d.%m.%y",
        tests=[("Heute ist 03.10.99", 10, 18)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)/(1[0-2]|0?\\d)/([12]\\d{3})",
        pattern="%d/%m/%Y",
        tests=[("Heute ist 03/10/1999", 10, 20)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)/(1[0-2]|0?\\d)/(\\d{2})",
        pattern="%d/%m/%y",
        tests=[("Heute ist 03/10/99", 10, 18)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)-(1[0-2]|0?\\d)-(\\d{2})",
        pattern="%d-%m-%y",
        tests=[("Heute ist 03-10-99", 10, 18)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)-(1[0-2]|0?\\d)-([12]\\d{3})",
        pattern="%d-%m-%Y",
        tests=[("Heute ist 03-10-1999", 10, 20)],
    ),
    Rule(
        regex=f"([0-2]?\\d|30|31)\\.\\s+({de.get_month_re()})\\s+([12]\\d{{3}})",
        pattern="%d. %b %Y",
        tests=[
            ("Heute ist 03. Januar 1999", 10, 25),
            ("Heute ist 03. Jan 1999", 10, 22),
        ],
    ),
    Rule(
        regex=f"([0-2]?\\d|30|31)\\.\\s+({de.get_month_re()})\\s+(\\d{{2}})",
        pattern="%d. %B %y",
        tests=[("Heute ist 03. Januar 99", 10, 23), ("Heute ist 03. Jan 99", 10, 20)],
    ),
    Rule(
        regex=f"({de.get_month_re()})\\s+([12]\\d{{3}})",
        pattern="%B %Y",
        tests=[("Heute ist Januar 1999", 10, 21), ("Heute ist Jan 1999", 10, 18)],
    ),
    Rule(
        regex=f"({de.get_month_re()})\\s+(\\d{{2}})",
        pattern="%B %y",
        tests=[("Heute ist Januar 99", 10, 19), ("Heute ist Jan 99", 10, 16)],
    ),
]
