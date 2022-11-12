import enum
import os

from github import Github, Repository
from pathlib import Path
import pandas as pd
from typing import List
from pydantic import BaseModel


USERNAME = "opencdms"
REPO_NAME = "spec.opencdms.org"
URL = f"https://api.github.com/repos/{USERNAME}/{REPO_NAME}/issues"

INPUT_FILEPATH = Path("../cdms/v1.0/cdms_specfications.xlsx").resolve()


class Classifications(enum.Enum):
    OPTIONAL = "Optional"
    RECOMMENDED = "Recommended"
    REQUIRED = "Required"


class Labels(enum.Enum):
    OPTIONAL = "Optional"
    RECOMMENDED = "Recommended"
    REQUIRED = "Required"
    CDMS_V1 = "CDMS v1.0"
    EPIC = "Epic"


class Component(BaseModel):
    title: str
    description: str
    classification: Classifications


LABEL_COLOR_MAP = {
    "Required": "e9d758",
    "Recommended": "297373",
    "Optional": "e6e6e6",
    "CDMS v1.0": "275dad",
    "Epic": "2c666e"
}


def get_components() -> List[Component]:
    component_sheet_names = [f"ch{n}_components" for n in range(3, 10)]
    components_df_list = [
        pd.read_excel(INPUT_FILEPATH, sheet_name=sheet_name).fillna("")
        for sheet_name in component_sheet_names
    ]
    return [
        Component(
            title=row["Title"],
            description=row["Description"],
            classification=row["Classification"],
        )
        for idx, row in pd.concat(
            [df.set_index("Number") for df in components_df_list]
        ).iterrows()
    ]


def get_client() -> Github:
    return Github(os.getenv("GITHUB_TOKEN"))


def get_repo() -> Repository.Repository:
    client = get_client()
    return client.get_repo(f"{USERNAME}/{REPO_NAME}")


def get_existing_labels():
    repo = get_repo()
    return repo.get_labels()


def get_existing_issues():
    repo = get_repo()
    return repo.get_issues(state="all")


if __name__ == "__main__":

    repo = get_repo()

    existing_labels = get_existing_labels()
    existing_labels_set = {label.name for label in existing_labels}
    labels_to_create = [
        label.value for label in Labels if label.value not in existing_labels_set
    ]

    for label in labels_to_create:
        repo.create_label(name=label, color=LABEL_COLOR_MAP[label])

    all_labels = get_existing_labels()

    label_map = {label.name: label for label in all_labels}

    existing_issues_set = {issue.title for issue in get_existing_issues()}
    issues_to_create = [
        component
        for component in get_components()
        if component.title not in existing_issues_set
    ]

    for issue in issues_to_create:
        repo.create_issue(
            title=issue.title,
            body=issue.description,
            labels=[
                label_map[Labels.CDMS_V1.value],
                label_map[issue.classification.value],
            ],
        )
