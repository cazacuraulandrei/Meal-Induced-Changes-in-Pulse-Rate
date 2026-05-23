import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# -------------------
# LOAD DATA
# -------------------
df = pd.read_excel("raw class pulse data.xlsx")

# Keep only relevant columns
df = df[[
    "Q01_Pre-meal pulse rate",
    "Q03_Post-meal pulse rate",
    "Q07_Sex",
    "Q06_Relative size of meal"
]].dropna()

print(df.head())
print("Rows analysed:", len(df))

# -------------------
# BASIC ANALYSIS
# -------------------
pre_mean = df["Q01_Pre-meal pulse rate"].mean()
post_mean = df["Q03_Post-meal pulse rate"].mean()

print("\nPre-meal average:", pre_mean)
print("Post-meal average:", post_mean)

df["difference"] = df["Q03_Post-meal pulse rate"] - df["Q01_Pre-meal pulse rate"]
print("Average change:", df["difference"].mean())

# -------------------
# STATISTICAL TEST
# -------------------
t_stat, p_value = stats.ttest_rel(
    df["Q01_Pre-meal pulse rate"],
    df["Q03_Post-meal pulse rate"]
)

print("\nT-statistic:", t_stat)
print("P-value:", p_value)

# -------------------
# GROUP ANALYSIS
# -------------------
sex_analysis = df.groupby("Q07_Sex")[
    ["Q01_Pre-meal pulse rate", "Q03_Post-meal pulse rate"]
].mean()

print("\nSex-based averages:")
print(sex_analysis)

meal_analysis = df.groupby("Q06_Relative size of meal")[
    ["Q01_Pre-meal pulse rate", "Q03_Post-meal pulse rate"]
].mean()

print("\nMeal size effect:")
print(meal_analysis)

# -------------------
# PLOTTING
# -------------------
summary = df[[
    "Q01_Pre-meal pulse rate",
    "Q03_Post-meal pulse rate"
]].mean()

summary.index = ["Pre-meal", "Post-meal"]

ax = summary.plot(kind="bar")

y_max = summary.max()

# significance bracket
plt.plot([0, 0, 1, 1],
         [y_max + 2, y_max + 4, y_max + 4, y_max + 2],
         color="black")

# significance label
if p_value < 0.001:
    sig_text = "***"
elif p_value < 0.01:
    sig_text = "**"
elif p_value < 0.05:
    sig_text = "*"
else:
    sig_text = "ns"

plt.text(0.5, y_max + 4.5, sig_text,
         ha="center", fontsize=14)

plt.title("Pulse Rate Before vs After Meal")
plt.ylabel("Mean Pulse Rate")
plt.show()
