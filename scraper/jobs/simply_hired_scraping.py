from scraper.constants.const import *
from scraper.utils.helpers import ScraperNaming, k_conversion, sleeper
from utils.helpers import log_scraper_running_time, saveLogs
from typing import List
from scraper.jobs.base_scraper import BaseScraper

JOB_SOURCE = "simplyhired"


class SimplyHiredScraper(BaseScraper):

    def __init__(self, job_type, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.job_type: str = job_type
        self.scrape_job_urls: List[str] = []

    def run_simplyhired(self):
        try:
            self.driver.get(self.url)
            flag = True
            page_no = 2
            while flag and page_no <= 40:
                flag = self.find_urls(page_no)
                page_no += 1
            if len(self.scrape_job_urls) > 0:
                self.get_previous_jobs(
                    job_source=JOB_SOURCE, urls=self.scrape_job_urls)
                self.find_jobs()
            if self.scraped_jobs:
                self.export_to_excel(
                    scraper_name=ScraperNaming.SIMPLY_HIRED, job_source="Simply Hired")
        except Exception as e:
            saveLogs(e)

    def find_urls(self, next_page_no):
        jobs = self.get_element(locator="css-1igwmid", alls=True)
        for job in jobs:
            job_url = self.get_element(
                selector="css", locator="h2 > .css-1djbb1k", parent=job).get_attribute("href")
            self.scrape_job_urls.append(job_url)
        try:
            next_page = self.get_element(locator="css-1vdegr", alls=True)
            next_page_clicked = False
            for i in next_page:
                if i.text == f'{next_page_no}':
                    i.click()
                    sleeper()
                    next_page_clicked = True
                    break
            return next_page_clicked
        except Exception as e:
            saveLogs(e)
            self.driver.quit()
            return False

    def populate_salary(self, context):
        salary = context[3].text
        if len(context) == 5:
            estimated_salary = salary.split(' a')[0]
            if "d: " in estimated_salary:
                estimated_salary = estimated_salary.split(": ")[1]
            if "to " in estimated_salary:
                estimated_salary = estimated_salary.split("to ")[1]
            self.job["estimated_salary"] = k_conversion(
                estimated_salary)
            try:
                self.job["salary_min"] = k_conversion(
                    estimated_salary.split(' - ')[0])
            except:
                self.job["salary_min"] = "N/A"
            try:
                self.job["salary_max"] = k_conversion(
                    estimated_salary.split(' - ')[1])
            except:
                self.job["salary_max"] = "N/A"
            if 'year' in salary:
                salary_format = 'yearly'
            elif 'month' in salary:
                salary_format = 'monthly'
            elif 'day' in salary:
                salary_format = 'daily'
            elif 'hour' in salary:
                salary_format = 'hourly'
            else:
                salary_format = 'N/A'
            self.job['salary_format'] = salary_format

            job_posted_date = context[4].text
        else:
            self.job["estimated_salary"] = 'N/A'
            self.job["salary_min"] = 'N/A'
            self.job["salary_max"] = 'N/A'
            self.job['salary_format'] = 'N/A'
            job_posted_date = context[3].text
        self.job['job_posted_date'] = job_posted_date

    def find_jobs(self):
        for job in self.scrape_job_urls:
            if self.previous_links.get(job):
                continue
            try:
                self.driver.get(job)
                self.job['job_title'] = self.get_element(
                    locator='css-yvgnf2').text
                context = self.get_element(locator='css-xyzzkl', alls=True)
                try:
                    company_name = context[0].text.split('-')[0]
                except:
                    company_name = context[0].text
                self.job['company_name'] = company_name
                self.job['address'] = context[1].text
                self.job['job_source_url'] = job
                self.job['job_source'] = 'simplyhired'
                self.job['job_type'] = self.job_type

                self.populate_salary(context)

                descriptions = self.get_element(
                    locator='css-10747oj', alls=True)
                self.job['job_description'] = descriptions[1].text
                self.job['job_description_tags'] = descriptions[1].get_attribute(
                    'innerHTML')

                self.scraped_jobs.append(self.job.copy())
                self.job = {}
            except Exception as e:
                saveLogs(e)


@log_scraper_running_time("SimplyHired")
def simply_hired(url: str, job_type: str) -> None:
    try:
        simply_hired_scraper = SimplyHiredScraper(job_type=job_type, url=url)
        simply_hired_scraper.run_simplyhired()
    except Exception as e:
        saveLogs(e)
    finally:
        simply_hired_scraper.delete_self()
