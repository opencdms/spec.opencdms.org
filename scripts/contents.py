import json
from pathlib import Path
import pandas as pd


contents = {
    "title": "Climate Data Management System Specifications",
    "chapters": [],
    "copyright": "World Meteorological Organization, 2014",
    "reference": "WMO-No. 1131",
    "version": "1.0",
}

if __name__ == "__main__":
    input_filepath = Path("../cdms/v1.0/cdms_specfications_md.xlsx").resolve()
    output_dir = Path(f"../docs/cdms/v1.0").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_filepath = Path(output_dir.joinpath("index.json")).resolve()
    chapters_df = pd.read_excel(input_filepath, sheet_name="chapters").fillna("")
    contents["chapters"] = chapters_df["Number"].values.tolist()

    with open(output_filepath, "w") as stream:
        json.dump(contents, stream, indent=2)
