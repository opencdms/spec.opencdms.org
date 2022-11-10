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
    input_filepath = Path("../data/input/chapters.csv").absolute()
    output_filepath = Path("../data/output/contents.json").absolute()
    chapters_df = pd.read_csv(input_filepath)
    contents["chapters"] = chapters_df["Number"].values.tolist()

    with open(output_filepath, "w") as stream:
        json.dump(contents, stream, indent=2)
