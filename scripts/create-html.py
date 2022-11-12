import pandas as pd
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape


INPUT_FILE_PATH = Path("../cdms/v1.0/cdms_specfications.xlsx")

contents = pd.read_excel(INPUT_FILE_PATH, )

env = Environment(
    loader=PackageLoader(package_name="wmo", package_path="../wmo/templates"),
    autoescape=select_autoescape()
)

index = env.get_template("index.html")

with open("../docs/index.html", "w") as stream:
    stream.write(index.render(data))
