import pandas as pd

# Load dataset
df = pd.read_csv("data/dataset.csv", header=None)

label_col = 41

# ---------- HEAVY ATTACK ----------
attack = df[df[label_col] != "normal"].sample(90)
normal = df[df[label_col] == "normal"].sample(10)
pd.concat([attack, normal]).to_csv("data/test_heavy_attack.csv", index=False)

# ---------- LOW ATTACK ----------
normal = df[df[label_col] == "normal"].sample(90)
attack = df[df[label_col] != "normal"].sample(10)
pd.concat([normal, attack]).to_csv("data/test_low_attack.csv", index=False)

# ---------- LARGE RANDOM ----------
df.sample(500).to_csv("data/test_random_large.csv", index=False)

# ---------- SMALL SAMPLE ----------
df.sample(20).to_csv("data/test_small_sample.csv", index=False)

# ---------- SPECIFIC ATTACK (example: neptune) ----------
df[df[label_col] == "neptune"].sample(100).to_csv("data/test_neptune_attack.csv", index=False)

print("✅ More CSV files created successfully!")