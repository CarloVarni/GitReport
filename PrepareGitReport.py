from gitlab import Gitlab
from github import Github

from GitReport.GitHubPullRequest import github_pull_request
from GitReport.GitLabMergeRequest import gitlab_merge_request
from GitReport.BeamerWriter import beamer_writer

from GitReport.GitHubManager import github_manager
from GitReport.GitLabManager import gitlab_manager

from datetime import datetime
import re

import os
from dotenv import load_dotenv
    
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
    gl_manager = gitlab_manager(gitlab_token=gitlab_token,
                                repository="https://gitlab.cern.ch",
                                project_id=53790)

    before_time = datetime.today()
    after_time = datetime(2022, 10, 8)

    list_merged_mrs_summary = gl_manager.get_merge_requests(state='merged',
                                                            labels='ACTS,master',
                                                            created_after=after_time.isoformat(),
                                                            created_before=before_time.isoformat(),
                                                            iterator=True)
    print(f"Found {len(list_merged_mrs_summary)} merged MRs in this period with an ACTS label ...")

    acts_tag_is_changed = gl_manager.changes_acts_tag
    acts_tag_changes = gl_manager.acts_tag_changes
    print('acts_tag_is_changed:', acts_tag_is_changed)
    print('acts_tag_changes:', acts_tag_changes)


    bwriter = beamer_writer("Report-Acts-Athena.tex",
                            title="Acts-Athena integration, MRs report",
                            author="carlo.varni",
                            date="21 October 2022")

    bwriter.add_data_group(title="Merged MRs with ACTS targeting master",
                           subtitle=f"Period: {after_time.isoformat()} -- {before_time.isoformat()}",
                           collection=list_merged_mrs_summary)


    open_with_label = gl_manager.get_merge_requests(state='opened',
                                                    labels='ACTS,master',
                                                    iterator=True)
    list_open_mrs_summary = []
    list_draft_mrs_summary = []

    for mr in open_with_label:
        if "Draft:" in mr.title:
            list_draft_mrs_summary.append(mr)
        else:
            list_open_mrs_summary.append(mr)
            
    bwriter.add_data_group(title="Open MRs with ACTS targeting master",
                           subtitle=f"Period: {after_time.isoformat()} -- {before_time.isoformat()}",
                           collection=list_open_mrs_summary)

    bwriter.add_data_group(title="Draft MRs with ACTS targeting master",
                           subtitle=f"Period: {after_time.isoformat()} -- {before_time.isoformat()}",
                           collection=list_draft_mrs_summary)

    


    if acts_tag_is_changed:
        # Github
        gh_manager = github_manager(github_token=github_token,
                                    repository="acts-project/acts")

        list_relevant_tags = gh_manager.get_relevant_releases(from_release=acts_tag_changes[0],
                                                              to_release=acts_tag_changes[len(acts_tag_changes)-1])

        print(f"List of relevant Acts tags interested: {[tag_name for (tag_name, release) in list_relevant_tags]}")

        for (tag_name, release) in list_relevant_tags:
            print(f"   * Getting PRs from Tag {tag_name}")
            list_prs = gh_manager.get_list_prs_for_release(tag_name=tag_name,
                                                           release_body=release)

            bwriter.add_data_group(title=f"Acts Tag {tag_name} in Athena",
                                   subtitle=f"PRs introduced with Tag {tag_name}",
                                   collection=list_prs)

    bwriter.write()
    


if __name__ == "__main__":
    main()

