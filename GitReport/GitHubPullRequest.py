from GitReport.GitMergeRequest import git_merge_request
from GitReport.TimeFormat import time_format
from GitReport.GitUser import git_user

class github_pull_request(git_merge_request):
    def __init__(self,
                 id: int,
                 merge_request_info: dict,
                 sha: str):
        assert isinstance(id, int)
        assert isinstance(merge_request_info, dict)
        assert id == int(merge_request_info['number'])
        assert isinstance(sha, str)
        
        super().__init__(id=id,
                         web_url=merge_request_info['html_url'],
                         state=merge_request_info['state'],
                         draft=merge_request_info['draft'],
                         title=merge_request_info['title'],
                         description=merge_request_info['body'],
                         author=git_user(merge_request_info['user']['login'],
                                         merge_request_info['user']['html_url']),
                         merged_by=git_user(merge_request_info['merged_by']['login'],
                                            merge_request_info['merged_by']['html_url']),
                         created_at=time_format(merge_request_info['created_at']),
                         merged_at=time_format(merge_request_info['merged_at']))

        self.__commit: str = sha
        self.__commit_url: str = f'https://github.com/acts-project/acts/commit/{sha}'
        self.__info: dict = merge_request_info

    @property
    def info(self) -> dict:
        return self.__info

    @property
    def commit(self) -> str:
        return self.__commit

    @property
    def commit_url(self) -> str:
        return self.__commit_url
    
    def __str__(self) -> str:
        message = f"Pull Request [id: {self.id}] ({self.commit})\n"
        message += f"   * web url: {self.web_url}\n"
        message += f"   * author: {self.author}\n"
        message += f"   * title: {self.title}\n"
        message += f"   * description: \n{self.description}\n"
        return message
    
    def dump_latex(self):
        message = f"\\textbf{{{self.title}}}"
        if self.id != 0:
            message += f" [\\href{{{self.web_url}}}{{PR \#{self.id}}}]" 
        message += f" (\\href{{{self.commit_url}}}{{{self.commit}}})\n\n"
        message += "{\scriptsize\n"
        message += f"created by \\href{{{self.author.web_url}}}{{@{self.author.username}}} [{self.created_at}]\n\n"
        if self.id != 0:
            message += f"merged by \\href{{{self.merged_by.web_url}}}{{@{self.merged_by.username}}} [{self.merged_at}]\n"
        message += "}\n\n"
        return message
    
