from github import Github
from GitReport.GitHubPullRequest import github_pull_request
import re

class github_manager:
    def __init__(self,
                 github_token: str,
                 repository: str):

        self.__repository: str = repository
        self.__github: Github = Github(github_token)
        self.__project = self.__github.get_repo(repository)

    @property
    def repository(self) -> str:
        return self.__repository

    def get_relevant_releases(self,
                              from_release: str,
                              to_release: str) -> tuple:
        assert from_release < to_release

        output = []
        if from_release == to_release:
            return output

        releases = self.__project.get_releases()
        for release in releases:
            tag_name = release.tag_name
            if tag_name > to_release:
                continue
            if tag_name <= from_release:
                continue
            output.append((tag_name, release.body))

        output = sorted(output,
                        key=lambda x: x[0],
                        reverse=False)
        return output

    def get_list_prs_for_release(self,
                                 tag_name: str,
                                 release_body: str) -> tuple:
        output = []

        body = release_body.split('\n')
        ids = []
        for el in body:
            match = re.findall("\(#(\\d+)\)", el)
            if len(match) != 1:
                continue
            ids.append(int(match[0]))

        for id in ids:
            pr = self.__project.get_pull(id).raw_data
            merge_request = github_pull_request(id, pr)
            output.append(merge_request)
        
        return output
        
    
