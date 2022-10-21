
class git_user:
    def __init__(self,
                 username: str,
                 web_url: str):
        assert isinstance(username, str)
        assert isinstance(web_url, str)

        self.__username: str = username
        self.__web_url: str = web_url

    def __str__(self):
        message = f"@{self.__username} [{self.__web_url}]"
        return message

    @property
    def username(self) -> str:
        return self.__username

    @property
    def web_url(self) -> str:
        return self.__web_url

