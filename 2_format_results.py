#2_format_results
import numpy as np
import pandas as pd

# Set the target file to format
file = input('Input name of file to format: ')

df = pd.read_excel(file)

# Split the column into two parts (n=1 splits on the FIRST dash)
split_courses = (
    df["Required_Course"].astype(str).str.split(r"\s*-\s*", n=1, expand=True)
)
df["Course_Number"] = split_courses[0]
df["Course_Name"] = split_courses[1]

# 4. Handle N/A, missing (NaN), or non-formatted values
invalid_mask = (
    df["Required_Course"].isna()
    | df["Required_Course"]
    .astype(str)
    .str.strip()
    .str.upper()
    .isin(["N/A", "NA", ""])
    | ~df["Required_Course"].astype(str).str.contains(" - ")
)


df.loc[invalid_mask, ["Course_Number", "Course_Name"]] = np.nan

df.to_excel("qc_majors_core_courses.xlsx", index=False)

print(df)
