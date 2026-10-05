# Data Job Market Analysis

## Introduction

Breaking into the data industry is not just about having the right skills — it is about knowing **where the opportunities are, what they pay, and which skills actually matter**.

This project turns a large database of job postings into practical answers for people building a career in Data Analytics, Data Science, Data Engineering, and related fields. Instead of relying on assumptions or generic career advice, I use advanced SQL analysis to uncover patterns in salaries, job boards, remote opportunities, experience requirements, and in-demand technical skills.

The goal is simple: **help job seekers make smarter career decisions with data.**

The analysis identifies which platforms offer the most attractive remote salaries, where entry-level and junior candidates have the best chances of finding opportunities, and which technical skills are associated with higher-paying positions. These insights can help candidates decide **where to search, what to learn, and which skills are worth investing their time in.**

Ultimately, this project demonstrates how raw job-market data can be transformed into actionable insights — turning thousands of job postings into a clearer strategy for entering and growing in the data industry.


## Tools Used

* **SQL**
* **Python (Matplotlib, Pandas)**


## Analysis

The analysis is broken down into five core areas, executing specific SQL queries to answer targeted business questions about the job market.

### 1. Top Paying Platforms by Role

To determine which platforms host the highest-paying remote jobs, I used Common Table Expressions (CTEs) and Window Functions to rank platforms by average salary for each distinct data role.

**Reference:** `1_top_paying_platforms.sql`

```sql
WITH ranked_platforms AS (
    SELECT
        job_title_short,
        TRIM(REPLACE(job_via, 'via ', '')) AS platform,
        ROUND(AVG(salary_year_avg), 0) AS avg_salary,
        MIN(salary_year_avg) AS min_salary,
        MAX(salary_year_avg) AS max_salary,
        ROW_NUMBER() OVER (
            PARTITION BY job_title_short 
            ORDER BY AVG(salary_year_avg) DESC
        ) AS salary_rank
    FROM
        job_postings_fact
    WHERE
        salary_year_avg IS NOT NULL
        AND job_work_from_home = TRUE -- Filters exclusively for remote positions (or = 1 if stored as integer)
        AND job_title_short IN (
            'Data Analyst',
            'Data Scientist',
            'Business Analyst',
            'Data Engineer',
            'Machine Learning Engineer',
            'Cloud Engineer'
        )
    GROUP BY
        job_title_short,
        TRIM(REPLACE(job_via, 'via ', ''))
)
SELECT
    job_title_short,
    platform,
    avg_salary,
    min_salary,
    max_salary
FROM
    ranked_platforms
WHERE
    salary_rank <= 5
ORDER BY
    job_title_short,
    avg_salary DESC;
```

> **<img width="2400" height="1200" alt="image" src="https://github.com/user-attachments/assets/f81631cb-9143-42dc-9cc0-f3621e976705" />
**

### 2. Platforms Favoring Junior Roles

Understanding where entry-level candidates should apply is critical. I utilized `CASE WHEN` statements with wildcard pattern matching to isolate junior, intern, and entry-level roles, aggregating them by platform.

**Reference:** `2_platforms_by_junior_jobs.sql`

```sql
WITH categorized_salary_jobs AS (
    SELECT
        TRIM(REPLACE(job_via, 'via ', '')) AS platform,
        salary_year_avg,
        CASE
            WHEN job_title LIKE '%junior%'
              OR job_title LIKE '%entry level%'
              OR job_title LIKE '%entry-level%'
              OR job_title LIKE '%associate%'
              OR job_title LIKE '%intern%'
              OR job_title LIKE '%trainee%'
            THEN 1
            ELSE 0
        END AS is_junior_role
    FROM
        job_postings_fact
    WHERE
        job_work_from_home = TRUE 
        AND job_via IS NOT NULL 
        AND salary_year_avg IS NOT NULL
)
SELECT
    platform,
    SUM(is_junior_role) AS junior_salary_postings,
    ROUND(AVG(CASE WHEN is_junior_role = 1 THEN salary_year_avg END), 0) AS junior_avg_salary
FROM
    categorized_salary_jobs
GROUP BY
    platform
HAVING
    SUM(is_junior_role) > 0
ORDER BY
    junior_salary_postings DESC;
```

> **<img width="2400" height="1200" alt="image" src="https://github.com/user-attachments/assets/1af7610a-ed88-4cc4-8d6d-5bcb2cf773f7" />**

### 3. Top Platforms by Job Quantity (Pivoted by Role)

To assess the sheer volume of opportunities, I built a query using conditional aggregation to create a pivot-table effect, displaying total job counts across different platforms separated by specific roles.

**Reference:** `3_top_platforms_by_job_quantity.sql`

```sql
SELECT
    TRIM(REPLACE(job_via, 'via ', '')) AS platform,
    COUNT(*) AS total_postings,
    COUNT(CASE WHEN job_title_short = 'Data Analyst' THEN 1 END) AS data_analyst_jobs,
    COUNT(CASE WHEN job_title_short = 'Data Scientist' THEN 1 END) AS data_scientist_jobs,
    COUNT(CASE WHEN job_title_short = 'Data Engineer' THEN 1 END) AS data_engineer_jobs,
    COUNT(CASE WHEN job_title_short = 'Business Analyst' THEN 1 END) AS business_analyst_jobs,
    COUNT(CASE WHEN job_title_short = 'Machine Learning Engineer' THEN 1 END) AS ml_engineer_jobs,
    COUNT(CASE WHEN job_title_short = 'Cloud Engineer' THEN 1 END) AS cloud_engineer_jobs
    
FROM
    job_postings_fact
WHERE
    job_title_short IN (
        'Data Analyst',
        'Data Scientist',
        'Business Analyst',
        'Data Engineer',
        'Machine Learning Engineer',
        'Cloud Engineer'
    )
    AND job_via IS NOT NULL
    AND job_work_from_home = TRUE
GROUP BY
    platform
ORDER BY
    total_postings DESC
LIMIT 20;
```

> **<img width="2400" height="1200" alt="image" src="https://github.com/user-attachments/assets/d3bc50ff-3795-4d95-afa7-6d7cc00d6616" />**

### 4. Job Volume vs. Salary by Platform

Volume does not always equate to quality. This query joins two separate CTEs to compare the total number of job postings on a platform against the average salary offered, providing a holistic view of platform value.

**Reference:** `4_top_job_count_platforms.sql`

```sql
WITH platform_volume AS (
    SELECT
        TRIM(REPLACE(job_via, 'via ', '')) AS platform,
        COUNT(job_id) AS posting_count
    FROM
        job_postings_fact
  
    GROUP BY
        platform
),
platform_salary AS (
    SELECT
        TRIM(REPLACE(job_via, 'via ', '')) AS platform,
        ROUND(AVG(salary_year_avg), 0) AS avg_platform_salary
    FROM
        job_postings_fact
    WHERE
        salary_year_avg IS NOT NULL
  	    AND job_work_from_home = TRUE
    GROUP BY
        platform
)
SELECT
    v.platform,
    v.posting_count,
    s.avg_platform_salary
FROM
    platform_volume v
INNER JOIN 
    platform_salary s ON v.platform = s.platform
ORDER BY
    v.posting_count DESC
LIMIT 30;
```

> **
<img width="2400" height="1500" alt="image" src="https://github.com/user-attachments/assets/61ef2d37-3a8e-427b-aba6-479ddff04ba8" />

**

### 5. Optimal Skills for Junior Professionals

To guide learning and development, I joined the main fact table with skill dimension tables to calculate which technical skills are most frequently requested in junior roles, and which of those skills yield the highest starting salaries.

**Reference:** `5_the_best_skills_for_juniors.sql`

```sql
WITH junior_jobs_with_salary AS (
    -- Pattern: Filter and isolate entry-level roles with non-null salary data
    SELECT
        job_id,
        salary_year_avg
    FROM
        job_postings_fact
    WHERE
        salary_year_avg IS NOT NULL
        AND (
            job_title LIKE '%junior%'
            OR job_title LIKE '%entry level%'
            OR job_title LIKE '%entry-level%'
            OR job_title LIKE '%associate%'
            OR job_title LIKE '%intern%'
            OR job_title LIKE '%trainee%'
        )
)
SELECT
    sd.skills,
    COUNT(j.job_id) AS postings_count,
    ROUND(AVG(j.salary_year_avg), 0) AS avg_salary
FROM
    junior_jobs_with_salary j
INNER JOIN
    skills_job_dim sjd ON j.job_id = sjd.job_id
INNER JOIN
    skills_dim sd ON sjd.skill_id = sd.skill_id
GROUP BY
    sd.skills
HAVING
	postings_count > 50
ORDER BY
    avg_salary DESC
LIMIT 40;
```

> **<img width="2400" height="1500" alt="image" src="https://github.com/user-attachments/assets/71d78868-9f76-4c8d-b4d8-f00473d7f0b4" />
**

## What I Learned

Executing this analysis significantly enhanced my SQL proficiency, specifically in the following areas:

* **Advanced Aggregation:** Utilized conditional aggregations (`COUNT(CASE WHEN...)`) to pivot data directly within SQL, reducing the need for heavy post-processing in BI tools.
* **Window Functions:** Applied `ROW_NUMBER() OVER (PARTITION BY...)` to create targeted rankings, such as isolating the top 5 paying platforms per job title.
* **Complex Joins:** Successfully navigated normalized database schemas by executing multi-table `INNER JOIN` operations between fact tables and dimension tables to connect job postings with specific skill requirements.
* **String Manipulation & Cleansing:** Relied on `TRIM()`, `REPLACE()`, and wildcard `LIKE` operators to clean unstructured text data (like platform names and job titles) for accurate grouping.

## Conclusions

The data reveals a critical strategic split in both platform selection and skill acquisition for data professionals. While LinkedIn dominates the overall market in total job volume, early-career candidates should focus heavily on ZipRecruiter and Indeed, which host the vast majority of entry-level roles. Conversely, to maximize earning potential, candidates must look beyond these generalist boards toward niche hubs like Y Combinator and Web3 Jobs, where specialized roles command immense salary premiums. Most importantly, the skills required to get a junior job are fundamentally different from the skills that maximize a junior salary. While Python and SQL are undeniable foundational requirements for passing initial screenings, mastering high-performance big data and cloud technologies—specifically Scala, Kafka, and AWS—is the true catalyst for commanding top-tier compensation early in a data career.

## How to Run This Project
1. Clone this repository
2. .Download the required database files from this Google Drive link.
3. Ensure you have a SQL client installed (e.g., pgAdmin, DBeaver, or a command-line interface).
4. Connect your SQL client to the downloaded database.
5. Execute the .sql files in the /queries/ directory in sequential order to replicate the analysis.
