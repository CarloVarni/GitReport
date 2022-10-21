from GitMergeRequest import git_merge_request    
from TimeFormat import time_format
from GitUser import git_user
import re

class gitlab_merge_request(git_merge_request):
    def __init__(self,
                 id: int,
                 merge_request_info: dict,
                 merge_request_diff: dict = None):
        assert isinstance(id, int)
        assert isinstance(merge_request_info, dict)
        assert id == int(merge_request_info['iid'])
        assert merge_request_diff is None or isinstance(merge_request_diff, dict)

        super().__init__(id=id,
                         web_url = merge_request_info['web_url'],
                         state = merge_request_info['state'],
                         title =  merge_request_info['title'],
                         description = merge_request_info['description'],
                         author = git_user(merge_request_info['author']['username'],
                                           merge_request_info['author']['web_url']),
                         merged_by = git_user(merge_request_info['merged_by']['username'] ,
                                              merge_request_info['merged_by']['web_url']),
                         created_at = time_format(merge_request_info['created_at']),
                         merged_at = time_format(merge_request_info['merged_at']))
        
        self.__info: dict = merge_request_info
        self.__acts_tag_change: tuple = self.check_changes(merge_request_diff)

    @property
    def acts_tag_change(self) -> tuple:
        return self.__acts_tag_change

    def changes_acts_tag(self) -> bool:
        return len(self.__acts_tag_change) != 0
        
    def __str__(self):
        message = f"Merge Request [id: {self.__id}]\n"
        message += f"   * web url: {self.__web_url}\n"
        message += f"   * state: {self.__state}\n"
        message += f"   * created at: {self.__created_at}\n"
        message += f"   * author: {self.__author}\n"
        message += f"   * merged by: {self.__merged_by}\n"
        message += f"   * merged at: {self.__merged_at}\n" 
        message += f"   * title: {self.__title}\n"
        message += f"   * description: \n{self.__description}\n"
        return message

    def dump_latex(self):
        message = f"\\textbf{{{self.title}}} [\\href{{{self.web_url}}}{{MR !{self.id}}}]\n\n"
        message += "{\scriptsize\n"
        message += f"created by \\href{{{self.author.web_url}}}{{@{self.author.username}}} [{self.created_at}]\n\n"
        message += f"merged by \\href{{{self.merged_by.web_url}}}{{@{self.merged_by.username}}} [{self.merged_at}]\n"
        message += "}\n\n"
        return message

    def check_changes(self,
                      changes: dict) -> tuple:
        output = []
        if changes is None:
            return output

        mr_changes = changes['changes']
        for changes in mr_changes:
            if changes['old_path'] != "Projects/Athena/build_externals.sh":
                continue
            if changes['new_path'] != "Projects/Athena/build_externals.sh":
                continue

            diff = changes['diff']
            match_removal = re.findall('\-  +\-DATLAS_ACTS_TAG="(.*)"', diff)
            match_addition = re.findall('\+ +\-DATLAS_ACTS_TAG="(.*)"', diff)
            if len(match_removal) != 0 and len(match_addition) != 0:
                output = [match_removal[0], match_addition[0]]

        return output
