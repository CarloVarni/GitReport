from gitlab import Gitlab
from github import Github

from GitReport.GitHubPullRequest import github_pull_request
from GitReport.GitLabMergeRequest import gitlab_merge_request
from GitReport.BeamerWriter import beamer_writer

from GitReport.GitHubManager import github_manager
from GitReport.GitLabManager import gitlab_manager

import argparse
import re
import os
from dotenv import load_dotenv

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--author', required=True, type=str, nargs=1,
                        help='Author of the Git Report document')
    parser.add_argument('--date', required=True, type=str, nargs=1, 
                        help='Date of the report')
    parser.add_argument('--title', required=False, type=str, nargs=1, default="Acts-Athena integration, MRs report",
                        help='Title of the presentation')
    parser.add_argument('--gitlab_repository', required=False, type=str, nargs=1, default="https://gitlab.cern.ch",
                        help='Gitlab repository')
    parser.add_argument('--gitlab_project_id', required=False, type=int, nargs=1, default=53790,
                        help='Gitlab projects id')
    parser.add_argument('--github_repository', required=False, type=str, nargs=1, default="acts-project/acts",
                        help='Github repository')
    parser.add_argument('--output_file', required=True, type=str, nargs=1,
                        help='Name of the output latex file')
    parser.add_argument('--from_date', required=True, type=str, nargs=1,
                        help='Get gitlab merge requests from given date')
    parser.add_argument('--to_date', required=True, type=str, nargs=1,
                        help='Get gitlab merge requests up to given date')
    parser.add_argument('--branch', required=False, type=str, nargs=1, default='master',
                        help='List of branches')
    
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    
    gitlab_repository_name = args.gitlab_repository if type(args.gitlab_repository) == str else args.gitlab_repository[0]
    gitlab_project_id = args.gitlab_project_id
    github_repository_name = args.github_repository if type(args.github_repository) == str else args.github_repository[0]
    output_file = args.output_file if type(args.output_file) == str else args.output_file[0]
    author = args.author if type(args.author) == str else args.author[0]
    title = args.title if type(args.title) == str else args.title[0]
    date = args.date if type(args.date) == str else args.date[0]
    date_from = args.from_date if type(args.from_date) == str else args.from_date[0]
    date_to = args.to_date if type(args.to_date) == str else args.to_date[0]
    branches = args.branch.split(',') if type(args.branch) == str else args.branch[0].split(',')

    gitlab_token = ""
    github_token = ""

    try:
        load_dotenv()
        gitlab_token = str(os.getenv('GITLAB_TOKEN'))
        github_token = str(os.getenv('GITHUB_TOKEN'))
    except Exception:
        print('Env variables are not properly set! Check the .env file is present and/or the env variables are set.')
        quit()
        
    # Gitlab
    gl_manager = gitlab_manager(gitlab_token=gitlab_token,
                                repository=gitlab_repository_name,
                                project_id=gitlab_project_id)

    bwriter = beamer_writer(output_file,
                            title=title,
                            author=author,
                            date=date)

    for branch in branches:
        print(f"Retrieving  MRs in this period with labels: ACTS and {branch} ...")
        list_merged_mrs_summary = gl_manager.get_merge_requests(state='merged',
                                                                labels=f'ACTS,{branch}',
                                                                created_after=date_from,
                                                                created_before=date_to,
                                                                iterator=True)
        print(f"   * Found {len(list_merged_mrs_summary)} merged MRs")
        
        bwriter.add_data_group(title=f"Merged MRs with ACTS targeting {branch}",
                               subtitle=f"Period: {date_from} -- {date_to}",
                               collection=[el for el in list_merged_mrs_summary])

        open_with_label = gl_manager.get_merge_requests(state='opened',
                                                        labels=f'ACTS,{branch}',
                                                        iterator=True)
        print(f"   * Found {len(list_merged_mrs_summary)} opened/draft MRs")
                
        bwriter.add_data_group(title=f"Open MRs with ACTS targeting {branch}",
                               subtitle=f"Period: {date_from} -- {date_to}",
                               collection=[el for el in open_with_label if not el.draft])

        bwriter.add_data_group(title=f"Draft MRs with ACTS targeting {branch}",
                               subtitle=f"Period: {date_from} -- {date_to}",
                               collection=[el for el in open_with_label if el.draft])

    acts_tag_is_changed = gl_manager.changes_acts_tag
    acts_tag_changes = gl_manager.acts_tag_changes
    print('acts_tag_is_changed:', acts_tag_is_changed)
    print('acts_tag_changes:', acts_tag_changes)
    
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
                                   collection=list_prs,
                                   section_page=True)

    bwriter.write()
    


if __name__ == "__main__":
    main()

