from faker import Faker

CARD_PREFIXES = {
    "Visa": 4,
    "MasterCard": 5,
    "American Express": 3,
    "Discover": 6,
    "JCB": 35,
    "Diners Club": 36,
    "Mir": 2
}

BANK_BINS = {
    "Sberbank": {
        "NSPK MIR": ["220100", "220220"],
        "MASTERCARD": ["519808", "522860", "527404", "530829"],
        "VISA": ["427610", "427609", "427612", "427616"]
    },
    "Alfa Bank": {
        "VISA": ["496014"]
    },
    "Tinkoff Bank": {
        "NSPK MIR": ["220070"],
        "MASTERCARD": ["553420", "553691", "555323", "548387"],
        "VISA": ["437772", "437773", "437783", "437784"]
    },
    "Raiffeisenbank": {
        "NSPK MIR": ["220030"],
        "MASTERCARD": ["510069", "510070", "515876", "528053", "528808", "537965"],
        "VISA": ["427474", "438420", "445977", "446916", "446917"]
    }
}

fake_ru = Faker('ru_RU')
fake_en = Faker('en_US')