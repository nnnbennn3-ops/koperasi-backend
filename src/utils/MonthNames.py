class IndonesianMonth:
    MONTHS = [
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    ]

    MONTH_TO_NUMBER = {}
    for index, name in enumerate(MONTHS, start=1):
        MONTH_TO_NUMBER[name.lower()] = index

    @classmethod
    def to_name(cls, month_number: int) -> str:
        if 1 <= month_number <= 12:
            return cls.MONTHS[month_number - 1]
        raise ValueError(f"Invalid month number: {month_number}")

    @classmethod
    def to_number(cls, month_name: str) -> int:
        if not month_name:
            raise ValueError("Month name cannot be empty")

        month = cls.MONTH_TO_NUMBER.get(month_name.lower())
        if not month:
            raise ValueError(f"Invalid month name: {month_name}")

        return month
