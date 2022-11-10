import json
import pandas as pd
from pathlib import Path

sections_filepath = Path("../data/input/sections.csv").absolute()
sub_sections_filepath = Path("../data/input/sub-sections.csv").absolute()

sections_df = pd.read_csv(sections_filepath, encoding="ISO-8859-1")
sub_sections_df = pd.read_csv(sections_filepath, encoding="ISO-8859-1")

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
        "copyright": "World Meteorological Organization, 2014",
        "reference": "WMO-No. 1131",
        "version": "1.0",
    }

    for sub_section in sub_sections:
        sub_section_row = sub_sections_df.loc[sub_sections_df["Number"] == sub_section].iloc[0]
        output[sub_section] = {
            "title": sub_section_row["Title"],
            "text": sub_section_row["Description"]
        }
    output_filepath = Path(f"../data/output/section_{section['Number']}.json").absolute()

    with open(output_filepath, "w") as stream:
        json.dump(output, stream, indent=2)


