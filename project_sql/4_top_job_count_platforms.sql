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