import json
import pandas as pd
from pathlib import Path


INPUT_FILEPATH = Path("../cdms/v1.0/cdms_specfications_md.xlsx")


def create_chapters():
    # set up env
    output_dir = Path(f"../docs/cdms/v1.0").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_filepath = Path(output_dir.joinpath("index.json")).resolve()

    # load data
    chapters_df = pd.read_excel(INPUT_FILEPATH, sheet_name="chapters").fillna("")

    # write to output files
    with open(output_filepath, "w") as stream:
        json.dump(
            {
                "title": "Climate Data Management System Specifications",
                "chapters": chapters_df["Number"].values.tolist(),
                "copyright": "World Meteorological Organization, 2014",
                "reference": "WMO-No. 1131",
                "version": "1.0",
            },
            stream,
            indent=2
        )


def create_sections():
    chapters_df = pd.read_excel(INPUT_FILEPATH, sheet_name="chapters").fillna("")
    sections_df = pd.read_excel(INPUT_FILEPATH, sheet_name="sections").fillna("")

    for idx, chapter in chapters_df.iterrows():
        output = {
            "title": chapter["Title"],
            "sections": list(
                filter(
                    lambda x: str(x).startswith(str(chapter["Number"])),
                    sections_df["Number"].values.tolist(),
                )
            ),
            "copyright": "World Meteorological Organization, 2014",
            "reference": "WMO-No. 1131",
            "version": "1.0",
        }

        output_dir = Path(f"../docs/cdms/v1.0/{chapter['Number']}").resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filepath = Path(output_dir.joinpath("index.json")).resolve()

        with open(output_filepath, "w") as stream:
            json.dump(output, stream, indent=2)


def create_sub_sections_with_contents():
    sections_df = pd.read_excel(INPUT_FILEPATH, sheet_name="sections").fillna("")
    sub_sections_df = pd.read_excel(INPUT_FILEPATH, sheet_name="sub-sections").fillna("")
    component_sheet_names = [f"ch{n}_components" for n in range(3, 10)]
    components_df_list = [
        pd.read_excel(INPUT_FILEPATH, sheet_name=sheet_name).fillna("")
        for sheet_name in component_sheet_names
    ]
    components_df = pd.concat([df.set_index("Number") for df in components_df_list])

    for idx, section in sections_df.iterrows():
        sub_sections = list(
            filter(
                lambda x: str(x).startswith(str(section["Number"])),
                sub_sections_df["Number"].values.tolist(),
            )
        )
        output = {
            "title": section["Title"],
            "subsections": sub_sections,
            "components": {},
            "copyright": "World Meteorological Organization, 2014",
            "reference": "WMO-No. 1131",
            "version": "1.0",
        }

        for sub_section in sub_sections:
            sub_section_row = sub_sections_df.loc[
                sub_sections_df["Number"] == sub_section
                ].iloc[0]
            component_indexes = list(
                filter(
                    lambda x: x.startswith(str(sub_section)),
                    components_df.index.values.tolist(),
                )
            )

            output[sub_section] = {
                "title": sub_section_row["Title"],
                "text": sub_section_row["Description"],
            }
            output["components"][sub_section] = component_indexes
            for component_index in component_indexes:
                output[sub_section][component_index] = (
                    components_df.filter(items=[component_index], axis=0)
                    .rename(
                        columns={
                            "Title": "title",
                            "Description": "text",
                            "Classification": "classification",
                        }
                    )
                    .iloc[0]
                ).to_dict()
        output_dir = Path(f"../docs/cdms/v1.0/{section['Number']}").resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filepath = Path(output_dir.joinpath("index.json")).resolve()

        with open(output_filepath, "w") as stream:
            json.dump(output, stream, indent=2)


if __name__ == "__main__":
    create_chapters()
    create_sections()
    create_sub_sections_with_contents()
