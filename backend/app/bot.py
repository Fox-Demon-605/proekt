
def weather_reply(text: str) -> str:
    t = text.lower()
    if "москва" in t:
        return "Сегодня в Москве облачно, +12°C."
    if "питер" in t or "санкт" in t:
        return "В Санкт-Петербурге дождь, +10°C."
    if "завтра" in t:
        return "Завтра ожидается похолодание."
    return "Укажите город и день, например: Погода в Москве сегодня."
