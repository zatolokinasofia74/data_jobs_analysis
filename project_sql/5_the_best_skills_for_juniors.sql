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