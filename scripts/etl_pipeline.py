"""
etlpiple.py — YouTube Trending Data ETL Pipeline

Purpose
-------
Single-file ETL script for the DVA Capstone YouTube trending analytics project.
It follows the same structure as the provided sample ETL pipeline:
1. Raw ingestion + full audit
2. Cleaning + transformation logging
3. Feature engineering for dashboard KPIs
4. Final validation
5. Exports for Tableau/dashboard work

Expected input
--------------
A YouTube trending CSV in data/raw/, commonly with columns such as:
video_id, trending_date, title, channel_title, category_id, categoryName,
publish_time or publishedAt, views, likes, dislikes, comment_count, country.

Usage
-----
python etlpiple.py \
  --input data/raw/youtube_trending.csv \
  --output-dir data/processed \
  --docs-dir docs \
  --tableau-dir data/tableau

The script is intentionally defensive: it handles missing optional columns and
creates all dashboard-ready exports that can be computed from the available data.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import numpy as np
import pandas as pd


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

NUMERIC_COLUMNS = ["views", "likes", "dislikes", "comment_count", "category_id"]
BOOLEAN_COLUMNS = ["comments_disabled", "ratings_disabled", "video_error_or_removed"]
TEXT_COLUMNS = ["title", "channel_title", "categoryName", "tags", "description", "country"]

CATEGORY_ID_MAP = {
    1: "Film & Animation",
    2: "Autos & Vehicles",
    10: "Music",
    15: "Pets & Animals",
    17: "Sports",
    18: "Short Movies",
    19: "Travel & Events",
    20: "Gaming",
    21: "Videoblogging",
    22: "People & Blogs",
    23: "Comedy",
    24: "Entertainment",
    25: "News & Politics",
    26: "Howto & Style",
    27: "Education",
    28: "Science & Technology",
    29: "Nonprofits & Activism",
    30: "Movies",
    31: "Anime/Animation",
    32: "Action/Adventure",
    33: "Classics",
    34: "Comedy",
    35: "Documentary",
    36: "Drama",
    37: "Family",
    38: "Foreign",
    39: "Horror",
    40: "Sci-Fi/Fantasy",
    41: "Thriller",
    42: "Shorts",
    43: "Shows",
    44: "Trailers",
}


# -----------------------------------------------------------------------------
# Utility helpers
# -----------------------------------------------------------------------------

def ensure_dirs(*dirs: Path) -> None:
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)


def safe_divide(numerator: pd.Series | float, denominator: pd.Series | float) -> pd.Series | float:
    """Divide while avoiding inf/NaN caused by zero denominators."""
    result = numerator / denominator
    if isinstance(result, pd.Series):
        return result.replace([np.inf, -np.inf], np.nan).fillna(0)
    if pd.isna(result) or np.isinf(result):
        return 0.0
    return result


def first_existing_column(df: pd.DataFrame, candidates: Iterable[str]) -> Optional[str]:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize common YouTube/Kaggle column variants to project standard names."""
    rename_map = {}
    for col in df.columns:
        cleaned = col.strip()
        lower = cleaned.lower()
        if lower in {"publish_time", "publishedat", "published_at", "published time"}:
            rename_map[col] = "publish_time"
        elif lower in {"trending_date", "trendingdate", "trending date"}:
            rename_map[col] = "trending_date"
        elif lower in {"channel_title", "channeltitle", "channel name", "channel"}:
            rename_map[col] = "channel_title"
        elif lower in {"comment_count", "comments", "commentcount"}:
            rename_map[col] = "comment_count"
        elif lower in {"category_name", "category", "categoryname"}:
            rename_map[col] = "categoryName"
        elif lower == "video id":
            rename_map[col] = "video_id"
        else:
            rename_map[col] = cleaned
    return df.rename(columns=rename_map)


# -----------------------------------------------------------------------------
# 01. Raw ingestion + audit
# -----------------------------------------------------------------------------

def load_raw_data(input_path: Path) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    df = pd.read_csv(input_path, dtype=str, encoding="utf-8", low_memory=False)
    return normalize_column_names(df)


def build_audit_report(df: pd.DataFrame) -> Dict:
    audit = {
        "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
        "columns": list(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_video_id_trending_date": None,
        "column_profiles": {},
    }

    if {"video_id", "trending_date"}.issubset(df.columns):
        audit["duplicate_video_id_trending_date"] = int(df.duplicated(["video_id", "trending_date"]).sum())

    for col in df.columns:
        sample_values = df[col].dropna().astype(str).unique()[:8].tolist()
        audit["column_profiles"][col] = {
            "dtype_raw": str(df[col].dtype),
            "null_count": int(df[col].isna().sum()),
            "null_pct": round(float(df[col].isna().mean() * 100), 2),
            "unique_count": int(df[col].nunique(dropna=True)),
            "sample_values": sample_values,
        }
    return audit


# -----------------------------------------------------------------------------
# 02. Cleaning + feature engineering
# -----------------------------------------------------------------------------

def parse_trending_date(series: pd.Series) -> pd.Series:
    """Parse common YouTube trending_date formats: YY.DD.MM, YYYY-MM-DD, MM/DD/YYYY."""
    s = series.astype(str).str.strip()

    parsed_yy_dd_mm = pd.to_datetime(s, format="%y.%d.%m", errors="coerce")
    parsed_general = pd.to_datetime(s, errors="coerce", utc=False)
    parsed = parsed_yy_dd_mm.fillna(parsed_general)
    return pd.to_datetime(parsed, errors="coerce")


def clean_boolean(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .map({"true": True, "false": False, "1": True, "0": False, "yes": True, "no": False})
        .fillna(False)
        .astype(bool)
    )


def infer_country_from_file(input_path: Path) -> Optional[str]:
    """Infer country from filenames like INvideos.csv, US_youtube_trending.csv."""
    name = input_path.name.upper()
    match = re.search(r"\b([A-Z]{2})VIDEOS\b|^([A-Z]{2})[_-]", name)
    if not match:
        return None
    return next(group for group in match.groups() if group)


def clean_and_transform(df: pd.DataFrame, input_path: Path) -> tuple[pd.DataFrame, Dict[str, str]]:
    log: Dict[str, str] = {}
    out = df.copy()

    # Step 01: trim text/object columns
    for col in out.columns:
        if out[col].dtype == object:
            out[col] = out[col].astype(str).str.strip().replace({"nan": np.nan, "None": np.nan, "": np.nan})
    log["step_01_text_trim"] = "Trimmed whitespace, converted blank/nan-like strings to null."

    # Step 02: parse dates
    if "trending_date" in out.columns:
        out["trending_date_raw"] = out["trending_date"]
        out["trending_date"] = parse_trending_date(out["trending_date"])
    else:
        out["trending_date"] = pd.NaT
    if "publish_time" in out.columns:
        out["publish_time_raw"] = out["publish_time"]
        out["publish_time"] = pd.to_datetime(out["publish_time"], errors="coerce", utc=True)
    else:
        out["publish_time"] = pd.NaT
    log["step_02_dates"] = "Parsed trending_date and publish_time into datetime fields; invalid values set to NaT."

    # Step 03: numeric conversion and invalid count handling
    for col in NUMERIC_COLUMNS:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    for col in ["views", "likes", "dislikes", "comment_count"]:
        if col in out.columns:
            out.loc[out[col] < 0, col] = np.nan
            out[col] = out[col].fillna(0).astype("int64")
        else:
            out[col] = 0
    if "category_id" in out.columns:
        out["category_id"] = out["category_id"].fillna(-1).astype("int64")
    log["step_03_numeric_metrics"] = "Converted views, likes, dislikes, comments, category_id to numeric; negative engagement counts reset to 0."

    # Step 04: boolean flags
    for col in BOOLEAN_COLUMNS:
        if col in out.columns:
            out[col] = clean_boolean(out[col])
        else:
            out[col] = False
    log["step_04_boolean_flags"] = "Standardized comments_disabled, ratings_disabled, and video_error_or_removed as Boolean values."

    # Step 05: text standardization
    for col in TEXT_COLUMNS:
        if col in out.columns:
            out[col] = out[col].fillna("UNKNOWN").astype(str).str.strip()
    if "channel_title" not in out.columns:
        out["channel_title"] = "UNKNOWN"
    if "title" not in out.columns:
        out["title"] = "UNKNOWN"
    log["step_05_text_standardization"] = "Filled missing title/channel/category/country text fields with UNKNOWN."

    # Step 06: category mapping
    if "categoryName" not in out.columns or out["categoryName"].eq("UNKNOWN").all():
        out["categoryName"] = out.get("category_id", pd.Series(-1, index=out.index)).map(CATEGORY_ID_MAP).fillna("Other/Unknown")
    out["categoryName"] = out["categoryName"].replace({"": "Other/Unknown", "UNKNOWN": "Other/Unknown"})
    log["step_06_categories"] = "Mapped category_id to readable categoryName where categoryName was missing."

    # Step 07: country handling and India flag
    if "country" not in out.columns:
        inferred_country = infer_country_from_file(input_path)
        out["country"] = inferred_country if inferred_country else "GLOBAL/UNKNOWN"
    out["country"] = out["country"].astype(str).str.upper().str.strip()
    out["is_india"] = out["country"].isin(["IN", "INDIA"])
    log["step_07_country_india"] = "Standardized country values and created is_india flag for India-specific dashboard."

    # Step 08: date-derived dimensions
    out["trending_year"] = out["trending_date"].dt.year
    out["trending_month"] = out["trending_date"].dt.month
    out["trending_month_name"] = out["trending_date"].dt.month_name()
    out["trending_day_of_week"] = out["trending_date"].dt.day_name()
    out["publish_hour"] = out["publish_time"].dt.hour.fillna(-1).astype(int)
    out["publish_day_of_week"] = out["publish_time"].dt.day_name().fillna("Unknown")
    log["step_08_date_dimensions"] = "Created year, month, month name, day of week, publish hour, and publish day dimensions."

    # Step 09: time-to-trend metrics
    published_date = out["publish_time"].dt.tz_convert(None).dt.normalize() if pd.api.types.is_datetime64tz_dtype(out["publish_time"]) else out["publish_time"].dt.normalize()
    trending_date = out["trending_date"].dt.normalize()
    out["time_to_trend_days"] = (trending_date - published_date).dt.days
    out.loc[out["time_to_trend_days"] < 0, "time_to_trend_days"] = np.nan
    out["time_to_trend_days"] = out["time_to_trend_days"].fillna(0).astype(int)
    log["step_09_time_to_trend"] = "Computed time_to_trend_days from publish_time to trending_date; negative/invalid durations set to 0."

    # Step 10: engagement, sentiment, virality features
    out["engagement_count"] = out["likes"] + out["comment_count"]
    out["engagement_rate"] = safe_divide(out["engagement_count"], out["views"])
    out["like_rate"] = safe_divide(out["likes"], out["views"])
    out["comment_rate"] = safe_divide(out["comment_count"], out["views"])
    out["dislike_ratio"] = safe_divide(out["dislikes"], out["likes"] + out["dislikes"])
    out["like_to_dislike_ratio"] = safe_divide(out["likes"], out["dislikes"].replace(0, np.nan)).replace(0, np.nan)
    out["like_to_dislike_ratio"] = out["like_to_dislike_ratio"].fillna(out["likes"])
    out["views_per_day_to_trend"] = safe_divide(out["views"], out["time_to_trend_days"].replace(0, 1))
    out["virality_score"] = out["views_per_day_to_trend"] * (1 + out["engagement_rate"])
    out["positive_engagement_rate"] = safe_divide(out["likes"], out["likes"] + out["dislikes"] + out["comment_count"])
    log["step_10_engagement_features"] = "Created engagement rate, like/comment rates, dislike ratio, like-to-dislike ratio, views/day, and virality score."

    # Step 11: repeated trending and channel consistency features
    if "video_id" in out.columns:
        out["times_trended"] = out.groupby("video_id")["video_id"].transform("count")
        out["is_repeat_trending_video"] = out["times_trended"] > 1
    else:
        out["video_id"] = np.arange(len(out)).astype(str)
        out["times_trended"] = 1
        out["is_repeat_trending_video"] = False
    out["channel_trending_count"] = out.groupby("channel_title")["video_id"].transform("count")
    out["channel_avg_views"] = out.groupby("channel_title")["views"].transform("mean")
    log["step_11_repeat_channel_features"] = "Added times_trended, repeat trending flag, channel trending count, and channel average views."

    # Step 12: duplicate removal
    before = len(out)
    dedupe_keys = [col for col in ["video_id", "trending_date"] if col in out.columns]
    if len(dedupe_keys) == 2:
        out = out.drop_duplicates(subset=dedupe_keys, keep="first")
    else:
        out = out.drop_duplicates(keep="first")
    removed = before - len(out)
    log["step_12_deduplication"] = f"Removed {removed} duplicate rows using video_id + trending_date when available."

    # Final cleanup for export friendliness
    out["trending_month_name"] = out["trending_month_name"].fillna("Unknown")
    out["trending_day_of_week"] = out["trending_day_of_week"].fillna("Unknown")

    return out, log


# -----------------------------------------------------------------------------
# 03. KPI computation + Tableau/dashboard exports
# -----------------------------------------------------------------------------

def compute_kpis(df: pd.DataFrame) -> Dict[str, object]:
    top_video_idx = df["views"].idxmax() if len(df) else None

    category_group = df.groupby("categoryName", dropna=False).agg(
        total_views=("views", "sum"),
        avg_engagement_rate=("engagement_rate", "mean"),
        trending_frequency=("video_id", "count"),
        avg_virality_score=("virality_score", "mean"),
    )

    channel_group = df.groupby("channel_title", dropna=False).agg(
        total_views=("views", "sum"),
        avg_views=("views", "mean"),
        avg_engagement_rate=("engagement_rate", "mean"),
        trending_videos=("video_id", "count"),
    )

    india = df[df["is_india"]]
    global_engagement = float(df["engagement_rate"].mean()) if len(df) else 0
    india_engagement = float(india["engagement_rate"].mean()) if len(india) else 0

    kpis = {
        "total_rows_after_cleaning": int(len(df)),
        "total_unique_videos": int(df["video_id"].nunique()),
        "total_views": int(df["views"].sum()),
        "total_likes": int(df["likes"].sum()),
        "total_comments": int(df["comment_count"].sum()),
        "avg_engagement_rate_pct": round(float(df["engagement_rate"].mean() * 100), 3) if len(df) else 0,
        "avg_views_per_video": round(float(df.groupby("video_id")["views"].max().mean()), 2) if len(df) else 0,
        "like_to_dislike_ratio": round(float(safe_divide(df["likes"].sum(), max(df["dislikes"].sum(), 1))), 2),
        "best_upload_hour": int(df.groupby("publish_hour")["views"].mean().idxmax()) if len(df) else None,
        "best_day_to_post": str(df.groupby("publish_day_of_week")["engagement_rate"].mean().idxmax()) if len(df) else None,
        "avg_time_to_trend_days": round(float(df["time_to_trend_days"].mean()), 2) if len(df) else 0,
        "fastest_viral_video": str(df.loc[df["virality_score"].idxmax(), "title"]) if len(df) else None,
        "top_channel_by_views": str(channel_group["total_views"].idxmax()) if len(channel_group) else None,
        "most_engaging_channel": str(channel_group["avg_engagement_rate"].idxmax()) if len(channel_group) else None,
        "channel_dominance_pct": round(float(channel_group["total_views"].max() / max(df["views"].sum(), 1) * 100), 2) if len(channel_group) else 0,
        "top_category_by_views": str(category_group["total_views"].idxmax()) if len(category_group) else None,
        "top_category_by_engagement": str(category_group["avg_engagement_rate"].idxmax()) if len(category_group) else None,
        "most_consistent_category": str(category_group["trending_frequency"].idxmax()) if len(category_group) else None,
        "fastest_growing_category": str(category_group["avg_virality_score"].idxmax()) if len(category_group) else None,
        "india_best_posting_hour": int(india.groupby("publish_hour")["engagement_rate"].mean().idxmax()) if len(india) else None,
        "india_highest_engagement_category": str(india.groupby("categoryName")["engagement_rate"].mean().idxmax()) if len(india) else None,
        "india_avg_time_to_trend_days": round(float(india["time_to_trend_days"].mean()), 2) if len(india) else None,
        "india_vs_global_engagement_rate_pct_point_gap": round((india_engagement - global_engagement) * 100, 3),
        "top_video_by_views": str(df.loc[top_video_idx, "title"]) if top_video_idx is not None else None,
    }
    return kpis


def export_tableau_files(df: pd.DataFrame, tableau_dir: Path) -> Dict[str, str]:
    exports: Dict[str, str] = {}

    def save_csv(dataframe: pd.DataFrame, filename: str) -> None:
        path = tableau_dir / filename
        dataframe.to_csv(path, index=False)
        exports[filename] = str(path)

    # 1. Overview time series
    save_csv(
        df.groupby("trending_date", dropna=False).agg(
            total_views=("views", "sum"),
            total_likes=("likes", "sum"),
            total_comments=("comment_count", "sum"),
            trending_videos=("video_id", "count"),
            avg_engagement_rate=("engagement_rate", "mean"),
            avg_views_per_video=("views", "mean"),
            like_to_dislike_ratio=("like_to_dislike_ratio", "mean"),
        ).reset_index(),
        "overview_time_series.csv",
    )

    # 2. Timing & virality
    save_csv(
        df.groupby(["publish_day_of_week", "publish_hour"], dropna=False).agg(
            avg_views=("views", "mean"),
            avg_engagement_rate=("engagement_rate", "mean"),
            avg_virality_score=("virality_score", "mean"),
            video_count=("video_id", "count"),
            avg_time_to_trend_days=("time_to_trend_days", "mean"),
        ).reset_index(),
        "timing_virality.csv",
    )

    # 3. Channel performance
    save_csv(
        df.groupby("channel_title", dropna=False).agg(
            total_views=("views", "sum"),
            avg_views_per_video=("views", "mean"),
            avg_engagement_rate=("engagement_rate", "mean"),
            trending_videos=("video_id", "count"),
            avg_virality_score=("virality_score", "mean"),
        ).reset_index().sort_values("total_views", ascending=False),
        "channel_performance.csv",
    )

    # 4. India dashboard data
    save_csv(
        df[df["is_india"]].groupby(["categoryName", "publish_hour"], dropna=False).agg(
            total_views=("views", "sum"),
            avg_engagement_rate=("engagement_rate", "mean"),
            avg_time_to_trend_days=("time_to_trend_days", "mean"),
            video_count=("video_id", "count"),
        ).reset_index(),
        "india_dashboard.csv",
    )

    # 5. Category performance
    save_csv(
        df.groupby("categoryName", dropna=False).agg(
            total_views=("views", "sum"),
            total_likes=("likes", "sum"),
            total_comments=("comment_count", "sum"),
            avg_likes_per_video=("likes", "mean"),
            comments_per_video=("comment_count", "mean"),
            avg_engagement_rate=("engagement_rate", "mean"),
            trending_frequency=("video_id", "count"),
            avg_virality_score=("virality_score", "mean"),
            positive_engagement_rate=("positive_engagement_rate", "mean"),
            dislike_ratio=("dislike_ratio", "mean"),
        ).reset_index().sort_values("total_views", ascending=False),
        "category_performance.csv",
    )

    # 6. Top videos table
    save_csv(
        df[[
            "video_id", "title", "channel_title", "categoryName", "country", "trending_date",
            "views", "likes", "dislikes", "comment_count", "engagement_rate",
            "dislike_ratio", "virality_score", "time_to_trend_days", "is_india"
        ]].sort_values(["views", "engagement_rate"], ascending=False).head(100),
        "top_100_videos.csv",
    )

    # 7. Date x engagement heatmap base
    save_csv(
        df.groupby(["trending_date", "trending_day_of_week"], dropna=False).agg(
            total_views=("views", "sum"),
            avg_engagement_rate=("engagement_rate", "mean"),
            video_count=("video_id", "count"),
        ).reset_index(),
        "date_engagement_heatmap.csv",
    )

    return exports


# -----------------------------------------------------------------------------
# 04. Validation
# -----------------------------------------------------------------------------

def validate_clean_data(df: pd.DataFrame) -> Dict[str, object]:
    checks = {
        "rows_after_cleaning": int(len(df)),
        "required_columns_present": True,
        "non_negative_metrics": True,
        "engagement_rate_range_valid": True,
        "no_duplicate_video_trending_date": True,
        "invalid_trending_dates": int(df["trending_date"].isna().sum()),
    }

    required = [
        "video_id", "title", "channel_title", "categoryName", "trending_date",
        "views", "likes", "dislikes", "comment_count", "engagement_rate", "virality_score"
    ]
    missing = [col for col in required if col not in df.columns]
    checks["missing_required_columns"] = missing
    checks["required_columns_present"] = len(missing) == 0

    metric_cols = ["views", "likes", "dislikes", "comment_count"]
    checks["non_negative_metrics"] = bool((df[metric_cols] >= 0).all().all())
    checks["engagement_rate_range_valid"] = bool((df["engagement_rate"] >= 0).all())
    checks["no_duplicate_video_trending_date"] = bool(df.duplicated(["video_id", "trending_date"]).sum() == 0)

    if not checks["required_columns_present"]:
        raise AssertionError(f"Missing required columns after ETL: {missing}")
    if not checks["non_negative_metrics"]:
        raise AssertionError("Negative values found in core metrics.")
    if not checks["engagement_rate_range_valid"]:
        raise AssertionError("Invalid negative engagement rates found.")
    if not checks["no_duplicate_video_trending_date"]:
        raise AssertionError("Duplicate video_id + trending_date records remain.")

    return checks


# -----------------------------------------------------------------------------
# Main orchestration
# -----------------------------------------------------------------------------

def run_pipeline(input_path: Path, output_dir: Path, docs_dir: Path, tableau_dir: Path) -> None:
    ensure_dirs(output_dir, docs_dir, tableau_dir)

    raw_df = load_raw_data(input_path)
    audit = build_audit_report(raw_df)
    (docs_dir / "cleaning_audit.json").write_text(json.dumps(audit, indent=2, default=str), encoding="utf-8")

    clean_df, transformation_log = clean_and_transform(raw_df, input_path)
    validation = validate_clean_data(clean_df)
    transformation_log["step_13_validation"] = "All validation assertions passed; see docs/etl_validation_summary.json."

    cleaned_path = output_dir / "youtube_trending_clean.csv"
    clean_df.to_csv(cleaned_path, index=False)

    kpis = compute_kpis(clean_df)
    exports = export_tableau_files(clean_df, tableau_dir)

    (docs_dir / "etl_transformation_log.json").write_text(json.dumps(transformation_log, indent=2), encoding="utf-8")
    (docs_dir / "etl_validation_summary.json").write_text(json.dumps(validation, indent=2, default=str), encoding="utf-8")
    (docs_dir / "kpi_summary.json").write_text(json.dumps(kpis, indent=2, default=str), encoding="utf-8")
    (docs_dir / "tableau_exports_manifest.json").write_text(json.dumps(exports, indent=2), encoding="utf-8")

    print("ETL complete")
    print(f"Raw audit:              {docs_dir / 'cleaning_audit.json'}")
    print(f"Cleaned data:           {cleaned_path}")
    print(f"Transformation log:     {docs_dir / 'etl_transformation_log.json'}")
    print(f"Validation summary:     {docs_dir / 'etl_validation_summary.json'}")
    print(f"KPI summary:            {docs_dir / 'kpi_summary.json'}")
    print(f"Tableau export folder:  {tableau_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Trending Data ETL Pipeline")
    parser.add_argument("--input", required=True, type=Path, help="Path to raw YouTube trending CSV")
    parser.add_argument("--output-dir", default=Path("data/processed"), type=Path)
    parser.add_argument("--docs-dir", default=Path("docs"), type=Path)
    parser.add_argument("--tableau-dir", default=Path("data/tableau"), type=Path)
    args = parser.parse_args()

    run_pipeline(args.input, args.output_dir, args.docs_dir, args.tableau_dir)
