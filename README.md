# Clean Netflix Dataset

A data cleaning and preparation project based on the `netflix_titles.csv` dataset, focused on handling missing values, correcting duration inconsistencies, converting date columns and generating analysis-ready files.

## Objective

The project reads the original dataset from `data/netflix_titles.csv` and generates cleaned versions in CSV and Pickle formats, along with supporting reports documenting the data quality treatments applied.

The main steps include:

* Analyzing missing values by column.
* Filling missing text fields with `Unknown`.
* Correcting duration values incorrectly stored in the `rating` column.
* Converting `date_added` into a new datetime column.
* Splitting the `duration` column into a numeric value and a standardized unit.
* Exporting the cleaned dataset and data quality reports.

## Dataset

The original dataset contains:

* 8,807 records.
* 12 original columns.
* Content classified as either `Movie` or `TV Show`.

After the cleaning process, the dataset contains 15 columns, including the following new columns:

* `date_added_datetime`: datetime version of the `date_added` column.
* `duration_value`: numeric duration value.
* `duration_unit`: standardized duration unit, such as `minutes` or `seasons`.

## Generated Outputs

### Cleaned Dataset

* `outputs/netflix_titles_clean.csv`: cleaned CSV file prepared for data analysis and visualization.
* `outputs/netflix_titles_clean.pkl`: serialized Pickle version for direct reuse with pandas.

### Reports

* `outputs/missing_values_report.csv`: shows missing values before and after cleaning, as well as the treatment applied to each column.
* `outputs/mixed_type_columns_report.csv`: documents columns containing mixed data types and how they were normalized.
* `outputs/date_columns_report.csv`: records date column conversions, including the minimum and maximum dates found.

## Data Cleaning Steps

### Missing Values

Missing values in the `director`, `cast`, `country`, `date_added`, `rating` and `duration` columns are filled with `Unknown`.

### `rating` Column Correction

Some rows contain duration values, such as `74 min` or `1 Season`, incorrectly stored in the `rating` column.

The cleaning script identifies these cases, moves the value to the `duration` column when necessary and removes the incorrect value from `rating`.

### Date Conversion

The original `date_added` column is preserved as text to retain its original value.

A new column named `date_added_datetime` is created using `pd.to_datetime`.

Missing or invalid dates remain as `NaT` in the converted column.

### Duration Normalization

The `duration` column combines a numeric value and a unit in the same text field. To make the data easier to analyze, the project creates two separate columns:

* `duration_value`: integer duration value.
* `duration_unit`: standardized text representation of the duration unit.

Examples:

```text
90 min    -> duration_value = 90, duration_unit = minutes
2 Seasons -> duration_value = 2, duration_unit = seasons
```

## Notebook

The `notebook.ipynb` file contains an exploratory version of the data cleaning process, including:

* Date column analysis.
* Missing value treatment.
* Data conversion validation.
* Duration normalization.
* Export of the cleaned dataset and reports.
