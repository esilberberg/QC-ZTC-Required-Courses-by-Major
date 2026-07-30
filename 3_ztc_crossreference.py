#3_ztc_crossreference
import pandas as pd
import numpy as np

ztc_file = input('Input name of file containing the list of ZTC courses: ')
major_reqs_file = input('Input name of file containing the list of major requirements: ')

df_ztc = pd.read_excel(ztc_file)
df_reqs = pd.read_excel(major_reqs_file)

df_reqs["ZTC_Status"] = np.where(
    df_reqs["Course_Number"].isin(df_ztc["Course_Number"]), "YES", ""
)

# Print number of ZTC courses
yes_count = (df_reqs["ZTC_Status"] == "YES").sum()
print(f"Number of ZTC courses: {yes_count}")

df_reqs.to_excel('qc_major_reqs_ZTC_crossref.xlsx', index=False)