from gitlab import Gitlab
from GitReport.GitLabMergeRequest import gitlab_merge_request
from datetime import datetime

class gitlab_manager:
    def __init__(self,
                 gitlab_token: str,
                 repository: str,
                 project_id: int):

        self.__repository: str = repository
        self.__project_id: int = project_id
        self.__gitlab: Gitlab = Gitlab(repository,
                                       private_token=gitlab_token)
        self.__project = self.__gitlab.projects.get(self.__project_id)
        self.__changes_acts_tag: bool = False
        self.__acts_tag_changes: tuple = []

    @property
    def repository(self) -> str:
        return self.__repository

    @property
    def project_id(self) -> int:
        return self.__project_id

    @property
    def changes_acts_tag(self) -> bool:
        return self.__changes_acts_tag

    @property
    def acts_tag_changes(self) -> tuple:
        return self.__acts_tag_changes
    
    def get_merge_requests(self,
                           merged_after: str = "",
                           merged_before: str = "",
                           **kwargs) -> tuple:
        list_of_requests = self.__project.mergerequests.list(**kwargs)

        output = []
        for mr in list_of_requests:
            id = mr.attributes['iid']

            merged_at = mr.attributes['merged_at']
            if len(merged_after) != 0 and len(merged_before) != 0 and merged_at is not None:
                merged_at_datetime = datetime.fromisoformat(merged_at)
                merged_after_datetime = datetime.fromisoformat(merged_after)
                merged_before_datetime = datetime.fromisoformat(merged_before)
                if merged_after_datetime > merged_at_datetime:
                    continue
                if merged_before_datetime < merged_at_datetime:
                    continue
                
            merge_request = gitlab_merge_request(id,
                                                 mr.attributes,
                                                 mr.changes())
            output.append(merge_request)

            if merge_request.changes_acts_tag():
                self.__changes_acts_tag = True
                self.__acts_tag_changes += merge_request.acts_tag_change

        if self.changes_acts_tag:
            self.__acts_tag_changes = sorted(self.__acts_tag_changes)
        return output
