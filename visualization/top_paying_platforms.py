import os
import matplotlib.pyplot as plt
import pandas as pd

#create folder for output charts
os.makedirs('images', exist_ok=True)#make sure images folder exists
# 1. Top 5 paying platforms for Data Analysts
df_pay = pd.read_csv('results_of_the_queries/top_paying_platforms.csv', sep='\t')#load top paying platforms data
da_df = df_pay[df_pay['job_title_short'] == 'Data Analyst'].sort_values(by='avg_salary', ascending=True)#filter data analysts and sort

plt.figure(figsize=(8, 4))#set chart dimensions
bars = plt.barh(da_df['platform'], da_df['avg_salary'] / 1000, color='#3b82f6', height=0.6)#draw horizontal bars in $k

for bar in bars:
    w = bar.get_width()#get bar length
    plt.text(w + 3, bar.get_y() + bar.get_height() / 2, f"${int(w)}k", va='center', fontsize=10, weight='bold')#write salary on bar

plt.xlim(0, max(da_df['avg_salary'] / 1000) * 1.15)#add padding on right
plt.title('Top 5 Highest-Paying Platforms for Data Analysts', fontsize=12, weight='bold')#chart title
plt.xlabel('Average Salary ($k USD)', fontsize=10)#x axis label
plt.ylabel('Platform', fontsize=10)#y axis label
plt.tight_layout()#adjust borders
plt.savefig('images/1_top_paying_analyst.png', dpi=300)#save image
plt.close()#close current plot
# 2. Top 5 platforms by junior job postings
df_juniors = pd.read_csv('results_of_the_queries/platforms_for_juniors.csv', sep='\t')#load junior jobs data
top5_junior = df_juniors.sort_values(by='junior_salary_postings', ascending=True).tail(5)#get top 5 junior platforms

plt.figure(figsize=(8, 4))#set chart dimensions
bars = plt.barh(top5_junior['platform'], top5_junior['junior_salary_postings'], color='#10b981', height=0.6)#draw green bars

for bar in bars:
    w = bar.get_width()#get posting count
    plt.text(w + 0.8, bar.get_y() + bar.get_height() / 2, f"{int(w)} jobs", va='center', fontsize=10, weight='bold')#write job count

plt.xlim(0, max(top5_junior['junior_salary_postings']) * 1.15)#add right margin
plt.title('Top 5 Platforms by Junior Job Postings', fontsize=12, weight='bold')#chart title
plt.xlabel('Number of Junior Postings', fontsize=10)#x axis label
plt.ylabel('Platform', fontsize=10)#y axis label
plt.tight_layout()#adjust borders
plt.savefig('images/2_junior_jobs_volume.png', dpi=300)#save image
plt.close()#close current plot
# 3. Top 5 platforms by total job postings
df_quantity = pd.read_csv('results_of_the_queries/platforms_by_quantity.csv', sep='\t')#load platform quantities data
top5_volume = df_quantity.head(5).sort_values(by='total_postings', ascending=True)#get top 5 largest platforms

plt.figure(figsize=(8, 4))#set chart dimensions
bars = plt.barh(top5_volume['platform'], top5_volume['total_postings'], color='#6366f1', height=0.6)#draw purple bars

for bar in bars:
    w = bar.get_width()#get total count
    plt.text(w + 25, bar.get_y() + bar.get_height() / 2, f"{int(w)}", va='center', fontsize=10, weight='bold')#write total on bar

plt.xlim(0, max(top5_volume['total_postings']) * 1.15)#add right margin
plt.title('Top 5 Job Platforms by Total Postings', fontsize=12, weight='bold')#chart title
plt.xlabel('Total Postings Count', fontsize=10)#x axis label
plt.ylabel('Platform', fontsize=10)#y axis label
plt.tight_layout()#adjust borders
plt.savefig('images/3_top_platforms_total.png', dpi=300)#save image
plt.close()#close current plot
# 4. Top 10 most in-demand skills for juniors
df_skills = pd.read_csv('results_of_the_queries/the_best_skills_for_juniors.csv', sep='\t')#load junior skills data
top10_skills = df_skills.sort_values(by='postings_count', ascending=True).tail(10)#get top 10 skills by count

plt.figure(figsize=(8, 5))#set chart dimensions
bars = plt.barh(top10_skills['skills'], top10_skills['postings_count'], color='#f59e0b', height=0.6)#draw orange bars

for bar in bars:
    w = bar.get_width()#get skill frequency
    plt.text(w + 5, bar.get_y() + bar.get_height() / 2, f"{int(w)}", va='center', fontsize=10, weight='bold')#label bar value

plt.xlim(0, max(top10_skills['postings_count']) * 1.12)#add right margin
plt.title('Top 10 Most In-Demand Skills for Juniors', fontsize=12, weight='bold')#chart title
plt.xlabel('Number of Postings', fontsize=10)#x axis label
plt.ylabel('Skill', fontsize=10)#y axis label
plt.tight_layout()#adjust borders
plt.savefig('images/4_top_junior_skills_demand.png', dpi=300)#save image
plt.close()#close current plot
# 5.top 10 highest-paying skills for juniors
top10_pay = df_skills.sort_values(by='avg_salary', ascending=True).tail(10)#get top 10 skills by salary

plt.figure(figsize=(8, 5))#set chart dimensions
bars = plt.barh(top10_pay['skills'], top10_pay['avg_salary'] / 1000, color='#ec4899', height=0.6)#draw pink bars

for bar in bars:
    w = bar.get_width()#get salary value
    plt.text(w + 1.5, bar.get_y() + bar.get_height() / 2, f"${int(w)}k", va='center', fontsize=10, weight='bold')#write salary on bar

plt.xlim(0, max(top10_pay['avg_salary'] / 1000) * 1.15)#add right margin
plt.title('Top 10 Highest-Paying Skills for Juniors', fontsize=12, weight='bold')#chart title
plt.xlabel('Average Salary ($k USD)', fontsize=10)#x axis label
plt.ylabel('Skill', fontsize=10)#y axis label
plt.tight_layout()#adjust borders
plt.savefig('images/5_top_junior_skills_salary.png', dpi=300)#save image
plt.close()#close current plot

print('All 5 charts successfully generated and saved to ./images/')#print completion message