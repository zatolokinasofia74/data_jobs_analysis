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