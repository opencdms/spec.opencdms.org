import json
import pandas as pd
from pathlib import Path


template = {
    "title": "",
    "sections": [],
    "copyright": "World Meteorological Organization, 2014",
    "reference": "WMO-No. 1131",
    "version": "1.0",
}

input_file_path = Path("../cdms/v1.0/cdms_specfications.xlsx")


chapters_df = pd.read_excel(input_file_path, sheet_name="chapters").fillna("")
sections_df = pd.read_excel(input_file_path, sheet_name="sections").fillna("")

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

