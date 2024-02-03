import pandas as pd

df = pd.read_csv("./stack-overflow-developer-survey-2023/survey_results_public.csv")
#print(df)
#df.info()
#pd.set_option('display.max_columns', 3)
#pd.set_option('display.max_rows', 50)
schema_df = pd.read_csv("./stack-overflow-developer-survey-2023/survey_results_schema.csv")
df.head()
print(df.columns)
print(df["LanguageWantToWorkWith"].value_counts())

path_to_excel = '/Users/uendellmagno/Desktop/INTERAÇÃO-LEADS-0810-2610.xlsx'
df = pd.read_excel(path_to_excel, sheet_name="M12S1", usecols='A:H')
print(df)


df = pd.DataFrame('Name')