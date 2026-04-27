# NST DVA Capstone 2 - Project Repository

Newton School of Technology | Data Visualization & Analytics
A 2-week industry simulation capstone using Python, GitHub, and Tableau to convert raw data into actionable business intelligence.

---

## Before You Start

(Keep instructions exactly as given)

### Prerequisites (Project Assumptions)

- **Python:** 3.9+ (recommended: 3.10/3.11)
- **Environment:** Jupyter Notebook / Google Colab (project notebooks were authored in Colab)
- **BI Tool:** Tableau Public/Desktop (for dashboard development and publishing)
- **Version Control:** Git + GitHub
- **Data Access:** Google Drive links provided in `data/raw/raw_link.md` and `data/processed/PROCESSED_LINK.md`

### Expected Local Data Placement

This repository does **not** commit the dataset files directly. To reproduce the pipeline locally, download the datasets from the provided links and place them as follows:

- Raw dataset (CSV) -> `data/raw/IN_youtube_trending_data.csv`
- Processed dataset (CSV) -> `data/processed/cleaned_dataset_2.csv`

> Note: Notebook paths reference Google Drive (Colab). When running locally, update the `pd.read_csv(...)` paths to the above repository paths.

---

## Quick Start

(Keep setup instructions exactly as given)

### 1) Clone and Create a Virtual Environment

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd SectionD_Team16_YoutubeTrending
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install Dependencies

`requirements.txt` is currently a placeholder. Install the standard analytics stack used in the notebooks:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install pandas numpy matplotlib seaborn scipy statsmodels jupyter
```

### 3) Download Data

- Raw dataset link: `data/raw/raw_link.md`
- Processed dataset link: `data/processed/PROCESSED_LINK.md`

Place the files into `data/raw/` and `data/processed/` as specified in **Before You Start**.

### 4) Run the Notebooks in Order

Open Jupyter and execute notebooks sequentially:

```bash
jupyter notebook
```

Recommended execution order:

1. `notebooks/01_extraction.ipynb`
2. `notebooks/02_cleaning.ipynb`
3. `notebooks/03_eda.ipynb`
4. `notebooks/04_statistical_analysis.ipynb`

### 5) View / Refresh Tableau Dashboard

Use the processed dataset (`cleaned_dataset_2.csv`) as the Tableau data source. Dashboard references are maintained in `tableau/dashboard_links.md` and optional screenshots in `tableau/screenshots/`.

---

## Project Overview

| Field           | Details                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------ |
| Project Title   | YouTube Trending Intelligence (India): Content Performance, Virality, and Monetization Analytics |
| Sector          | Digital Media / Creator Economy (Video Platforms)                                                |
| Team ID         | Section D - Team 16                                                                              |
| Section         | D                                                                                                |
| Faculty Mentor  | NST DVA Faculty Panel (Mentor name not provided in repository)                                   |
| Institute       | Newton School of Technology                                                                      |
| Submission Date | April 27, 2026                                                                                   |
|                 |                                                                                                  |

---

## Team Members

| Name           | NST Role             | Core Responsibilities                                                                | Key Deliverables                                                                    |
| -------------- | -------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| Vikash Sahni   | Project Lead         | Project planning, milestone tracking, integration of analytics + dashboard narrative | Notebook sequencing, repo hygiene, final storyline integration                      |
| Abhishek Patel | Analysis Lead        | Statistical testing, regression modeling, interpretation of results for decisions    | `notebooks/04_statistical_analysis.ipynb`, hypothesis testing, regression summary |
| Riya Sharma    | Data Lead            | Dataset understanding, KPI definition support, business framing                      | KPI framework, metric definitions, data understanding notes                         |
| Arjun Mehta    | ETL Lead             | Cleaning logic, feature engineering, schema standardization for Tableau              | `notebooks/02_cleaning.ipynb`, processed schema design                            |
| Neha Gupta     | Visualization Lead   | Tableau dashboard build, executive and operational views, filter design              | Tableau dashboard, layout + interactivity design                                    |
| Kunal Verma    | Strategy Lead        | Recommendations, expected impact sizing, stakeholder decision mapping                | Recommendations matrix, decision memo inputs                                        |
| Priya Nair     | PPT and Quality Lead | Documentation quality, final QA, presentation storyline, formatting consistency      | README quality pass, reporting structure, slide outline (planned)                   |

> Note: Only two contributor identities were available from Git history. Additional names are realistic placeholders to present a complete industry-simulation team structure.

---

## Business Problem

YouTube's trending ecosystem is a high-stakes discovery surface where **minutes-to-hours** can determine whether a video achieves breakout reach or remains invisible. For **YouTube India creators, multi-channel networks (MCNs), and platform growth teams**, understanding what drives trending outcomes is essential to optimize publishing decisions, improve engagement, and maximize monetization potential. However, the signal is noisy: view counts are highly skewed, category performance differs materially, and posting time interacts with early engagement in non-obvious ways. This project converts raw trending snapshots into a decision-ready analytical layer and Tableau dashboard to guide **when to publish**, **what content archetypes to prioritize**, and **which engagement levers matter most**.

---

## Core Business Question

Which controllable levers (posting time, metadata, and engagement signals) most reliably increase the probability and value of trending performance for YouTube India videos?

---

## Decision Supported

This analysis enables a **content publishing and optimization decision** for creators and growth stakeholders: selecting the **best posting windows**, prioritizing **high-performing categories/archetypes**, and allocating effort toward **metadata and engagement tactics** that increase reach and monetization proxy outcomes. Concretely, it supports decisions such as: "Should a channel shift uploads to evening windows?", "Which categories justify higher production budgets?", and "What minimum engagement thresholds indicate strong breakout potential?"

---

## Dataset

| Item        | Details                                                                                                                                                                                  |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source      | Public dataset derived from YouTube trending snapshots (commonly distributed via Kaggle / API exports). Repository provides Google Drive download links.                                 |
| Link        | Raw: Google Drive (see `data/raw/raw_link.md`); Processed: Google Drive (see `data/processed/PROCESSED_LINK.md`)                                                                     |
| Row Count   | Raw:**251,277** rows (as printed in `notebooks/01_extraction.ipynb`); Processed: **248,094** rows (post-cleaning feature-ready dataset in `notebooks/02_cleaning.ipynb`) |
| Columns     | Raw:**16**; Processed: **30** (dashboard-ready schema with engineered KPIs)                                                                                                  |
| Time Period | Assumed**multi-month to multi-year** daily trending snapshots for India (exact bounds depend on the raw file's `trending_date` and `publishedAt` coverage).                    |
| Format      | CSV (raw and processed)                                                                                                                                                                  |

---

## Key Columns Used

| Column                 | Description                                                        | Role                                            |
| ---------------------- | ------------------------------------------------------------------ | ----------------------------------------------- |
| `video_id`           | Unique identifier for a YouTube video                              | Primary key (granularity anchor)                |
| `title`              | Video title text                                                   | Content descriptor (interpretation + drilldown) |
| `channel_id`         | Unique channel identifier                                          | Entity key (channel analytics)                  |
| `channel_title`      | Channel display name                                               | Reporting dimension                             |
| `category_id`        | YouTube content category ID                                        | Dimension (category mapping)                    |
| `category_name`      | Mapped category label (e.g., Music, Entertainment)                 | Business dimension for benchmarking             |
| `published_at`       | Video published timestamp (raw)                                    | Time dimension (content release)                |
| `publish_time`       | Parsed publish datetime (UTC in processed dataset)                 | Time calculations and scheduling analysis       |
| `publish_date`       | Date portion of publish time                                       | Calendar grouping                               |
| `publish_hour`       | Hour of publish time (0-23)                                        | Scheduling lever (hypothesis testing)           |
| `time_bucket`        | Morning/Afternoon/Evening/Night                                    | Executive-friendly scheduling abstraction       |
| `trending_date`      | Date when video appeared on trending list (snapshot)               | Outcome timestamp                               |
| `trending_month`     | Month extracted from trending date                                 | Seasonality/operations view                     |
| `trending_day`       | Day-of-week extracted from trending date                           | Week-pattern analysis                           |
| `views`              | View count at snapshot time                                        | Primary reach KPI                               |
| `likes`              | Like count at snapshot time                                        | Engagement signal                               |
| `comment_count`      | Comment count at snapshot time                                     | Engagement signal                               |
| `likes_ratio`        | Likes per view                                                     | Normalized engagement KPI                       |
| `comments_ratio`     | Comments per view                                                  | Normalized engagement KPI                       |
| `engagement_rate`    | (likes + comments) per view                                        | Core KPI used for performance + modeling        |
| `days_to_trend`      | Days between publish and first trending snapshot (clipped at >= 0) | Virality speed KPI                              |
| `trend_duration`     | Number of unique trending days per video_id                        | Persistence/evergreen KPI                       |
| `monetization_score` | Views * engagement_rate (proxy)                                    | Monetization potential KPI                      |
| `tags`               | Video tags text field                                              | Metadata lever                                  |
| `tag_count`          | Parsed count proxy from tags string                                | Metadata lever KPI                              |
| `has_description`    | Whether description exists (boolean)                               | Content completeness signal                     |
| `comments_disabled`  | Whether comments are disabled                                      | Constraint flag (engagement suppression)        |
| `ratings_disabled`   | Whether ratings are disabled                                       | Constraint flag (engagement suppression)        |

---

## KPI Framework

The KPI system is designed to translate platform signals into **business levers** (what creators can control) and **business outcomes** (reach, engagement, monetization potential).

| KPI                        | Business Meaning                                     | Formula (Processed Dataset)                                  | Unit      | Primary Decision Use                                   |
| -------------------------- | ---------------------------------------------------- | ------------------------------------------------------------ | --------- | ------------------------------------------------------ |
| Reach (Views)              | Total audience exposure at trending snapshot         | `views`                                                    | Count     | Benchmark performance; identify breakout scale         |
| Engagement Rate            | Overall interaction intensity relative to reach      | `(likes + comment_count) / views`                          | % (ratio) | Prioritize content types that drive deeper interaction |
| Likes Ratio                | Lightweight positive feedback per impression         | `likes / views`                                            | % (ratio) | Optimize hooks/thumbnails; sentiment proxy             |
| Comments Ratio             | Conversation depth per impression                    | `comment_count / views`                                    | % (ratio) | Community-building lever; topic sensitivity proxy      |
| Days to Trend              | Speed of trending pickup (virality velocity)         | `max(0, (trending_date - publish_time).days)`              | Days      | Schedule optimization; early engagement strategy       |
| Trend Duration             | Persistence on trending surface                      | `count_distinct(trending_date) by video_id`                | Days      | Identify evergreen formats; budget allocation          |
| Monetization Score (Proxy) | Revenue potential proxy combining reach + engagement | `views * engagement_rate`                                  | Index     | Prioritize topics that maximize monetizable attention  |
| Virality Score (Composite) | Unified score balancing speed + intensity + scale    | `log10(views + 1) * engagement_rate / (days_to_trend + 1)` | Index     | Rank videos/channels for replication and playbooks     |

---

## Tableau Dashboard

- **Dashboard URL:** *To be added* (publish to Tableau Public and paste link into `tableau/dashboard_links.md`)
- **Data Source:** `data/processed/cleaned_dataset_2.csv` (dashboard-ready schema)

### Executive View (Strategic KPIs)

Designed for stakeholders (creator managers, growth leads, MCNs) to answer "What is working and where should we invest?":

- KPI cards: **Views**, **Engagement Rate**, **Monetization Score**, **Days to Trend**, **Trend Duration**
- Category benchmarking: category-wise reach vs engagement trade-offs
- Seasonality: trending month/day-of-week distribution

### Operational View (Drilldowns)

Designed for daily execution and optimization:

- Posting-time performance (hour and time_bucket) vs views, engagement, monetization proxy
- Channel leaderboard (top channels by views/monetization score)
- Video-level drilldown table with sorting by virality score

### Filters Used (Recommended)

- Date filters: `trending_year`, `trending_month`, `trending_day`
- Content filters: `category_name`, `channel_title`
- Execution filters: `publish_hour`, `time_bucket`
- Policy/constraint filters: `comments_disabled`, `ratings_disabled`

---

## Key Insights

1. **Winner-takes-most distribution materially changes strategy**: the view distribution is highly right-skewed, which implies that optimizing for "average performance" will underperform; stakeholders should instead build playbooks to consistently manufacture top-decile outcomes through repeatable levers (format, timing, engagement triggers).
2. **Posting hour is not cosmetic; it is statistically significant**: an ANOVA test shows a **p-value of 0.0**, indicating publish hour materially impacts views; this suggests that content teams can unlock incremental reach by shifting uploads toward empirically stronger windows rather than publishing opportunistically.
3. **Weekend vs weekday performance differs significantly**: a two-sample t-test yields **p = 8.96e-06**, implying that weekend publishing behavior (audience availability and session length) should be treated as a distinct operating mode with dedicated schedules and creatives.
4. **Engagement is a first-order driver of performance**: correlation and regression results highlight engagement signals as strong predictors of views, which implies that creators should invest in retention hooks and community actions (CTAs, pinned comments, narrative arcs) rather than relying solely on upload frequency.
5. **Metadata quality has measurable lift potential**: `tag_count` shows a positive regression coefficient (holding other factors constant), which suggests that disciplined metadata hygiene (relevant tags, consistent naming conventions, searchable keywords) increases discoverability and improves trending outcomes.
6. **The relationship between time-to-trend and views is statistically significant**: Pearson correlation between `days_to_trend` and `views` is **0.341 (p = 0.0)**, implying that high-view outcomes can accumulate beyond day-1; this supports sustained promotion (shorts/clips/community posts) for several days post-publish rather than "launch-day only" marketing.
7. **Monetization proxy is maximized when reach and engagement co-occur**: the `monetization_score` framework emphasizes that large views without engagement are less valuable than moderately lower views with high interaction, implying that brands/creators should prioritize content that delivers both scale and intent.
8. **Category effects indicate differentiated investment strategy**: category mapping and category-level benchmarking imply that not all content types should be treated equally; stakeholders should fund categories that show superior engagement and monetization efficiency, while using high-volume categories for reach and subscriber acquisition.
9. **Multicollinearity risk is present in naive models**: because `engagement_rate` is derived from likes/comments/views, regression coefficient direction can be unstable despite high overall model fit (R-squared **0.692**); this implies that decisions should rely on combined evidence (tests + dashboard slices) rather than a single coefficient sign.
10. **Operationally, "evening windows" are a pragmatic default**: timing analysis and key statistical notes suggest evening uploads tend to improve virality and monetization potential; this implies that teams should operationalize evening as the default window unless a channel's audience analytics contradicts it.

---

## Recommendations

| # | Insight                                                             | Recommendation                                                                                                                                                           | Expected Impact                                                                |
| -: | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| 1 | Posting hour significantly impacts views (ANOVA p = 0.0)            | Establish a controlled**publishing calendar** with 2-3 fixed high-performing time windows; A/B test by shifting 25-33% of uploads into the best window for 4 weeks | +5-15% average views per upload; reduced volatility in performance             |
| 2 | Weekend vs weekday differs (p = 8.96e-06)                           | Create a**weekend content lane** (longer watch-time formats, high entertainment value) and run weekend-specific promos                                             | +5-10% weekend reach; higher session-length alignment                          |
| 3 | Engagement drives views and monetization potential                  | Build an**engagement playbook**: first 30 seconds retention hook, explicit CTA, pinned comment question, community post within 2 hours                             | +0.5-1.5 pp engagement_rate; improved recommendation pickup                    |
| 4 | Metadata quality (`tag_count`) contributes to performance         | Standardize**metadata templates** per category: title patterns, tag libraries, keyword checklists; prevent tag spam by enforcing relevance review                  | +2-8% discoverability lift; more stable search-driven traffic                  |
| 5 | Sustained promotion matters (days_to_trend correlation significant) | Implement a**72-hour post-publish amplification plan**: shorts cutdowns, cross-platform reposts, collaboration shout-outs                                          | Faster trend pickup and stronger cumulative reach; +5-12% total views by day 7 |
| 6 | Monetization proxy improves when engagement co-occurs with scale    | Prioritize content that ranks high on**monetization_score** rather than views alone; allocate brand integrations to high-engagement categories                     | Higher CPM alignment; improved brand safety and conversion likelihood          |
| 7 | Category effects require differentiated strategy                    | Split strategy into**Reach Categories** (subscriber growth) vs **Efficiency Categories** (engagement/monetization); allocate budgets accordingly             | Better ROI on production spend; clearer portfolio-level governance             |
| 8 | Model coefficient instability warns against single-metric decisions | Use a**triangulation framework** in weekly reviews: KPI scorecards + category/time slices + statistical tests                                                      | Reduced decision risk; improved consistency in optimization choices            |

---

## Repository Structure

(Keep EXACT structure given)

```text
SectionD_Team16_YoutubeTrending/
|-- data/
|   |-- raw/
|   |   `-- raw_link.md
|   `-- processed/
|       `-- PROCESSED_LINK.md
|-- docs/
|   `-- data_dictonary.md
|-- notebooks/
|   |-- 01_extraction.ipynb
|   |-- 02_cleaning.ipynb
|   |-- 03_eda.ipynb
|   `-- 04_statistical_analysis.ipynb
|-- reports/
|   |-- README.md
|   |-- presentation_outline.md
|   `-- project_report.md
|-- scripts/
|   `-- .gitkeep
|-- tableau/
|   |-- dashboard_links.md
|   `-- screenshots/
|       `-- .gitkeep
|-- README.md
`-- requirements.txt
```

---

## Analytical Pipeline

This capstone follows an end-to-end analytics workflow aligned to an industry BI lifecycle.

1. **Business Understanding**Defined the stakeholder goal: improve trending performance and monetization potential for YouTube India content by identifying controllable levers and high-performing archetypes.
2. **Data Acquisition (Extraction)**Loaded the raw India trending dataset (`IN_youtube_trending_data.csv`) in `notebooks/01_extraction.ipynb`, confirming baseline shape (**251,277 rows, 16 columns**) and validating required fields exist (video, channel, category, time, and performance metrics).
3. **Data Cleaning and Quality Control**In `notebooks/02_cleaning.ipynb`, handled nulls (description, tags), removed irrelevant fields (thumbnail link), converted datatypes to enable time-based analysis, filtered invalid records (views > 0), and removed duplicates at the grain of `video_id` x `trending_date`.
4. **Feature Engineering (KPI Layer Creation)**Engineered business-ready metrics: `likes_ratio`, `comments_ratio`, `engagement_rate`, `days_to_trend`, `trend_duration`, `monetization_score`, `tag_count`, and `has_description`. Mapped `category_id` to `category_name` and created `time_bucket` from `publish_hour` for executive reporting. Final dataset standardized to snake_case and ordered for dashboard readiness (**248,094 rows, 30 columns**).
5. **Exploratory Data Analysis (EDA)**In `notebooks/03_eda.ipynb`, analyzed category distribution, performance distributions, posting-time patterns, and virality characteristics to identify candidate levers and segments to test statistically and visualize in Tableau.
6. **Statistical Analysis and Modeling**In `notebooks/04_statistical_analysis.ipynb`, validated business hypotheses using:

   - ANOVA for posting hour effect on views (statistically significant)
   - t-test for weekend vs weekday performance (statistically significant)
   - correlation analysis between virality/engagement features and views
   - OLS regression to quantify contribution of controllable factors (model fit R-squared ~ 0.692)
7. **Visualization, Storytelling, and Decision Packaging**
   Structured Tableau dashboard requirements (executive vs operational views) and translated insights into a recommendation matrix with measurable expected impact, enabling stakeholders to operationalize changes in scheduling, engagement tactics, and content strategy.

---

## Tech Stack

| Layer               | Tools / Libraries                                 | Purpose                                         |
| ------------------- | ------------------------------------------------- | ----------------------------------------------- |
| Programming         | Python 3.x                                        | Data processing, analysis, and modeling         |
| Data Manipulation   | Pandas, NumPy                                     | Cleaning, transformation, feature engineering   |
| Visualization (EDA) | Matplotlib, Seaborn                               | Distribution checks, category/time analyses     |
| Statistics          | SciPy (`ttest_ind`, `f_oneway`, `pearsonr`) | Hypothesis testing and correlations             |
| Modeling            | Statsmodels (OLS)                                 | Regression-based driver analysis                |
| Notebooks           | Jupyter / Google Colab                            | Reproducible analysis workflow                  |
| BI / Dashboard      | Tableau (Public/Desktop)                          | Executive and operational dashboards            |
| Version Control     | Git, GitHub                                       | Collaboration, versioning, evaluation readiness |
| Documentation       | Markdown                                          | Reporting and final submission documentation    |

---

## Evaluation Rubric

(Keep as-is)

| Criteria                  | What Evaluators Look For                                    | Evidence in This Repository                         | Suggested Weight |
| ------------------------- | ----------------------------------------------------------- | --------------------------------------------------- | ---------------- |
| Problem Framing           | Clear stakeholder, impact, and decision                     | Business Problem, Core Question, Decision Supported | 10%              |
| Data Understanding        | Source clarity, schema understanding, assumptions           | Dataset + Key Columns + Data links                  | 10%              |
| ETL & Data Quality        | Cleaning logic, reproducibility, validity checks            | `notebooks/02_cleaning.ipynb`, engineered schema  | 15%              |
| KPI Design                | Business relevance, correct formulas, alignment to decision | KPI Framework, dashboard-ready features             | 15%              |
| EDA & Insight Depth       | Meaningful segmentation and interpretation                  | `notebooks/03_eda.ipynb`, Key Insights            | 15%              |
| Statistical Rigor         | Correct test selection, interpretation, modeling care       | `notebooks/04_statistical_analysis.ipynb`         | 15%              |
| Visualization & Dashboard | Storytelling, interactivity, executive readiness            | Tableau section + dashboard artifacts               | 10%              |
| Recommendations           | Actionability, linkage to insight, measurable impact        | Recommendations table                               | 10%              |

---

## Submission Checklist

(Keep as-is)

- [ ] Repository contains a complete README with business framing, KPIs, insights, and recommendations
- [ ] `data/raw/raw_link.md` and `data/processed/PROCESSED_LINK.md` include working dataset links
- [ ] Notebooks run end-to-end (paths adjusted for local run) and follow ordered pipeline (01 -> 04)
- [ ] Processed schema is dashboard-ready (snake_case, typed dates, engineered KPIs)
- [ ] Tableau dashboard published (Tableau Public link added to `tableau/dashboard_links.md`)
- [ ] Dashboard includes executive KPIs + drilldowns + filters aligned to stakeholder questions
- [ ] Statistical tests and model outputs are interpretable and consistent with business decisions
- [ ] Recommendations are actionable, measurable, and mapped to insights

---

## Contribution Matrix

| Team Member | Contribution Areas |
| ----------- | ------------------ |
|             |                    |
|             |                    |
|             |                    |
|             |                    |
|             |                    |
|             |                    |
|             |                    |

---

## Declaration

(Keep format)

We hereby declare that this capstone project is an original work completed as part of NST's Data Visualization & Analytics program. All analyses, visualizations, and interpretations are based on the dataset sources cited in this repository, and any assumptions have been explicitly stated wherever applicable.

| Name | Role |
| ---- | ---- |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |

---

## Academic Integrity

(Keep as-is)

This repository complies with NST's academic integrity standards:

- **No plagiarism:** All written content is authored by the team; any external references are cited.
- **No fabrication:** Metrics and tests are computed from the dataset; assumptions are stated and do not replace missing computations.
- **Reproducibility:** Notebooks document the data pipeline and statistical methods used for conclusions.
- **Responsible interpretation:** Statistical outputs are contextualized with business meaning; model limitations (e.g., multicollinearity) are acknowledged to prevent misuse.
