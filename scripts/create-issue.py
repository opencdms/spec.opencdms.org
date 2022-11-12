import enum
import logging
import os
import argparse
import time

from github import Github, Repository
from pathlib import Path
import pandas as pd
from typing import List, Optional
from pydantic import BaseModel


INPUT_FILEPATH = Path("../cdms/v1.0/cdms_specfications.xlsx").resolve()


class Classifications(enum.Enum):
    OPTIONAL = "Optional"
    RECOMMENDED = "Recommended"
    REQUIRED = "Required"


class Label(BaseModel):
    name: str
    color: str


class IssueData(BaseModel):
    title: str
    description: Optional[str]
    classification: Optional[Classifications]


LABEL_COLOR_MAP = {
    "Required": "e9d758",
    "Recommended": "297373",
    "Optional": "e6e6e6",
    "CDMS v1.0": "275dad",
    "Epic": "2c666e"
}

ALL_LABELS = [Label(name=k, color=v) for k, v in LABEL_COLOR_MAP.items()]


def get_components() -> List[IssueData]:
    component_sheet_names = [f"ch{n}_components" for n in range(3, 10)]
    components_df_list = [
        pd.read_excel(INPUT_FILEPATH, sheet_name=sheet_name).fillna("")
        for sheet_name in component_sheet_names
    ]
    return [
        IssueData(
            title=f"{idx} {row['Title']}",
            description=row["Description"],
            classification=row["Classification"],
        )
        for idx, row in pd.concat(
            [df.set_index("Number") for df in components_df_list]
        ).iterrows()
    ]


def get_chapters() -> List[IssueData]:
    chapter_df = pd.read_excel(INPUT_FILEPATH, sheet_name="chapters").fillna("")
    return [
        IssueData(
            title=f"{row['Number']} {row['Title']}"
        )
        for idx, row in chapter_df.iterrows()
    ]


def get_sections() -> List[IssueData]:
    section_df = pd.read_excel(INPUT_FILEPATH, sheet_name="sections").fillna("")
    return [
        IssueData(
            title=f"{row['Number']} {row['Title']}",
            description=row["Description"]
        )
        for idx, row in section_df.iterrows()
    ]


def get_sub_sections() -> List[IssueData]:
    sub_section_df = pd.read_excel(INPUT_FILEPATH, sheet_name="sections").fillna("")
    return [
        IssueData(
            title=f"{row['Number']} {row['Title']}",
            description=row["Description"]
        )
        for idx, row in sub_section_df.iterrows()
    ]


def get_client() -> Github:
    return Github(os.getenv("GITHUB_TOKEN"))


def get_repo(username: str, repo: str) -> Repository.Repository:
    client = get_client()
    return client.get_repo(f"{username}/{repo}")


def get_existing_labels(repo: Repository.Repository):
    return repo.get_labels()


def get_existing_issues(repo: Repository.Repository):
    return repo.get_issues(state="all")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("OpenCDMS")

    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="opencdms", required=False)
    parser.add_argument("--repo", default="temp-repo", required=False)
    parser.add_argument("--issue-limit", default=1, required=False)
    parser.add_argument("--common-labels", default=["Epic", "CDMS v1.0"], required=False)
    args = parser.parse_args()

    logger.info(f"""
    =====================================================================
    Creating issues for : https://github.com/{args.username}/{args.repo}
    INPUT FILE          : {INPUT_FILEPATH}
    =====================================================================
    """)

    repo = get_repo(args.username, args.repo)

    existing_labels = get_existing_labels(repo)
    existing_labels_set = {label.name for label in existing_labels}

    logger.info(f"""Existing labels in the repo: {', '.join(existing_labels_set)}""")

    labels_to_create = [
        label for label in ALL_LABELS if label.name not in existing_labels_set
    ]

    if labels_to_create:
        logger.info(f"""Labels to create: {', '.join([l.name for l in labels_to_create])}""")
    else:
        logger.info("No label to create...")

    for label in labels_to_create:
        logger.info(f"""Creating label: {label.name} with color: {label.color}""")
        repo.create_label(name=label.name, color=label.color)

    repo_labels = get_existing_labels(repo)
    label_map = {label.name: label for label in repo_labels}

    existing_issues_set = {issue.title for issue in get_existing_issues(repo)}
    issues_to_create = [
        component
        for component in get_components()
        if component.title not in existing_issues_set
    ]

    logger.info(f"""Creating {args.issue_limit} issue(s)...""")
    for issue in issues_to_create[:args.issue_limit]:
        common_labels = [label_map[label] for label in args.common_labels]
        issue_labels = common_labels+[label_map[issue.classification.value]]
        logger.info(f"""
        Creating issue with
        Title: {issue.title}
        Labels: {', '.join([label.name for label in issue_labels])}
        """)
        try:
            repo.create_issue(
                title=issue.title,
                body=issue.description,
                labels=issue_labels,
            )
            logger.info("""Issue created successfully...""")
        except Exception as e:
            logger.exception(e)
        time.sleep(0.1)
