from GitReport.GitMergeRequest import git_merge_request
from GitReport.TimeFormat import time_format
from GitReport.GitUser import git_user

class github_pull_request(git_merge_request):
    def __init__(self,
                 id: int,
                 merge_request_info: dict):
        assert isinstance(id, int)
        assert isinstance(merge_request_info, dict)
        assert id == int(merge_request_info['number'])

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
        
        self.__info: dict = merge_request_info
        
    @property
    def info(self) -> dict:
        return self.__info
        
    def __str__(self) -> str:
        message = f"Pull Request [id: {self.id}]\n"
        message += f"   * web url: {self.web_url}\n"
        message += f"   * author: {self.author}\n"
        message += f"   * title: {self.title}\n"
        message += f"   * description: \n{self.description}\n"
        return message
    
    def dump_latex(self):
        message = f"\\textbf{{{self.title}}} [\\href{{{self.web_url}}}{{PR \#{self.id}}}]\n\n"
        message += "{\scriptsize\n"
        message += f"created by \\href{{{self.author.web_url}}}{{@{self.author.username}}} [{self.created_at}]\n\n"
        message += f"merged by \\href{{{self.merged_by.web_url}}}{{@{self.merged_by.username}}} [{self.merged_at}]\n"
        message += "}\n\n"
        return message
    
