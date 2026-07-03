# Complete Example: Production-Ready Skill

This example demonstrates all key skill authoring patterns in one place.

## The Skill: csv-data-analyzer

```yaml
---
name: csv-data-analyzer
description: When a user uploads a file with .csv extension, proactively run a
  comprehensive data analysis including summary statistics, missing value
  detection, correlation analysis, and automatic visualization generation.
allowed-tools: |
  bash: python, cat, head
  Read, Write
---

# CSV Data Analyzer

<task>
Perform comprehensive automated analysis of CSV data with zero user prompting.
Deliver complete insights in first response.
</task>

<validation>
Before processing:
- Verify file has .csv extension
- Check file is readable and properly formatted
- Confirm at least one numeric column exists
- Validate data types are inferrable
</validation>

<execution>
1. Run `python analyze_csv.py --file [filename]`
2. The script performs:
   - Summary statistics (mean, median, std, quartiles)
   - Missing value analysis
   - Correlation matrix for numeric columns
   - Distribution analysis
   - Outlier detection
3. Generate three visualizations:
   - Correlation heatmap
   - Distribution histograms for key columns
   - Time series plot (if date column detected)
</execution>

<output_format>
Deliver in this exact structure:

## Data Overview
- Rows: [count]
- Columns: [count]
- Memory usage: [size]

## Key Findings
- [3-5 bullet points of actionable insights]
- Highlight any data quality issues in **bold**

## Summary Statistics
[Table of statistics for numeric columns]

## Visualizations
[Embedded charts]

## Recommendations
- [Specific next steps based on data characteristics]

Save full report to `analysis_report.md`
</output_format>

<critical_rules>
- Complete the ENTIRE analysis before responding
- Never ask "What would you like me to analyze?"
- Never ask "What columns are you interested in?"
- Never say "I can help you with..." or offer options
- If errors occur, fix them and continue (don't ask for help)
- Be thorough and complete in first response
</critical_rules>

## Examples

### Example 1: Sales Data
**User uploads:** `Q3_sales_data.csv`

**Expected output:**
```
## Data Overview
- Rows: 1,247
- Columns: 8 (5 numeric, 3 categorical)
- Memory usage: 156 KB

## Key Findings
- **West region outperformed by 23%** with $2.3M revenue
- **15 missing values** in shipping_cost column (1.2% of data)
- Strong correlation (0.87) between marketing_spend and revenue
- Seasonal pattern detected: peaks in months 7 and 11

[...full analysis continues...]
```

### Example 2: Customer Survey
**User uploads:** `customer_feedback.csv`

**Expected output:**
```
## Data Overview
- Rows: 523
- Columns: 12 (3 numeric, 9 text)

## Key Findings
- **78% positive sentiment** overall
- Top complaint: "shipping delays" (mentioned 89 times)
- **32 incomplete responses** should be excluded from analysis
- Net Promoter Score: 67 (considered excellent)

[...full analysis continues...]
```

## Reference: Analysis Techniques

### Missing Value Strategies
- < 5% missing: Drop rows
- 5-40% missing: Flag in report, consider imputation
- > 40% missing: Warn that column may not be useful

### Outlier Detection
- Use IQR method: Q1 - 1.5*IQR to Q3 + 1.5*IQR
- Flag but don't automatically remove
- Report count and percentage

### Visualization Choices
- 1-2 numeric columns: Histogram + box plot
- 3+ numeric columns: Correlation heatmap
- Time series data: Line plot with trend
- Categorical: Bar chart of frequencies
```

## Why This Example Works

### Level 1 (Metadata) - The Trigger
- Specific condition: "file with .csv extension"
- Proactive verbs: "proactively run", "generate"
- Concrete deliverables: "summary statistics, missing value detection, correlation analysis, visualization generation"

### Level 2 (Instructions) - The Workflow
- XML tags create clear phases: `<validation>`, `<execution>`, `<output_format>`, `<critical_rules>`
- Explicit negative constraints override Claude's default helpful-question-asking behavior
- Exact output format specification eliminates ambiguity

### Level 3 (Resources) - The Execution
- Script reference (`analyze_csv.py`) - execution happens outside context
- Reference section for domain knowledge
- Examples show exact expected output

### Personality Override
The `<critical_rules>` section explicitly forbids Claude's default behaviors:
- No asking questions
- No offering options
- No waiting for direction
- Complete everything in first response

This transforms Claude from a passive assistant into a proactive specialist.
