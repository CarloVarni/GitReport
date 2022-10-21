from gitlab import Gitlab
from github import Github

from GitHubPullRequest import github_pull_request
from GitLabMergeRequest import gitlab_merge_request
from BeamerWriter import beamer_writer

from datetime import datetime
import re

import os
from dotenv import load_dotenv

def get_relevant_releases(acts_tag_changes,
                          releases) -> tuple:
    list_relevant_releases = []
    for release in releases:
        tag_name = release.tag_name
        if (tag_name > acts_tag_changes[len(acts_tag_changes) - 1]):
            continue
        if (tag_name <= acts_tag_changes[0]):
            continue
        list_relevant_releases.append( (tag_name, release.body))
    return list_relevant_releases
    
def get_list_prs_for_release(tag_name: str,
                             release_body: str,
                             repo) -> tuple:
    body = release_body.split('\n')
    ids = []
    for el in body:
        match = re.findall("\(#(\\d+)\)", el)
        if len(match) != 1:
            continue
        ids.append(int(match[0]))

    list_prs = []
    for id in ids:
        pr = repo.get_pull(id).raw_data
        merge_request = github_pull_request(id, pr)
        list_prs.append(merge_request)
    return list_prs


def main():
    gitlab_token = ""
    github_token = ""

    try:
        load_dotenv()
        gitlab_token = str(os.getenv('GITLAB_TOKEN'))
        github_token = str(os.getenv('GITHUB_TOKEN'))
    except Exception:
        print('Env variables are not properly set! Check the .env file is present and/or the env variables are set.')
        quit()
        
    # Athena
    Gitlab_repo = "https://gitlab.cern.ch"
    gl = Gitlab(Gitlab_repo, private_token=gitlab_token)
    athena_project = gl.projects.get(53790)

    before_time = datetime.today()
    after_time = datetime(2022, 10, 8)

    merged_with_label = athena_project.mergerequests.list(state='merged',
                                                          labels='ACTS,master',
                                                          created_after=after_time.isoformat(),
                                                          created_before=before_time.isoformat(),
                                                          iterator=True)
    print(f"Found {len(merged_with_label)} merged MRs in this period with an ACTS label ...")

    acts_tag_is_changed = False
    acts_tag_changes = []
    
    list_merged_mrs_summary = []
    for mr in merged_with_label:
        id = mr.attributes['iid']
        merge_request = gitlab_merge_request(id,
                                             mr.attributes,
                                             mr.changes())
        list_merged_mrs_summary.append(merge_request)

        if merge_request.changes_acts_tag():
            acts_tag_is_changed = True
            acts_tag_changes += merge_request.acts_tag_change
        
    bwriter = beamer_writer("Report-Acts-Athena.tek",
                            title="Acts-Athena integration, MRs report",
                            author="carlo.varni",
                            date="21 October 2022")

    bwriter.add_data_group(title="Merged MRs with ACTS targeting master",
                           subtitle=f"Period: {after_time.isoformat()} -- {before_time.isoformat()}",
                           collection=list_merged_mrs_summary)

    acts_tag_changes = sorted(acts_tag_changes)
    print('acts_tag_is_changed:', acts_tag_is_changed)
    print('acts_tag_changes:', acts_tag_changes)


    if acts_tag_is_changed:
        # Github
        gh = Github(github_token)
        repo = gh.get_repo("acts-project/acts")

        list_relevant_tags = get_relevant_releases(acts_tag_changes,
                                                   repo.get_releases())
        list_relevant_tags = sorted(list_relevant_tags,
                                    key=lambda x: x[0],
                                    reverse=False)        
        print(f"List of relevant Acts tags interested: {[tag_name for (tag_name, release) in list_relevant_tags]}")

        for (tag_name, release) in list_relevant_tags:
            print(f"   * Getting PRs from Tag {tag_name}")
            list_prs = get_list_prs_for_release(tag_name, release, repo)

            bwriter.add_data_group(title=f"Acts Tag {tag_name} in Athena",
                                   subtitle=f"PRs introduced with Tag {tag_name}",
                                   collection=list_prs)

    bwriter.write()
    


if __name__ == "__main__":
    main()
