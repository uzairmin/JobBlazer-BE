from datetime import timedelta, datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from scraper.utils.helpers import remove_emojis, sleeper
from utils.helpers import saveLogs, log_scraper_running_time
from scraper.jobs.base_scraper import BaseScraper

REMOTEOK_BASEURL = "https://remoteok.com"
JOB_SOURCE = "remoteok"
class RemoteOkScraper(BaseScraper):
    def __init__(self,job_type, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.job_type:str = job_type

    def load_jobs(self):
        previous_jobs = self.get_element(locator="job", alls=True)
        previous_len = len(previous_jobs)
        while True:
            if not self.check_if_job_day_ago(previous_jobs[previous_len-1]):
                break
            sleeper()
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleeper()
            previous_jobs = self.get_element(locator="job", alls=True)
            if previous_len == len(previous_jobs):
                break
            previous_len = len(previous_jobs)


    def get_job_urls(self):
        self.load_jobs()
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "tr[data-slug][data-id]"))
            )
        except Exception as e:
            saveLogs(e)
        job_urls = self.get_element(selector="css", locator="tr[data-slug][data-id]", alls=True)
        links = []
        for job_url in job_urls:
            try:
                link = job_url.get_attribute("data-href")
                links.append(REMOTEOK_BASEURL+link)
            except Exception as e:
                saveLogs(e)
        return links

    def check_if_job_day_ago(self, job):
        day_ago = False
        try:
            date_elm = self.get_element(selector="tag", locator="time", parent=job)
            date_str = date_elm.get_attribute("datetime")
            date_obj = datetime.fromisoformat(date_str)
            current_date = datetime.now(tz=date_obj.tzinfo)
            one_day_ago_date = current_date - timedelta(days=1)
            if date_obj >= one_day_ago_date: 
                day_ago = True
        except Exception as e:
            saveLogs(e)
        return day_ago

    def is_convertible_to_number(self, s):
        if isinstance(s, str):
            try:
                int(s)
                return True
            except ValueError:
                return False
        return False

    def find_jobs(self):
        self.driver.get(self.url)
        links = self.get_job_urls()
        self.get_previous_jobs(job_source=JOB_SOURCE,urls=links)
        original_window = self.driver.current_window_handle
        try:
            for link in links:
                if self.previous_links.get(link):
                    continue
                try:
                    self.driver.switch_to.new_window('tab')
                    self.driver.get(link)
                    sleeper()
                    id = link.split("-")[-1]
                    if self.is_convertible_to_number(id):
                        id = int(id)
                        job = WebDriverWait(self.driver, 40).until(
                            EC.presence_of_element_located(
                            (By.CLASS_NAME, f"job-{id}"))) 
                        job_desc = WebDriverWait(self.driver, 40).until(
                            EC.presence_of_element_located(
                            (By.CLASS_NAME, "expandContents")))
                        temp = self.get_element(locator="company_and_position", parent=job).text
                        temp = temp.splitlines()
                        self.job['job_title'] = remove_emojis(temp[0])
                        self.job['company_name'] = remove_emojis(temp[1])
                        address = remove_emojis(temp[2])
                        self.job['address'] = address.split('$')[0]
                        self.job['job_description'] = job_desc.text
                        self.job['job_source_url'] = link
                        self.job['job_posted_date'] = self.get_element(locator="time", parent=job).text
                        salary_format = "yearly"
                        self.job['salary_format'] = salary_format
                        temp2 = temp[-1].split(" ")
                        if len(temp2[-3]) >= 4 and temp2[-3][0] == "$":
                            salary_min = remove_emojis(temp2[-3])
                        else:
                            salary_min = "N/A"
                        self.job["salary_min"] = salary_min
                        if len(temp2[-1]) >= 4 and temp2[-1][0] == "$":
                            salary_max = remove_emojis(temp2[-1])
                        else:
                            salary_max = "N/A"
                        self.job["salary_max"] = salary_max
                        if salary_max == "N/A" or salary_min == "N/A":
                            estimated_salary = "N/A"
                        else:
                            estimated_salary = f"{salary_min}-{salary_max}"
                        self.job["estimated_salary"] = estimated_salary
                        self.job['job_source'] = JOB_SOURCE
                        self.job['job_type'] = self.job_type
                        self.job['job_description_tags'] = str(job_desc.get_attribute("innerHTML"))

                        self.scraped_jobs.append(self.job.copy())
                        self.job={}
                except Exception as e:
                        saveLogs(e)
                    
                self.driver.close()
                self.driver.switch_to.window(original_window)
        except Exception as e:
            saveLogs(e)
        if self.scraped_jobs:
            self.export_to_excel(scraper_name=JOB_SOURCE, job_source="Remote ok")

# code starts from here
@log_scraper_running_time("RemoteOk")
def remoteok(link, job_type):
    try:
        remoteok_scraper = RemoteOkScraper(job_type=job_type, url=link)
        remoteok_scraper.find_jobs()
    except Exception as e:
        saveLogs(e)
    finally:
        remoteok_scraper.delete_self()
