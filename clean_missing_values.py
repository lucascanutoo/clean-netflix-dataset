from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/netflix_titles.csv")
OUTPUT_DIR = Path("outputs")
CLEAN_CSV_PATH = OUTPUT_DIR / "netflix_titles_clean.csv"
CLEAN_PICKLE_PATH = OUTPUT_DIR / "netflix_titles_clean.pkl"
MISSING_REPORT_PATH = OUTPUT_DIR / "missing_values_report.csv"
MIXED_TYPE_REPORT_PATH = OUTPUT_DIR / "mixed_type_columns_report.csv"
DATE_REPORT_PATH = OUTPUT_DIR / "date_columns_report.csv"


def build_missing_report(before: pd.DataFrame, after: pd.DataFrame) -> pd.DataFrame:
    treatments = {
        "show_id": "Sem ausentes; mantida.",
        "type": "Sem ausentes; mantida.",
        "title": "Sem ausentes; mantida.",
        "director": "Ausentes preenchidos com 'Unknown'.",
        "cast": "Ausentes preenchidos com 'Unknown'.",
        "country": "Ausentes preenchidos com 'Unknown'.",
        "date_added": "Ausentes preenchidos com 'Unknown' na coluna original; datetime derivado usa NaT.",
        "release_year": "Sem ausentes; mantida como ano numerico.",
        "rating": "Valores de duracao deslocados para duration; ausentes preenchidos com 'Unknown'.",
        "duration": "Duracoes deslocadas de rating corrigidas; ausentes restantes preenchidos com 'Unknown'.",
        "listed_in": "Sem ausentes; mantida.",
        "description": "Sem ausentes; mantida.",
    }

    rows = []
    for column in before.columns:
        rows.append(
            {
                "column": column,
                "missing_before": int(before[column].isna().sum()),
                "missing_before_pct": round(before[column].isna().mean() * 100, 2),
                "missing_after": int(after[column].isna().sum()),
                "treatment": treatments[column],
            }
        )

    return pd.DataFrame(rows)


def build_mixed_type_report() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "column": "duration",
                "issue": "Valores combinavam numero e unidade no mesmo texto, como '90 min' e '2 Seasons'.",
                "treatment": "Criadas duration_value como numero inteiro e duration_unit como unidade padronizada.",
                "new_columns": "duration_value, duration_unit",
            }
        ]
    )


def build_date_report(before: pd.DataFrame, after: pd.DataFrame) -> pd.DataFrame:
    date_added_datetime = after["date_added_datetime"]

    return pd.DataFrame(
        [
            {
                "column": "date_added",
                "original_dtype": str(before["date_added"].dtype),
                "converted_column": "date_added_datetime",
                "converted_dtype": str(date_added_datetime.dtype),
                "missing_before": int(before["date_added"].isna().sum()),
                "nat_after_conversion": int(date_added_datetime.isna().sum()),
                "min_date": date_added_datetime.min().date().isoformat(),
                "max_date": date_added_datetime.max().date().isoformat(),
                "treatment": "Convertida com pd.to_datetime; datas ausentes/invalidas permanecem como NaT.",
            },
            {
                "column": "release_year",
                "original_dtype": str(before["release_year"].dtype),
                "converted_column": "",
                "converted_dtype": "",
                "missing_before": int(before["release_year"].isna().sum()),
                "nat_after_conversion": "",
                "min_date": "",
                "max_date": "",
                "treatment": "Mantida como ano numerico, pois nao contem mes e dia para formar data completa.",
            },
        ]
    )


def clean_netflix_titles(df: pd.DataFrame) -> pd.DataFrame:
    clean = df.copy()

    duration_in_rating = clean["rating"].astype("string").str.contains(
        r"\b(?:min|Season|Seasons)\b", case=False, na=False, regex=True
    )
    duration_missing = duration_in_rating & clean["duration"].isna()
    clean.loc[duration_missing, "duration"] = clean.loc[duration_missing, "rating"]
    clean.loc[duration_in_rating, "rating"] = pd.NA

    date_added_text = clean["date_added"].astype("string").str.strip()
    clean["date_added_datetime"] = pd.to_datetime(
        date_added_text, format="%B %d, %Y", errors="coerce"
    )

    columns_to_unknown = [
        "director",
        "cast",
        "country",
        "date_added",
        "rating",
        "duration",
    ]
    clean[columns_to_unknown] = clean[columns_to_unknown].fillna("Unknown")

    duration_parts = clean["duration"].str.extract(
        r"^(?P<value>\d+)\s+(?P<unit>min|Season|Seasons)$"
    )
    clean["duration_value"] = duration_parts["value"].astype("int64")
    clean["duration_unit"] = (
        duration_parts["unit"]
        .str.lower()
        .replace({"min": "minutes", "season": "seasons"})
    )

    return clean


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    clean = clean_netflix_titles(df)

    missing_report = build_missing_report(df, clean)
    mixed_type_report = build_mixed_type_report()
    date_report = build_date_report(df, clean)

    clean.to_csv(CLEAN_CSV_PATH, index=False)
    clean.to_pickle(CLEAN_PICKLE_PATH)
    missing_report.to_csv(MISSING_REPORT_PATH, index=False)
    mixed_type_report.to_csv(MIXED_TYPE_REPORT_PATH, index=False)
    date_report.to_csv(DATE_REPORT_PATH, index=False)

    print(f"Original shape: {df.shape}")
    print(f"Clean shape: {clean.shape}")
    print(f"Clean CSV dataset: {CLEAN_CSV_PATH}")
    print(f"Clean pickle dataset: {CLEAN_PICKLE_PATH}")
    print(f"Missing report: {MISSING_REPORT_PATH}")
    print(f"Mixed type report: {MIXED_TYPE_REPORT_PATH}")
    print(f"Date report: {DATE_REPORT_PATH}")
    print("\nDate columns report:")
    print(date_report.to_string(index=False))
    print("\nClean dtypes:")
    print(clean[["date_added_datetime", "release_year", "duration_value", "duration_unit"]].dtypes)


if __name__ == "__main__":
    main()
