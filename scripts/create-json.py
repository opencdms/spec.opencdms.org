import json
import pandas as pd
from pathlib import Path

INPUT_FILEPATH = Path(__file__).parent.parent.joinpath(
    "cdms/v1.0/cdms_specifications_md.xlsx"
)


def write_json(path: str, data: dict):
    with open(path, "w") as stream:
        json.dump(data, stream, default=str, indent=2)


def generate_index():
    # set up env
    output_dir = Path(__file__).parent.parent.joinpath(f"docs/cdms/v1.0").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_filepath = Path(output_dir.joinpath("index.json")).resolve()

    # load data
    chapters_df = pd.read_excel(
        INPUT_FILEPATH, sheet_name="chapters", dtype=str
    ).fillna("")

    # write to output files
    return output_filepath, {
        "title": "Climate Data Management System Specifications",
        "chapters": chapters_df["Number"].values.tolist(),
        "copyright": "World Meteorological Organization, 2014",
        "reference": "WMO-No. 1131",
        "version": "1.0",
    }


def generate_index_with_children():
    output_dir = (
        Path(__file__).parent.parent.joinpath(f"docs/cdms/v1.0/children").resolve()
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    output_filepath = Path(output_dir.joinpath("index.json")).resolve()

    chapters_df = pd.read_excel(
        INPUT_FILEPATH, sheet_name="chapters", dtype=str
    ).fillna("")
    sections_df = pd.read_excel(
        INPUT_FILEPATH, sheet_name="sections", dtype=str
    ).fillna("")
    sub_sections_df = pd.read_excel(INPUT_FILEPATH, sheet_name="sub-sections").fillna(
        ""
    )
    component_sheet_names = [f"ch{n}_components" for n in range(3, 10)]
    components_df_list = [
        pd.read_excel(INPUT_FILEPATH, sheet_name=sheet_name).fillna("")
        for sheet_name in component_sheet_names
    ]
    components_df = pd.concat([df.set_index("Number") for df in components_df_list])

    output = {
        "title": "Climate Data Management System Specifications",
        "chapters": chapters_df["Number"].values.tolist(),
        "copyright": "World Meteorological Organization, 2014",
        "reference": "WMO-No. 1131",
        "version": "1.0",
    }

    for idx, chapter in chapters_df.iterrows():
        chapter_output = {
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

        output[chapter["Number"]] = chapter_output

    for idx, section in sections_df.iterrows():
        sub_sections = list(
            filter(
                lambda x: str(x).startswith(str(section["Number"])),
                sub_sections_df["Number"].values.tolist(),
            )
        )
        section_output = {
            "title": section["Title"],
            "text": section["Description"],
            "subsections": sub_sections,
            "copyright": "World Meteorological Organization, 2014",
            "reference": "WMO-No. 1131",
            "version": "1.0",
        }

        chapter_number = str(section["Number"]).split(".")[0]

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

            section_output[sub_section] = {
                "title": sub_section_row["Title"],
                "text": sub_section_row["Description"],
            }
            section_output[sub_section]["components"] = component_indexes
            for component_index in component_indexes:
                section_output[sub_section][component_index] = (
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

        output[chapter_number][str(section["Number"])] = section_output

    write_json(output_dir.joinpath("index.json").resolve().as_posix(), output)


def generate_chapter():
    chapters_df = pd.read_excel(
        INPUT_FILEPATH, sheet_name="chapters", dtype=str
    ).fillna("")
    sections_df = pd.read_excel(
        INPUT_FILEPATH, sheet_name="sections", dtype=str
    ).fillna("")

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

        output_dir = (
            Path(__file__)
            .parent.parent.joinpath(f"docs/cdms/v1.0/{chapter['Number']}")
            .resolve()
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filepath = Path(output_dir.joinpath("index.json")).resolve()

        with open(output_filepath, "w") as stream:
            json.dump(output, stream, indent=2)


def generate_chapter_with_children():
    chapters_df = pd.read_excel(
        INPUT_FILEPATH, sheet_name="chapters", dtype=str
    ).fillna("")
    sections_df = pd.read_excel(
        INPUT_FILEPATH, sheet_name="sections", dtype=str
    ).fillna("")

    sub_sections_df = pd.read_excel(
        INPUT_FILEPATH, sheet_name="sub-sections", dtype=str
    ).fillna("")
    component_sheet_names = [f"ch{n}_components" for n in range(3, 10)]
    components_df_list = [
        pd.read_excel(INPUT_FILEPATH, sheet_name=sheet_name).fillna("")
        for sheet_name in component_sheet_names
    ]
    components_df = pd.concat([df.set_index("Number") for df in components_df_list])

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
        for idx, section in sections_df.iterrows():
            sub_sections = list(
                filter(
                    lambda x: str(x).startswith(str(section["Number"])),
                    sub_sections_df["Number"].values.tolist(),
                )
            )
            section_output = {
                "title": section["Title"],
                "text": section["Description"],
                "subsections": sub_sections,
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

                section_output[sub_section] = {
                    "title": sub_section_row["Title"],
                    "text": sub_section_row["Description"],
                }
                section_output[sub_section]["components"] = component_indexes
                for component_index in component_indexes:
                    section_output[sub_section][component_index] = (
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

            output[str(section["Number"])] = section_output

        output_dir = (
            Path(__file__)
            .parent.parent.joinpath(f"docs/cdms/v1.0/{chapter['Number']}/children")
            .resolve()
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filepath = Path(output_dir.joinpath("index.json")).resolve()

        write_json(output_filepath.as_posix(), output)


def generate_section():
    sections_df = pd.read_excel(INPUT_FILEPATH, sheet_name="sections").fillna("")
    sub_sections_df = pd.read_excel(INPUT_FILEPATH, sheet_name="sub-sections").fillna(
        ""
    )

    for idx, section in sections_df.iterrows():
        sub_sections = list(
            filter(
                lambda x: str(x).startswith(str(section["Number"])),
                sub_sections_df["Number"].values.tolist(),
            )
        )
        output = {
            "title": section["Title"],
            "text": section["Description"],
            "subsections": sub_sections,
            "copyright": "World Meteorological Organization, 2014",
            "reference": "WMO-No. 1131",
            "version": "1.0",
        }

        output_dir = (
            Path(__file__)
            .parent.parent.joinpath(f"docs/cdms/v1.0/{section['Number']}")
            .resolve()
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filepath = Path(output_dir.joinpath("index.json")).resolve()

        with open(output_filepath, "w") as stream:
            json.dump(output, stream, indent=2)


def generate_section_with_children():
    sections_df = pd.read_excel(INPUT_FILEPATH, sheet_name="sections").fillna("")
    sub_sections_df = pd.read_excel(INPUT_FILEPATH, sheet_name="sub-sections").fillna(
        ""
    )
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
            "text": section["Description"],
            "subsections": sub_sections,
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
            output[sub_section]["components"] = component_indexes
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
        output_dir = (
            Path(__file__)
            .parent.parent.joinpath(f"docs/cdms/v1.0/{section['Number']}/children")
            .resolve()
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filepath = Path(output_dir.joinpath("index.json")).resolve()

        with open(output_filepath, "w") as stream:
            json.dump(output, stream, indent=2)


def generate_sub_section():
    sub_sections_df = pd.read_excel(INPUT_FILEPATH, sheet_name="sub-sections").fillna(
        ""
    )
    component_sheet_names = [f"ch{n}_components" for n in range(3, 10)]
    components_df_list = [
        pd.read_excel(INPUT_FILEPATH, sheet_name=sheet_name).fillna("")
        for sheet_name in component_sheet_names
    ]
    components_df = pd.concat([df.set_index("Number") for df in components_df_list])

    for idx, sub_section in sub_sections_df.iterrows():
        output = {
            "title": sub_section["Title"],
            "text": sub_section["Description"],
            "components": list(
                filter(
                    lambda x: x.startswith(sub_section["Number"]),
                    components_df.index.values.tolist(),
                )
            ),
            "copyright": "World Meteorological Organization, 2014",
            "reference": "WMO-No. 1131",
            "version": "1.0",
        }

        output_dir = (
            Path(__file__)
            .parent.parent.joinpath(f"docs/cdms/v1.0/{sub_section['Number']}")
            .resolve()
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filepath = Path(output_dir.joinpath("index.json")).resolve()

        with open(output_filepath, "w") as stream:
            json.dump(output, stream, indent=2)


def generate_sub_section_with_children():
    sub_sections_df = pd.read_excel(INPUT_FILEPATH, sheet_name="sub-sections").fillna(
        ""
    )
    component_sheet_names = [f"ch{n}_components" for n in range(3, 10)]
    components_df_list = [
        pd.read_excel(INPUT_FILEPATH, sheet_name=sheet_name).fillna("")
        for sheet_name in component_sheet_names
    ]
    components_df = pd.concat([df.set_index("Number") for df in components_df_list])

    for idx, sub_section in sub_sections_df.iterrows():
        output = {
            "title": sub_section["Title"],
            "text": sub_section["Description"],
            "components": list(
                filter(
                    lambda x: x.startswith(sub_section["Number"]),
                    components_df.index.values.tolist(),
                )
            ),
            "copyright": "World Meteorological Organization, 2014",
            "reference": "WMO-No. 1131",
            "version": "1.0",
        }

        for cpt_idx, component in components_df.iterrows():
            if cpt_idx.startswith(sub_section["Number"]):
                output[cpt_idx] = {
                    "title": component["Title"],
                    "text": component["Description"],
                    "classification": component["Classification"],
                }
        output_dir = (
            Path(__file__)
            .parent.parent.joinpath(f"docs/cdms/v1.0/{sub_section['Number']}/children")
            .resolve()
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filepath = Path(output_dir.joinpath("index.json")).resolve()

        with open(output_filepath, "w") as stream:
            json.dump(output, stream, indent=2)


def generate_component():
    component_sheet_names = [f"ch{n}_components" for n in range(3, 10)]
    components_df_list = [
        pd.read_excel(INPUT_FILEPATH, sheet_name=sheet_name).fillna("")
        for sheet_name in component_sheet_names
    ]
    components_df = pd.concat([df.set_index("Number") for df in components_df_list])

    for cpt_idx, component in components_df.iterrows():
        output = {
            "title": component["Title"],
            "text": component["Description"],
            "classification": component["Classification"],
            "copyright": "World Meteorological Organization, 2014",
            "reference": "WMO-No. 1131",
            "version": "1.0",
        }

        output_dir = (
            Path(__file__).parent.parent.joinpath(f"docs/cdms/v1.0/{cpt_idx}").resolve()
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filepath = Path(output_dir.joinpath("index.json")).resolve()

        write_json(output_filepath.as_posix(), output)


if __name__ == "__main__":
    generate_index()
    generate_index_with_children()
    generate_chapter()
    generate_chapter_with_children()
    generate_section()
    generate_section_with_children()
    generate_sub_section()
    generate_sub_section_with_children()
    generate_component()
