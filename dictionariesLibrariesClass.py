import pandas as pd
people = {"first": ["Uendell", 'Thalita', 'Julia'], "last": ["Avila", 'Souza', 'Medeiros'], "email": ["uendellmagno@gmail.com", "thalitaalisouza@gmail.com", "julinheiros@gmail.com"]}
print(people['first'])

df = pd.DataFrame(people)
print(df[['first', 'last']])
print(df.iloc[[0,2], 2])
