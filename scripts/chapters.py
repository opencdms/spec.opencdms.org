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

chapters_filepath = Path("../data/input/chapters.csv").absolute()
sections_filepath = Path("../data/input/sections.csv").absolute()


chapters_df = pd.read_csv(chapters_filepath)
sections_df = pd.read_csv(sections_filepath, encoding="ISO-8859-1")

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

    output_filepath = Path(f"../data/output/chapter_{chapter['Number']}.json")

    with open(output_filepath, "w") as stream:
        json.dump(output, stream, indent=2)

