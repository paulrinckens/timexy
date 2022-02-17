from ..language import Language
from ..rule import Rule

en = Language(
    lang="en",
    units={
        "Y": ["year", "years"],
        "M": ["month", "months"],
        "W": ["week", "weeks"],
        "D": ["day", "days"],
    },
    num_words=[
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
        "twenty",
    ],
    months=[
        ["January", "Jan"],
        ["February", "Feb"],
        ["March", "Mar"],
        ["April", "Apr"],
        ["May"],
        ["June", "Jun"],
        ["July", "Jul"],
        ["August", "Aug"],
        ["September", "Sep"],
        ["October", "Oct"],
        ["November", "Nov"],
        ["December", "Dec"],
    ],
)

en.rules = [
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)\\.(1[0-2]|0?\\d)\\.([12]\\d{3})",
        pattern="%d.%m.%Y",
        tests=[("Today is 03.10.1999", 9, 19)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)\\.(1[0-2]|0?\\d)\\.(\\d{2})",
        pattern="%d.%m.%y",
        tests=[("Today is 03.10.99", 9, 17), ("Today is 3.10.99", 9, 16)],
    ),
    Rule(
        regex="([0-2]?\\d|30|31)/(1[0-2]|0?\\d)/([12]\\d{3})",
        pattern="%d/%m/%Y",
        tests=[("Today is 03/10/1999", 9, 19), ("Today is 3/10/1999", 9, 18)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)/(1[0-2]|0?\\d)/(\\d{2})",
        pattern="%d/%m/%y",
        tests=[("Today is 03/10/99", 9, 17), ("Today is 3/10/99", 9, 16)],
    ),
    Rule(
        regex=f"([0-2]?\\d|30|31)/({en.get_month_re()})/(\\d{{2}})",
        pattern="%d/%b/%y",
        tests=[("Today is 03/Feb/99", 9, 18), ("Today is 3/Feb/99", 9, 17)],
    ),
    Rule(
        regex=f"([0-2]?\\d|30|31)/({en.get_month_re()})/([12]\\d{{3}})",
        pattern="%d/%b/%Y",
        tests=[("Today is 03/Feb/1999", 9, 20), ("Today is 3/Feb/1999", 9, 19)],
    ),
    Rule(
        regex="(?<![0-9])([12]\\d{3})/(1[0-2]|0?\\d)/([0-2]?\\d|30|31)",
        pattern="%Y/%m/%d",
        tests=[("Today is 1999/10/03", 9, 19), ("Today is 1999/10/3", 9, 18)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)-(1[0-2]|0?\\d)-([12]\\d{3})",
        pattern="%d-%m-%Y",
        tests=[("Today is 03-10-1999", 9, 19), ("Today is 3-10-1999", 9, 18)],
    ),
    Rule(
        regex="(?<![0-9])([0-2]?\\d|30|31)-(1[0-2]|0?\\d)-(\\d{2})",
        pattern="%d-%m-%y",
        tests=[("Today is 03-10-99", 9, 17), ("Today is 3-10-99", 9, 16)],
    ),
    Rule(
        regex=f"([0-2]?\\d|30|31)-({en.get_month_re()})-(\\d{{2}})",
        pattern="%d-%b-%y",
        tests=[
            ("Today is 03-Feb-99", 9, 18),
            ("Today is 3-Feb-99", 9, 17),
            ("Today is 3-FEB-99", 9, 17),
        ],
    ),
    Rule(
        regex=f"([0-2]?\\d|30|31)-({en.get_month_re()})-([12]\\d{{3}})",
        pattern="%d-%b-%Y",
        tests=[
            ("Today is 03-Feb-1999", 9, 20),
            ("Today is 3-Feb-1999", 9, 19),
            ("Today is 3-FEB-1999", 9, 19),
        ],
    ),
    Rule(
        regex=f"([12]\\d{{3}})-({en.get_month_re()})-([0-2]?\\d|30|31)",
        pattern="%Y-%b-%d",
        tests=[
            ("Today is 2018-Jun-04", 9, 20),
            ("Today is 2018-JUN-04", 9, 20),
            ("Today is 2018-Jun-4", 9, 19),
        ],
    ),
    Rule(
        regex="(?<![0-9])([12]\\d{3})-(1[0-2]|0?\\d)-([0-2]?\\d|30|31)",
        pattern="%Y-%m-%d",
        tests=[("Today is 1999-10-03", 9, 19), ("Today is 1999-10-3", 9, 18)],
    ),
    Rule(
        regex=f"([0-2]?\\d|30|31)\\.\\s+({en.get_month_re()})\\s+([12]\\d{{3}})",
        pattern="%d. %B %Y",
        tests=[
            ("Today is 03. January 1999", 9, 25),
            ("Today is 3. January 1999", 9, 24),
            ("Today is 3. JANUARY 1999", 9, 24),
            ("Today is 03. Jan 1999", 9, 21),
            ("Today is 3. Jan 1999", 9, 20),
            ("Today is 3. JAN 1999", 9, 20),
        ],
    ),
    Rule(
        regex=f"([0-2]?\\d|30|31)\\.\\s+({en.get_month_re()})\\s+(\\d{{2}})",
        pattern="%d. %B %y",
        tests=[
            ("Today is 03. January 99", 9, 23),
            ("Today is 3. January 99", 9, 22),
            ("Today is 3. JANUARY 99", 9, 22),
            ("Today is 03. Jan 99", 9, 19),
            ("Today is 3. Jan 99", 9, 18),
            ("Today is 3. JAN 99", 9, 18),
        ],
    ),
    Rule(
        regex=f"([0-2]?\\d|30|31)\\s+({en.get_month_re()})\\s+([12]\\d{{3}})",
        pattern="%d %b %Y",
        tests=[
            ("Today is 03 Jan 1999", 9, 20),
            ("Today is 3 Jan 1999", 9, 19),
            ("Today is 3 JAN 1999", 9, 19),
            ("Today is 03 January 1999", 9, 24),
            ("Today is 3 January 1999", 9, 23),
            ("Today is 3 JANUARY 1999", 9, 23),
        ],
    ),
    Rule(
        regex=f"([0-2]?\\d|30|31)\\s+({en.get_month_re()})\\s+(\\d{{2}})",
        pattern="%d %b %y",
        tests=[
            ("Today is 03 Jan 99", 9, 18),
            ("Today is 3 Jan 99", 9, 17),
            ("Today is 3 JAN 99", 9, 17),
            ("Today is 03 January 99", 9, 22),
            ("Today is 3 January 99", 9, 21),
            ("Today is 3 JANUARY 99", 9, 21),
        ],
    ),
    Rule(
        regex=f"({en.get_month_re()})\\s+([12]\\d{{3}})",
        pattern="%B %Y",
        tests=[
            ("Today is January 1999", 9, 21),
            ("Today is JANUARY 1999", 9, 21),
            ("Today is Jan 1999", 9, 17),
            ("Today is JAN 1999", 9, 17),
        ],
    ),
    Rule(
        regex=f"({en.get_month_re()})\\s+(\\d{{2}})",
        pattern="%B %y",
        tests=[
            ("Today is January 99", 9, 19),
            ("Today is JANUARY 99", 9, 19),
            ("Today is Jan 99", 9, 15),
            ("Today is JAN 99", 9, 15),
        ],
    ),
    Rule(
        regex=f"({en.get_month_re()})\\s([0-2]?\\d|30|31)\\,\\s+([12]\\d{{3}})",
        pattern="%b %d, %Y",
        tests=[
            ("Today is Jan 03, 1999", 9, 21),
            ("Today is JAN 03, 1999", 9, 21),
            ("Today is January 03, 1999", 9, 25),
            ("Today is JANUARY 03, 1999", 9, 25),
        ],
    ),
    Rule(
        regex=f"({en.get_month_re()})\\s([0-2]?\\d|30|31)\\s+([12]\\d{{3}})",
        pattern="%b %d %Y",
        tests=[
            ("Today is Jan 03 1999", 9, 20),
            ("Today is JAN 03 1999", 9, 20),
            ("Today is January 03 1999", 9, 24),
            ("Today is JANUARY 03 1999", 9, 24),
        ],
    ),
]
