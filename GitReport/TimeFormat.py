import re

class time_format:
    def __init__(self,
                 time_format: str):
        assert isinstance(time_format, str)

        self.__date: str = ""
        self.__hours: str = ""
        time_match = re.findall("(.*)T(.*)", time_format)
        if len(time_match) != 1:
            raise ValueError(f"Time format is not correct: {time_format}")

        self.__date, self.__hours = time_match[0]

    def __str__(self) -> str:
        return f"{self.date} at {self.hours}"

    @property
    def date(self) -> str:
        return self.__date

    @property
    def hours(self) -> str:
        return self.__hours
