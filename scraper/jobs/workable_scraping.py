import html

from .base_scraper import BaseScraper

from scraper.utils.helpers import ScraperNaming, set_job_type, sleeper
from utils.helpers import saveLogs, log_scraper_running_time


class WorkableScraper(BaseScraper):
    def __init__(self, *args, **kwargs):
        self.count = 0
        self.flag = True
        super().__init__(*args, **kwargs)

    # loading jobs
    def loading(self):
        try:
            sleeper()
            load = self.get_element(locator="jobsList__button-container--3FEJ-")
            btn = self.get_element(selector='tag', locator="button", parent=load)
            btn.location_once_scrolled_into_view
            btn.click()
            self.count += 1
            self.flag = False if self.count == 30 else True
        except:
            self.flag = False

    def accept_cookie(self):
        try:
            self.get_element(locator="styles__primary-button--tFH2O").click()
        except Exception as e:
            saveLogs(e)

    def find_job_data_hash(self, job):
        dhash = {"link": "", "tc": ""}  # tc stands for title and company
        try:
            anchor = self.get_element(selector='tag', locator="a", parent=job)
            title_n_company = anchor.get_attribute("aria-label")
            dhash["link"] = anchor.get_attribute("href")
            dhash["tc"] = str(html.unescape(
                title_n_company.replace(" at ", "-"))).lower()
        except Exception as e:
            saveLogs(e)
        return dhash

    def find_jobs(self, job_type):
        try:
            sleeper()
            raw_jobs = self.get_element(locator="jobsList__list-item--3HLIF", alls=True)
            jobs, tcs, urls = zip(*[(dhash := self.find_job_data_hash(job), dhash["tc"], dhash["link"])
                                    for job in raw_jobs])
            self.previous_company_wise_titles(list(tcs))
            self.get_previous_jobs(job_source='workable', urls=list(urls))
            for job in list(jobs):
                try:
                    if self.previous_links.get(job["link"]) or self.previous_tcs.get(job["tc"]):
                        continue
                    self.driver.get(job["link"])
                    self.get_element(locator="jobBreakdown__job-breakdown--31MGR", timeout=30)
                    job_title = self.get_element(locator="jobOverview__job-title--kuTAQ")
                    self.job["job_title"] = job_title.text
                    company_name = self.get_element(locator="companyName__link--2ntbf")
                    self.job["company_name"] = company_name.text
                    address = self.get_element(locator="jobDetails__job-detail--3As6F", alls=True)[1]
                    self.job["address"] = address.text
                    job_description = self.get_element(locator="jobBreakdown__job-breakdown--31MGR")
                    self.job["job_description"] = job_description.text
                    self.job["job_source_url"] = self.driver.current_url
                    job_posted_date = self.get_element(
                        locator="jobOverview__date-posted-container--9wC0t")
                    self.job["job_posted_date"] = job_posted_date.text
                    self.job["job_source"] = "Workable"
                    self.job["estimated_salary"] = "N/A"
                    self.job["salary_format"] = "N/A"
                    self.job["salary_min"] = "N/A"
                    self.job["salary_max"] = "N/A"
                    try:
                        job_type_check = self.get_element(locator="jobOverview__job-details--3JOit")
                        if 'contract' in job_type_check.text.lower():
                            self.job["job_type"] = set_job_type(
                                'Contract', self.determine_job_sub_type(job_type_check.text))
                        elif 'full time' in job_type_check.text.lower():
                            self.job["job_type"] = set_job_type(
                                'Full time', self.determine_job_sub_type(job_type_check.text))
                        else:
                            self.job["job_type"] = set_job_type(job_type)
                    except Exception as e:
                        saveLogs(e)
                        self.job["job_type"] = set_job_type(job_type)
                    self.job["job_description_tags"] = job_description.get_attribute(
                        'innerHTML')
                    self.scraped_jobs.append(self.job.copy())
                    self.job = {}
                except Exception as e:
                    saveLogs(e)
            if self.scraped_jobs:
                self.export_to_excel(ScraperNaming.WORKABLE, 'Workable')
        except Exception as e:
            saveLogs(e)

    def determine_job_sub_type(self, type):
        sub_type = 'onsite'
        if 'remote' in type.lower():
            sub_type = 'remote'
        if 'hybrid' in type.lower():
            sub_type = 'hybrid'
        return sub_type

    def run(self, job_type):
        try:
            self.driver.get(self.url)
            self.accept_cookie()
            while self.flag:
                self.loading()
            self.find_jobs(job_type)
        except Exception as e:
            saveLogs(e)


@log_scraper_running_time("Workable")
def workable(link, job_type):
    try:
        workable = WorkableScraper(url=link, block_elements=['img'])
        workable.run(job_type)
    except Exception as e:
        saveLogs(e)
    finally:
        workable.delete_self()
