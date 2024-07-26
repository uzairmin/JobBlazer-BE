from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from scraper.constants.const import *
from scraper.utils.helpers import k_conversion, set_job_type, sleeper
from utils.helpers import saveLogs, log_scraper_running_time
from scraper.jobs.base_scraper import BaseScraper

JOB_SOURCE = "ycombinator"


class YCombinatorScraper(BaseScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def finding_job(self):
        try:
            loc_type = ''
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'bg-beige-lighter'))
            )
            self.job['job_title'] = self.get_element(
                locator='company-name').text
            details = self.get_element('company-details', alls=True)
            details_loc = self.get_element(
                selector='tag', locator='div', alls=True, parent=details[1])
            self.job['address'] = details_loc[0].text
            if 'remote' in details[1].text.lower():
                loc_type = 'remote'
            elif 'hybrid' in details[1].text.lower():
                loc_type = 'hybrid'
            else:
                loc_type = 'onsite'
            job_type_check = details_loc[2].text
            if 'full-time' in job_type_check.lower():
                job_type = 'full time'
            elif 'contract' in job_type_check.lower():
                job_type = 'contract'
            else:
                return
            self.job['job_type'] = set_job_type(job_type, loc_type)
            self.job['job_source'] = JOB_SOURCE
            self.job['job_posted_date'] = 'N/A'
            description = self.get_element(locator='bg-beige-lighter')
            job_description = self.get_element(
                selector='tag', locator='div', alls=True, parent=description)

            desc = ""
            desc_tags = ""
            for i in range(1, len(job_description)):
                desc += job_description[i].text
                desc_tags += job_description[i].get_attribute('innerHTML')
            self.job['job_description'] = desc
            self.job['job_description_tags'] = desc_tags
            self.job['job_source_url'] = self.driver.current_url
            salary = self.get_element(locator='company-title')
            slr = self.get_element(
                selector='tag', locator='div', alls=True, parent=salary)
            if len(slr) > 0 and slr[0].text != '':
                estimated_salary = self.get_element(
                    selector='tag', locator='span', parent=slr[1]).text
                if '-' in estimated_salary:
                    salary_min = estimated_salary.split(' - ')[0]
                    salary_max = estimated_salary.split(' - ')[1]
                    salary_format = 'N/A'
                else:
                    salary_min = estimated_salary.split('K')[0]
                    salary_max = estimated_salary.split('K')[0]
                    salary_format = 'N/A'
            else:
                salary_format = 'N/A'
                estimated_salary = 'N/A'
                salary_min = 'N/A'
                salary_max = 'N/A'
            self.job['salary_min'] = k_conversion(salary_min)
            self.job['salary_max'] = k_conversion(salary_max)
            self.job['estimated_salary'] = k_conversion(estimated_salary)
            self.job['salary_format'] = salary_format

            self.scraped_jobs.append(self.job.copy())
            self.job = {}
        except Exception as e:
            saveLogs(e)

    def company_jobs(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'job-name'))
            )
            job_name = self.get_element(locator='job-name', alls=True)
            for job in job_name:
                try:
                    link = self.get_element(
                        selector='tag', locator='a', parent=job).get_attribute('href')
                    if self.previous_links.get(link):
                        continue
                    self.job['company_name'] = self.get_element(
                        locator='company-name').text
                    original_window = self.driver.current_window_handle
                    self.driver.switch_to.new_window('tab')
                    self.driver.get(link)
                    self.finding_job()
                    self.driver.close()
                    self.driver.switch_to.window(original_window)
                except Exception as e:
                    saveLogs(e)
        except Exception as e:
            saveLogs(e)

    def loading(self):
        while True:
            try:
                sleeper()
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'loading'))
                )
                load = self.get_element(locator='loading', alls=True)
                if len(load) > 0:
                    load[0].location_once_scrolled_into_view
                else:
                    break
            except Exception as e:
                break

    def login(self):
        try:
            sleeper()
            self.get_element(locator='MuiTypography-root').click()
            sleeper()
            self.get_element(locator='input-group', alls=True)[3].click()
            sleeper()
            email = self.get_element(locator='MuiInput-input', alls=True)[3]
            email.clear()
            email.send_keys(Y_EMAIL)
            sleeper()
            self.get_element(locator='input-group', alls=True)[4].click()
            sleeper()
            password = self.get_element(locator='MuiInput-input', alls=True)[4]
            password.clear()
            password.send_keys(Y_PASSWORD)
            sleeper()
            self.get_element(locator='sign-in-button').click()
            sleeper()
            return True
        except Exception as e:
            return False

    # find's job name
    def find_jobs(self):
        try:
            self.driver.get(YCOMBINATOR_LOGIN_URL)
            if not self.login():
                return
            self.driver.get(self.url)
            self.loading()
            companies = self.get_element(locator='text-2xl', alls=True)
            self.get_previous_jobs(job_source=JOB_SOURCE)
            for i in range(1, len(companies)):
                try:
                    link = self.get_element(selector='tag', locator='a', alls=True, parent=companies[i])[
                        0].get_attribute('href')
                    original_window = self.driver.current_window_handle
                    self.driver.switch_to.new_window('tab')
                    self.driver.get(link)
                    self.company_jobs()
                    self.driver.close()
                    self.driver.switch_to.window(original_window)
                except Exception as e:
                    saveLogs(e)
            if len(self.scraped_jobs) > 0:
                self.export_to_excel(JOB_SOURCE, 'YCombinator')
        except Exception as e:
            saveLogs(e)

# code starts from here


@log_scraper_running_time("YCombinator")
def ycombinator(link, job_type):
    try:
        ycombinator = YCombinatorScraper(url=link)
        ycombinator.find_jobs()
    except Exception as e:
        saveLogs(e)
    finally:
        ycombinator.delete_self()
