# 📘 Data Dictionary

## Dataset Summary

| Item | Details |
|---|---|
| Dataset name | YouTube Trending Videos Dataset |
| Source | YouTube public trending data (Kaggle / API-based dataset) |
| Raw file name | trending_videos.csv |
| Last updated | Based on dataset (e.g., 2023 or project dataset version) |
| Granularity | One row per video per trending date |

---

## Column Definitions

| Column Name | Data Type | Description | Example Value | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| video_id | string | Unique identifier of each video | Xyz123Abc | EDA, KPI, Tableau | Removed duplicates using video_id + trending_date |
| title | string | Title of the video | Top 10 Moments | EDA | Cleaned special characters, trimmed text |
| channel_title | string | Name of the YouTube channel | T-Series | KPI, Channel Dashboard | Standardized casing |
| categoryName | string | Category of video (e.g., Music, Gaming) | Music | Category Dashboard | Mapped IDs to names |
| publish_time | datetime | When video was uploaded | 2023-08-01 18:30:00 | Timing Dashboard | Converted to datetime format |
| trending_date | date | Date when video appeared in trending | 2023-08-03 | All dashboards | Standardized date format |
| views | int | Total number of views | 1500000 | KPI, All dashboards | Removed nulls, ensured numeric |
| likes | int | Total likes | 50000 | KPI, Engagement Analysis | Filled nulls with 0 |
| dislikes | int | Total dislikes | 2000 | Sentiment Analysis | Nullable in some datasets |
| comment_count | int | Number of comments | 8000 | Engagement KPI | Nulls replaced with 0 |
| comments_disabled | boolean | Whether comments are disabled | False | Data Quality | Converted to boolean |
| ratings_disabled | boolean | Whether ratings are disabled | False | Data Quality | Converted to boolean |
| video_error_or_removed | boolean | Whether video was removed | False | Data Quality | Filtered invalid rows |
| tags | string | Video tags | music, trending | EDA | Cleaned delimiter issues |
| description | string | Video description | Official music video | EDA | Not heavily used |

---

## Derived Columns

| Derived Column | Logic | Business Meaning |
|---|---|---|
| engagement_rate | (likes + comment_count) / views | Measures content quality |
| like_dislike_ratio | likes / (likes + dislikes) | Audience sentiment |
| views_per_video | total_views / total_videos | Content efficiency |
| time_to_trend | trending_date - publish_time | Speed of virality |
| virality_score | views / days_trending | Growth speed |
| publish_hour | Extract hour from publish_time | Best upload timing |
| publish_day | Day of week from publish_time | Weekly trend analysis |
| views_per_day_trending | views / days_in_trending | Sustained performance |
| category_engagement_rate | avg engagement_rate per category | Category performance |
| channel_avg_views | avg views per channel | Channel consistency |

---

## Data Quality Notes

- Duplicate records handled using composite key (video_id + trending_date)
- Missing values in likes, dislikes, comments filled with 0
- Some videos had disabled engagement → excluded from KPIs
- Category IDs mapped to readable names
- Outliers retained (important for virality insights)
- Time formats standardized
- Some datasets missing dislike counts (API limitation)
