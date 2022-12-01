from github import Github
from GitReport.GitHubPullRequest import github_pull_request
from datetime import datetime
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
        info = []
        for el in body:
            print(el)
            match_string = "(.*?)(?:\(#(.*)\))?\s\(([^#@]+)\)\s\(@(.*)\)"
            match = re.findall(match_string, el)

            if len(match) != 1:
                continue
            if len(match[0]) != 4:
                continue
            toAdd = [match[0][0], match[0][1], match[0][2], match[0][3]]
            if len(toAdd[1]) == 0:
                toAdd[1] = '0' 
            toAdd[1] = int(toAdd[1])
            info.append(toAdd)

        for [title, id, sha, user] in info:
            pr = self.__project.get_pull(id).raw_data if id != 0 else {'number': id,
                                                                       'html_url': 'unknown',
                                                                       'state': 'merged',
                                                                       'draft': False,
                                                                       'title': title,
                                                                       'body': 'Not Found',
                                                                       'user': {'login': user,
                                                                                'html_url': f'https://github.com/{user}'},
                                                                       'merged_by': {'login': 'Not Known',
                                                                                     'html_url': 'https://github.com/Not Known'},
                                                                       'created_at': datetime.now().isoformat(),
                                                                       'merged_at': datetime.now().isoformat()}
            merge_request = github_pull_request(id, pr)
            output.append(merge_request)
        
        return output
