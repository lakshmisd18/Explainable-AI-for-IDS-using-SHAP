import pandas as pd

df = pd.read_csv("data/dataset.csv", header=None)

# REMOVE LABEL COLUMN
df = df.iloc[:, :-1]

# Create test files
df.sample(50).to_csv("test_mixed.csv", index=False, header=False)
df.sample(50).to_csv("test_normal.csv", index=False, header=False)
df.sample(50).to_csv("test_attack.csv", index=False, header=False)