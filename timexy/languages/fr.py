from ..language import Language
from ..rule import Rule

fr = Language(
    lang="fr",
    units={
        "Y": ["an", "ans", "années"],
        "M": ["mois"],
        "W": ["semaine", "semaines"],
        "D": ["jour", "jours"],
    },
    num_words=[
        "zéro",
        "un",
        "deux",
        "trois",
        "quatre",
        "cinq",
        "six",
        "sept",
        "huit",
        "neuf",
        "dix",
        "onze",
        "douze",
        "treize",
        "quatorze",
        "quinze",
        "seize",
        "dix-sept",
        "dix-huit",
        "dix-neuf",
        "vingt",
    ],
    months=[
        ["janvier", "jan"],
        ["février", "fév"],
        ["mars", "mar"],
        ["avril", "avr"],
        ["mai"],
        ["juin"],
        ["juillet"],
        ["août"],
        ["septembre", "sep", "sept"],
        ["octobre", "oct"],
        ["novembre", "nov"],
        ["décembre", "déc"],
    ],
)
fr.rules = [
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)\\.(1[0-2]|0?\\d)\\.([12]\\d{3})",
        pattern="%d.%m.%Y",
        tests=[("Nous sommes le 03.10.1990", 15, 25)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)\\.(1[0-2]|0?\\d)\\.(\\d{2})",
        pattern="%d.%m.%y",
        tests=[("Nous sommes le 03.10.99", 15, 23)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)/(1[0-2]|0?\\d)/([12]\\d{3})",
        pattern="%d/%m/%Y",
        tests=[("Nous sommes le 03/10/1999", 15, 25)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)/(1[0-2]|0?\\d)/(\\d{2})",
        pattern="%d/%m/%y",
        tests=[("Nous sommes le 03/10/99", 15, 23)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)-(1[0-2]|0?\\d)-(\\d{2})",
        pattern="%d-%m-%y",
        tests=[("Nous sommes le 03-10-99", 15, 23)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)-(1[0-2]|0?\\d)-([12]\\d{3})",
        pattern="%d-%m-%Y",
        tests=[("Nous sommes le 03-10-1999", 15, 25)],
    ),
    Rule(
        regex=f"([0-2]?\\d|30|31)\\s+({fr.get_month_re()})\\s+([12]\\d{{3}})",
        pattern="%d %b %Y",
        tests=[
            ("Nous sommes le 03 janvier 1999", 15, 30),
            ("Nous sommes le 03 jan 1999", 15, 26),
            ("Nous sommes le 10 mai 2021 semaines", 15, 26),
        ],
    ),
    Rule(
        regex=f"([0-2]?\\d|30|31)\\s+({fr.get_month_re()})\\s+(\\d{{2}})",
        pattern="%d %B %y",
        tests=[
            ("Nous sommes le 03 janvier 99", 15, 28),
            ("Nous sommes le 03 jan 99", 15, 24),
        ],
    ),
    Rule(
        regex=f"({fr.get_month_re()})\\s+([12]\\d{{3}})",
        pattern="%B %Y",
        tests=[
            ("Nous sommes en janvier 1999", 15, 27),
            ("Nous sommes en jan 1999", 15, 23),
        ],
    ),
    Rule(
        regex=f"({fr.get_month_re()})\\s+(\\d{{2}})",
        pattern="%B %y",
        tests=[
            ("Nous sommes en janvier 99", 15, 25),
            ("Nous sommes en jan 99", 15, 21),
        ],
    ),
]
