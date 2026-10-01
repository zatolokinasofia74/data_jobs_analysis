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