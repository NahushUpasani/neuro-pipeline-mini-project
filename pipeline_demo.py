"""
Mini Project: Neuro Data Pipeline (QC → Aggregation → Outputs)

Goal:
- Simulate trial-level neuro/behavioral data
- Apply trial-level QC
- Apply subject-level QC
- Aggregate ONLY after QC
- Produce defensible subject-level outputs
"""

import pandas as pd
import numpy as np

# -----------------------------
# STEP 1 — RAW DATA (SIMULATED)
# -----------------------------
np.random.seed(42)

subjects = ["S01", "S02"]
conditions = ["visual", "auditory"]

rows = []
trial_id = 1

for subj in subjects:
    for cond in conditions:
        for _ in range(12):
            rt = np.random.normal(350 if cond == "visual" else 400, 30)
            rows.append({
                "subject": subj,
                "condition": cond,
                "trial": trial_id,
                "rt": rt
            })
            trial_id += 1

# Inject known bad trials (sanity checks)
rows.append({"subject": "S01", "condition": "visual",
            "trial": trial_id, "rt": 9000})
trial_id += 1
rows.append({"subject": "S02", "condition": "auditory",
            "trial": trial_id, "rt": -50})

df = pd.DataFrame(rows)

print("\nRAW DATA SUMMARY:")
print(df["rt"].describe())

# -----------------------------
# STEP 2 — TRIAL-LEVEL QC
# -----------------------------
RT_MIN = 150
RT_MAX = 1500

df["qc_flag"] = True
df["qc_reason"] = None

df.loc[df["rt"].isna(), ["qc_flag", "qc_reason"]] = (False, "missing_rt")
df.loc[df["rt"] < 0, ["qc_flag", "qc_reason"]] = (False, "negative_rt")
df.loc[(df["rt"] >= 0) & (df["rt"] < RT_MIN), [
    "qc_flag", "qc_reason"]] = (False, "rt_too_fast")
df.loc[df["rt"] > RT_MAX, ["qc_flag", "qc_reason"]] = (False, "rt_too_slow")

print("\nTRIAL QC FLAG COUNTS:")
print(df["qc_flag"].value_counts(dropna=False))

print("\nTRIAL QC — REJECTED TRIALS:")
print(
    df.loc[df["qc_flag"] == False,
           ["subject", "condition", "trial", "rt", "qc_reason"]]
)

# -----------------------------
# STEP 3 — SUBJECT-LEVEL QC
# -----------------------------
valid_trials = df[df["qc_flag"]]

subject_qc = (
    valid_trials
    .groupby("subject")
    .size()
    .reset_index(name="n_valid_trials")
)

MIN_TRIALS = 10
valid_subjects = subject_qc.loc[
    subject_qc["n_valid_trials"] >= MIN_TRIALS,
    "subject"
]

print("\nSUBJECT-LEVEL QC:")
print(subject_qc)

# -----------------------------
# STEP 4 — FINAL VALID DATASET
# -----------------------------
final_df = valid_trials[valid_trials["subject"].isin(valid_subjects)]

print("\nFINAL DATASET SIZE:", len(final_df))

# -----------------------------
# STEP 5 — AGGREGATION (JUDGMENT ZONE)
# -----------------------------
agg_median = (
    final_df
    .groupby(["subject", "condition"])["rt"]
    .median()
    .reset_index(name="median_rt")
)

agg_mean = (
    final_df
    .groupby(["subject", "condition"])["rt"]
    .mean()
    .reset_index(name="mean_rt")
)

print("\nAGGREGATED RESULTS (MEDIAN):")
print(agg_median)

print("\nAGGREGATED RESULTS (MEAN):")
print(agg_mean)

# -----------------------------
# STEP 6 — INTERPRETATION
# -----------------------------
print("""
INTERPRETATION NOTES:
- Trial-level QC removed impossible RTs (-50, 9000)
- Subject-level QC ensures sufficient valid data
- Aggregation happens ONLY after QC
- Median is safer under skew/outliers than mean
- These outputs are defensible and ML-ready
""")
