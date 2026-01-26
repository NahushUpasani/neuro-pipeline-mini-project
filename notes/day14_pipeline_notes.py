"""
DAY 14 — END-TO-END NEUROTECH PIPELINE (DEFENSIBLE WORKFLOW)

This file is NOTES ONLY. Keep it in every project.

Goal:
- Know the correct order of operations for neuro/BCI data
- Be able to defend every step

CANONICAL PIPELINE (MEMORIZE ORDER)
Raw data
 → Trial-level QC (FLAGS, not deletion)
 → Subject-level QC
 → Valid trial set
 → Aggregation (mean/median/trimmed)
 → Subject-level outputs
 → (Optional) Modeling / ML
 → Reporting & interpretation

STEP 1 — RAW DATA (DO NOT TOUCH)
- Raw data = original collected trials/signals
- Never overwrite raw
- Keep provenance (source/version)

STEP 2 — TRIAL-LEVEL QC (FLAGGING)
- Mark invalid trials, don’t delete
Examples:
- RT > task limit
- electrode pop / motion artifact
- missing response
Output:
- qc_flag column + documented rules

STEP 3 — SUBJECT-LEVEL QC
- Evaluate participants after trial QC
Examples:
- <70% valid trials
- persistent noise/noncompliance
Output:
- subject inclusion/exclusion table + criteria

STEP 4 — VALID TRIAL SET
- First dataset allowed downstream
Example:
valid_df = df[df["qc_flag"] == True]

STEP 5 — AGGREGATION (JUDGMENT ZONE)
- Group + summarize; decision affects meaning
- Mean sensitive to outliers
- Median safer under skew/outliers
Output:
- aggregated table + justification

STEP 6 — SUBJECT-LEVEL OUTPUTS
- Interpretable results per subject/condition
Output:
- final results table (optional plots later)

STEP 7 — MODELING/ML (ALWAYS LAST)
- ML amplifies errors; requires clean pipeline first

MATH (ONLY WHERE IT APPEARS)
- QC thresholds: inequalities
- Subject QC: proportions
- Aggregation: basic stats (mean/median)
- Features later: vectors/matrices
- ML later: probability/evaluation
- Calculus: only when optimization shows up
"""
