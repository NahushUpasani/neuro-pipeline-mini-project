# neuro-pipeline-mini-project

Learning neurotech data pipelines (QC, aggregation, reproducibility)

End-to-end toy pipeline showing the correct order:

raw data → trial-level QC → subject-level QC → valid dataset → aggregation → outputs

## What this demonstrates
- QC before aggregation (aggregation after QC prevents irreversible distortion)
- Trial-level rejection with reasons (e.g., impossible RTs)
- Subject-level checks for sufficient valid data
- Mean vs median aggregation and why median is safer under outliers

## How to run
```bash
python pipeline_demo.py
This script intentionally includes extreme RT artifacts to demonstrate why QC must precede aggregation.