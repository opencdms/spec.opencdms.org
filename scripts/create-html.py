import pandas as pd
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape


INPUT_FILEPATH = Path("../cdms/v1.0/cdms_specfications_md.xlsx")

chapters = pd.read_excel(
    INPUT_FILEPATH, sheet_name="chapters", index_col="Number", dtype=str
).fillna("")
sections = pd.read_excel(
    INPUT_FILEPATH, sheet_name="sections", index_col="Number", dtype=str
).fillna("")
sub_sections = pd.read_excel(
    INPUT_FILEPATH, sheet_name="sub-sections", index_col="Number", dtype=str
).fillna("")
components = pd.concat(
    [
        pd.read_excel(
            INPUT_FILEPATH, sheet_name=f"ch{i}_components", index_col="Number", dtype=str
        ).fillna("")
        for i in range(3, 10)
    ]
)

env = Environment(
    loader=PackageLoader(package_name="wmo", package_path="../wmo/templates"),
    autoescape=select_autoescape(),
)

index = env.get_template("index.html")


if __name__ == "__main__":
    with open("../docs/index.html", "w") as stream:
        stream.write(
            index.render(
                {
                    "chapters": chapters.to_dict(orient="index"),
                    "sections": sections.to_dict(orient="index"),
                    "sub_sections": sub_sections.to_dict(orient="index"),
                    "components": components.to_dict(orient="index"),
                    "str": str
                }
            )
        )
