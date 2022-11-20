import markdown
import pandas as pd
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape

INPUT_FILEPATH = Path(__file__).parent.parent.joinpath(
    "cdms/v1.0/cdms_specifications_md.xlsx"
)

chapters: pd.DataFrame = pd.read_excel(
    INPUT_FILEPATH, sheet_name="chapters", index_col="Number", dtype=str
).fillna("")
sections: pd.DataFrame = pd.read_excel(
    INPUT_FILEPATH, sheet_name="sections", index_col="Number", dtype=str
).fillna("")
sub_sections: pd.DataFrame = pd.read_excel(
    INPUT_FILEPATH, sheet_name="sub-sections", index_col="Number", dtype=str
).fillna("")
components: pd.DataFrame = pd.concat(
    [
        pd.read_excel(
            INPUT_FILEPATH,
            sheet_name=f"ch{i}_components",
            index_col="Number",
            dtype=str,
        ).fillna("")
        for i in range(3, 10)
    ]
)

env = Environment(
    loader=PackageLoader(package_name="wmo", package_path="../wmo/templates"),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)

if __name__ == "__main__":
    index_template = env.get_template("index.html")
    chapter_template = env.get_template("chapter.html")
    section_template = env.get_template("section.html")
    sub_section_template = env.get_template("sub_section.html")
    component_template = env.get_template("component.html")
    index_output_filepath = Path(__file__).parent.parent.joinpath(
        "docs/cdms/v1.0/index.html"
    )
    with open(index_output_filepath, "w") as stream:
        stream.write(
            index_template.render(
                {
                    "chapters": chapters.to_dict(orient="index"),
                    "sections": sections.to_dict(orient="index"),
                    "sub_sections": sub_sections.to_dict(orient="index"),
                    "components": components.to_dict(orient="index"),
                    "str": str,
                    "markdown": markdown.markdown,
                },
            )
        )

    for idx, chapter in chapters.iterrows():
        output_file_path = Path(__file__).parent.parent.joinpath(
            f"docs/cdms/v1.0/{idx}/index.html"
        )
        with open(output_file_path, "w") as stream:
            stream.write(
                chapter_template.render(
                    {
                        "chapter": {"Name": idx, **chapter.to_dict()},
                        "str": str,
                        "markdown": markdown.markdown,
                    }
                )
            )

    for idx, section in sections.iterrows():
        output_file_path = Path(__file__).parent.parent.joinpath(
            f"docs/cdms/v1.0/{idx}/index.html"
        )
        with open(output_file_path, "w") as stream:
            stream.write(
                section_template.render(
                    {
                        "section": {"Number": idx, **section.to_dict()},
                        "str": str,
                        "markdown": markdown.markdown,
                    }
                )
            )

    for idx, sub_section in sub_sections.iterrows():
        output_file_path = Path(__file__).parent.parent.joinpath(
            f"docs/cdms/v1.0/{idx}/index.html"
        )
        with open(output_file_path, "w") as stream:
            stream.write(
                sub_section_template.render(
                    {
                        "subsection": {"Number": idx, **sub_section.to_dict()},
                        "str": str,
                        "markdown": markdown.markdown,
                    }
                )
            )

    for idx, cmpt in components.iterrows():
        output_file_path = Path(__file__).parent.parent.joinpath(
            f"docs/cdms/v1.0/{idx}/index.html"
        )
        with open(output_file_path, "w") as stream:
            stream.write(
                component_template.render(
                    {
                        "cmpt": {
                            "Number": idx,
                            "Title": cmpt["Title"],
                            "Description": cmpt["Description"],
                            "Classification": cmpt["Classification"],
                        },
                        "str": str,
                        "markdown": markdown.markdown,
                    }
                )
            )
