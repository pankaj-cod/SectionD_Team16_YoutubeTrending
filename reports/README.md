# NST DVA Capstone 2 - Project Repository

Newton School of Technology | Data Visualization & Analytics

A 2-week industry simulation capstone using Python, GitHub, and Tableau to convert raw data into actionable business intelligence.

---

---

## Project Overview

| Field           | Details                                                  |
| --------------- | ---------------------------------------------------------|
| Project Title   | YouTube Trending Analytics: Decoding Virality on Youtube |
| Sector          | Digital Media / Content Platforms                        |
| Team ID         | Section D - Team 16                                      |
| Section         | D                                                        |
| Faculty Mentor  | NST DVA Faculty Panel                                    |
| Institute       | Newton School of Technology                              |
| Submission Date | April 29, 2026                                           |

---

## Team Members

| Name     | Role |
| -------- | ---- |
| Vikash   |      |
| Yashi    |      |
| Pankaj   |      |
| Abhishek |      |
| Sarthak  |      |
| Kanishk  |      |

## Business Problem

YouTube’s trending ecosystem is highly competitive, where early performance determines whether content achieves massive reach or fades quickly. For creators, media companies, and platform teams, identifying what drives virality is essential for optimizing publishing strategies and maximizing engagement. The challenge lies in understanding timing, content type, and audience behavior at scale. This project transforms raw trending data into actionable insights to guide content strategy, improve engagement, and enhance visibility—especially within the Indian market.

---

## Core Business Question

What key factors (publishing time, category, and early engagement) drive virality and increase the probability of a video trending in India?

---

## Decision Supported

Enables creators and strategists to optimize upload timing, focus on high-performing content categories, and improve early engagement strategies to maximize trending success.

---

---

## Dataset

| Attribute           | Details                           |
| ------------------- | --------------------------------- |
| Source Name         | Kaggle (YouTube Trending Dataset) |
| Direct Access Link  | Refer `data/raw/raw_link.md`    |
| Row Count           | ~250,000+                         |
| Column Count        | 16+ raw / 30+ processed           |
| Time Period Covered | Multi-year trending snapshots     |
| Format              | CSV                               |

---

## Key Columns Used

| Column Name       | Description                      | Role in Analysis         |
| ----------------- | -------------------------------- | ------------------------ |
| `video_id`      | Unique identifier for each video | Tracking distinct videos |
| `title`         | Video title                      | Content context          |
| `channel_title` | Channel name                     | Channel performance      |
| `category_id`   | Content category                 | Category analysis        |
| `views`         | Number of views                  | Reach metric             |
| `likes`         | Likes count                      | Positive engagement      |
| `dislikes`      | Dislikes count                   | Sentiment analysis       |
| `comment_count` | Comments count                   | Engagement depth         |
| `publish_time`  | Upload time                      | Timing analysis          |
| `trending_date` | Trending date                    | Outcome metric           |

---

## KPI Framework

| KPI                 | Definition                             | Formula / Computation           |
| ------------------- | -------------------------------------- | ------------------------------- |
| Engagement Rate     | Measures interaction relative to views | (likes + comments) / views      |
| Virality Score      | Measures speed of growth               | views / days trending           |
| Avg Views per Video | Average reach per video                | total views / unique videos     |
| Time to Trend       | Time taken to trend                    | trending_date - publish_time    |
| Channel Dominance % | Share of top channels                  | top channel views / total views |
| Like-Dislike Ratio  | Audience sentiment                     | likes / dislikes                |

## Tableau Dashboard

| Item             | Details                                                |
| ---------------- | ------------------------------------------------------ |
| Dashboard URL    | Added in `tableau/dashboard_links.md`                |
| Executive View   | Overview of KPIs, India insights, category performance |
| Operational View | Timing, virality, and channel-level deep dive          |
| Main Filters     | Date, category, channel, publish time                  |

---

## Key Insights

1.**A small percentage of channels drive the majority of total views** (Pareto effect).

2.**Evening uploads (6–9 PM)** perform best in India.

3.**Faster time-to-trend** strongly correlates with higher virality.

4.**High engagement categories** may also have high dislike ratios (controversial content).

5.**Weekend uploads** tend to remain trending longer.

6.**Entertainment and Music** dominate in views, while niche categories show higher engagement rates.

7.**Early like ratio** predicts long-term performance.

8.**High comment activity** increases content longevity.

9.**Indian audience strongly prefers** entertainment-focused content.

10.**First 72 hours** are critical for viral success.

---

---

## Recommendations

| # | Insight                        | Recommendation                     | Expected Impact                |
| - | ------------------------------ | ---------------------------------- | ------------------------------ |
| 1 | Evening uploads perform best   | Schedule uploads between 6–9 PM   | Increased engagement and views |
| 2 | Early momentum drives virality | Focus promotions in first 24 hours | Faster trending                |
| 3 | Channel dominance exists       | Learn from top creators            | Better content performance     |
| 4 | Controversial content risk     | Monitor sentiment closely          | Protect brand reputation       |

## Repository Structure

```text
SectionD_Team16_YoutubeTrending/
├── data/
│   ├── raw/                 <- Original datasets
│   └── processed/           <- Cleaned & transformed data
├── notebooks/               <- Analysis & modeling notebooks
├── src/                     <- Production-grade ETL pipeline
├── reports/
│   ├── assets/              <- Dashboard recordings & screenshots
│   └── YouTube_Trending_Intelligence.pdf <- Final findings
├── docs/                    <- Data dictionary & dashboard links
├── DVA-focused-Portfolio/   <- Career-oriented assets
├── DVA-focused-Resume/      <- Professional resume
├── README.md
└── requirements.txt
```

---

## Analytical Pipeline

1. Define problem and objectives
2. Extract dataset
3. Clean and transform data
4. Perform EDA and statistical analysis
5. Build Tableau dashboards
6. Generate insights and recommendations
7. Deliver final report

---

---

## Tech Stack

| Tool             | Status    | Purpose         |
| ---------------- | --------- | --------------- |
| Python           | Mandatory | Data analysis   |
| Jupyter Notebook | Mandatory | Workflow        |
| Tableau Public   | Mandatory | Visualization   |
| GitHub           | Mandatory | Version control |

## Evaluation Rubric

| Area            | Marks | Focus         |
| --------------- | ----- | ------------- |
| Problem Framing | 10    | Clarity       |
| Data Quality    | 15    | Cleaning      |
| Analysis        | 25    | Insights      |
| Dashboard       | 20    | Visualization |
| Recommendations | 20    | Actionability |
| Storytelling    | 10    | Presentation  |

## Submission Checklist

- [X] Repository complete
- [X] Notebooks included
- [X] Data structured
- [X] Dashboard published
- [X] Insights & recommendations added

---

## Contribution Matrix

| Team Member | Contribution Areas                          |
| ----------- | --------------------------------------------|
| Vikash      | ETL, EDA & Analysis                         |
| Yashi       | Feature Engineering, Analysis & Dashboarding|
| Pankaj      | Dataset Sourcing & Dashboarding             |
| Abhishek    | Statistical Analysis & Data Cleaning        |
| Sarthak     | Presentation & Analysis                     |
| Kanishk     | Project Report & Analysis                   |

---

## Academic Integrity

All work is original and aligned with NST guidelines. Contributions are verifiable via GitHub history.

*Newton School of Technology - Data Visualization & Analytics | Capstone 2*
