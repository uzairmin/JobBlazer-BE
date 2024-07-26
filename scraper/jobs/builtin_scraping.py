from scraper.utils.helpers import ScraperNaming, k_conversion, set_job_type, run_pia_proxy, change_pia_location, sleeper
from utils.helpers import saveLogs, log_scraper_running_time
from scraper.jobs.base_scraper import BaseScraper

class BuiltinScraper(BaseScraper):

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 

    def run_builtin(self):
        try:
            flag = True
            run_pia_proxy(self.driver)
            sleeper()
            self.driver.get(self.url)
            self.get_previous_jobs(job_source='builtin')
            while flag:
                flag= self.find_jobs()
        except Exception as e:
                saveLogs(e)        

    def find_jobs(self):
        try:
            sleeper()
            links = self.get_element(selector="css", locator="a[data-id='view-job-button']", alls=True)
            job_details = self.get_element(locator="job-bounded-responsive", alls=True)
            job_links = []
            job_det = []
            for link, job in zip(links,job_details):
                cur_link = link.get_attribute('href') 
                if self.previous_links.get(cur_link):
                    continue
                job_links.append(cur_link)
                job_det.append(job.text)
            original_window = self.driver.current_url
            retries  = 5
            for i, url in enumerate(job_links):
                try:
                    job_detail = job_det[i].split('\n')
                    self.job["job_title"] = job_detail[1]
                    self.job["company_name"] = job_detail[0]
                    self.job["job_source"] = "Builtin"
                    self.job["job_posted_date"] = job_detail[2]
                    self.driver.get(url)
                    sleeper()
                    outer_loop_exit = False
                    for retry in range(retries):
                        try:
                            self.get_element(selector="id", locator="read-more-description-toggle").click()
                            sleeper()
                            break
                        except Exception as e:
                            if retry == retries:
                                outer_loop_exit = True
                                break
                            error_status = change_pia_location(self.driver)
                            if not error_status:
                                self.driver.get(url)
                            else:
                                outer_loop_exit = True
                                break
                    if outer_loop_exit:
                        continue
                    try:
                        address = self.get_element(locator="company-address").text
                    except:
                        try:
                            address = self.get_element(locator="icon-description").text
                        except:
                            address = 'USA'
                    self.job["address"] = address
                    job_description = self.get_element(locator="job-description")
                    self.job["job_description"] = job_description.text
                    self.job["job_source_url"] = self.driver.current_url
                    self.populate_salary()
                    try:
                        job_type_check = self.get_element(locator="company-info")
                        if 'remote' in job_type_check.text.lower():
                            self.job["job_type"] = set_job_type('Full time', 'remote')
                        elif 'hybrid' in job_type_check.text.lower():
                            self.job["job_type"] = set_job_type('Full time', 'hybrid')
                        else:
                            self.job["job_type"] = set_job_type('Full time', 'onsite')
                    except Exception as e:
                        try:
                            job_type_check = self.get_element(locator="company-options")
                            if 'remote' in job_type_check.text.lower():
                                self.job["job_type"] = set_job_type('Full time', 'remote')
                            elif 'hybrid' in job_type_check.text.lower():
                                self.job["job_type"] = set_job_type('Full time', 'hybrid')
                            else:
                                self.job["job_type"] = set_job_type('Full time', 'onsite')
                        except Exception as e:
                            saveLogs(e)
                            self.job["job_type"] = set_job_type(self.job_type)
                    self.job["job_description_tags"] = job_description.get_attribute('innerHTML')

                    self.scraped_jobs.append(self.job.copy())
                    self.job = {}
                except Exception as e:
                    saveLogs(e)
            if len(self.scraped_jobs) > 0:
                self.export_to_excel(scraper_name=ScraperNaming.BUILTIN, job_source='builtin')
            try:
                self.driver.get(original_window)
                sleeper()
                next_page = self.get_element(locator='pagination')
                pagination = self.get_element(selector='tag', locator='li', alls=True, parent=next_page)
                next_page_anchor = self.get_element(selector='tag', locator='a', parent=pagination[-1])
                next_page_url = next_page_anchor.get_attribute('href')
                self.driver.get(next_page_url)
                return True
            except Exception as e:
                return False
        except Exception as e:
            saveLogs(e)
            return False


    def populate_salary(self):
        try:
            estimated_salary = self.get_element("provided-salary")
            salary = estimated_salary.text
            if 'hour' in salary:
                 self.job["salary_format"] = "hourly"
            elif 'Annually' in salary or 'ANNUALLY' in salary:
                self.job["salary_format"] = "yearly"
            elif 'month' in salary:
                self.job["salary_format"] = "monthly"
            else:
                self.job["salary_format"] = "N/A"
            try:
                self.job["estimated_salary"] = k_conversion(salary.split(' A')[0])
            except:
                self.job["estimated_salary"] = "N/A"
            try:
                salary_min = salary.split('A')[0].split('-')[0]
                self.job["salary_min"] = k_conversion(salary_min)
            except:
                self.job["salary_min"] = "N/A"
            try:
                salary_max = salary.split('A')[0].split('-')[1]
                self.job["salary_max"] = k_conversion(salary_max)
            except:
                self.job["salary_max"] = "N/A"
        except:
            self.job["salary_format"] = "N/A"
            self.job["estimated_salary"] = "N/A"
            self.job["salary_min"] = "N/A"
            self.job["salary_max"] = "N/A"

@log_scraper_running_time("Builtin")
def builtin(link, job_type):
    try:
        builtin_scraper = BuiltinScraper(url=link)
        builtin_scraper.run_builtin()
    except Exception as e:
        saveLogs(e)
    finally:
        builtin_scraper.delete_self()

