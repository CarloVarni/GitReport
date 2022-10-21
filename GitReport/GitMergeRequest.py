from GitReport.TimeFormat import time_format
from GitReport.GitUser import git_user

class git_merge_request:
    def __init__(self,
                 id: int,
                 web_url: str,
                 state: str,
                 title: str,
                 description: str,
                 author: git_user,
                 created_at: time_format,
                 merged_by: git_user = None,
                 merged_at: time_format = None):
        assert isinstance(id, int)
        assert isinstance(web_url, str)
        assert isinstance(state, str)
        assert isinstance(title, str)
        assert description is None or isinstance(description, str)
        assert isinstance(author, git_user)
        assert merged_by is None or isinstance(merged_by, git_user)
        assert isinstance(created_at, time_format)
        assert merged_at is None or isinstance(merged_at, time_format)
        
        self.__id: int = id
        self.__web_url: str = web_url
        self.__state: str = state
        self.__title: str = title
        self.__description: str = description
        self.__author: git_user = author
        self.__merged_by: git_user = merged_by
        self.__created_at: time_format = created_at
        self.__merged_at: time_format = merged_at

    def __str__(self) -> str:
        pass
    
    @property
    def id(self) -> int:
        return self.__id

    @property
    def web_url(self) -> str:
        return self.__web_url
    
    @property
    def info(self) -> dict:
        return self.__info
    
    @property
    def state(self) -> str:
        return self.__state

    @property
    def title(self) -> str:
        return self.__title

    @property
    def description(self) -> str:
        return self.__description

    @property
    def author(self) -> git_user:
        return self.__author

    @property
    def merged_by(self) -> git_user:
        return self.__merged_by

    @property
    def created_at(self) -> time_format:
        return self.__created_at

    @property
    def merged_at(self) -> time_format:
        return self.__merged_at

    def dump_latex(self) -> str:
        pass    

