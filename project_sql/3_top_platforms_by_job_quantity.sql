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