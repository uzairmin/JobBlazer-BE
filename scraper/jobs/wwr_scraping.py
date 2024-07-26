import re
from typing import List, Union
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, \
    ElementNotVisibleException
from selenium.webdriver.remote.webelement import WebElement
from django.utils import timezone
from scraper.utils.helpers import ScraperNaming, make_plural, previous_jobs, sleeper
from utils.helpers import saveLogs
from .base_scraper import BaseScraper


class WeWorkRemotelyScraper(BaseScraper):
    def __init__(self, *args, **kwargs):
        self.DATE_CONST = "%Y-%m-%dT%H:%M:%SZ"
        super().__init__(*args, **kwargs)

    def request_page(self) -> None:
        self.driver.get(self.url)

    def home_page_loaded(self) -> bool:
        loaded: bool = False
        for retry in range(1, 6):
            try:
                self.request_page()
                homepage_element: WebElement = self.get_element(
                    locator='jobs-container')
                if homepage_element:
                    loaded = True
                    break
            except (WebDriverException, TimeoutException, NoSuchElementException, ElementNotVisibleException) as e:
                if retry >= 5:
                    saveLogs(e)
                    self.driver.quit()
                    break
        return loaded

    def extract_links(self) -> List[str]:
        job_links: list[str] = []
        if self.home_page_loaded():
            sleeper()
            jobs_list: list[WebElement] = self.get_element(locator='section.jobs ul li:not(.view-all)', selector='css',
                                                           alls=True)
            for item in jobs_list:
                anchor_elements: list[WebElement] = self.get_element(selector='tag', locator='a', parent=item,
                                                                     alls=True)
                if anchor_elements and anchor_elements[1]:
                    job_links.append(anchor_elements[1].get_attribute('href'))
        return job_links

    def extract_salary(self, salary: str) -> None:
        pattern = r"\$(?P<min>[0-9,]+)(?:\s*-\s*\$(?P<max>[0-9,]+))?(\s+OR\s+MORE)?\s+(?P<format>[A-Z]+)"
        match = re.search(pattern, salary)
        if match:
            min_salary = match.group("min") or ""
            max_salary = match.group("max") or min_salary
            unit = match.group("format") or "USD"
            currency_format = "yearly" if int(
                max_salary.replace(',', '')) > 1000 else "monthly"
            self.job['salary_min'] = f"{min_salary}"
            self.job['salary_max'] = f"{max_salary}"
            self.job['salary_format'] = currency_format
            self.job['estimated_salary'] = f"{min_salary} - {max_salary} {unit}"
        else:
            self.job['salary_min'] = "N/A"
            self.job['salary_max'] = "N/A"
            self.job['salary_format'] = "N/A"
            self.job['estimated_salary'] = "N/A"

    def get_job_type(self, job_type: str) -> None:
        default_type: str = 'full time remote'
        if job_type == 'FULL-TIME':
            default_type: str = 'full time remote'
        if job_type == 'CONTRACT':
            default_type: str = 'contract remote'
        self.job['job_type'] = default_type

    def parse_posted_date(self, datetime_str: str) -> str:
        pattern = r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)$'
        match = re.match(pattern, datetime_str)
        if match:
            day_span = 24 * 60 * 60
            datetime_str = match.group(1)
            datetime_obj = timezone.datetime.strptime(
                datetime_str, self.DATE_CONST)
            current_time = timezone.now().replace(tzinfo=None)
            time_difference = (current_time - datetime_obj).total_seconds()
            days = time_difference // day_span
            # Remove days to get only hours or minutes
            time_difference = time_difference - days * day_span
            minutes = time_difference // 60
            hours = time_difference // (60 * 60)
            # Increment days if hours > 20
            if hours >= 20:
                days += 1
            if days == 0:
                if hours == 0:
                    result = f"{int(minutes)} {make_plural('minute', minutes)} ago"
                else:
                    result = f"{int(hours)} {make_plural('hour', hours)} ago"
            else:
                result = f"{int(days)} {make_plural('day', days)} ago"
        else:
            result = datetime_str
        return result

    def extract_values_from_header(self, header: Union[WebElement, None]) -> None:
        try:
            element: Union[WebElement, List[WebElement], None]
            if header:
                # Job Posted Date
                element: WebElement = self.get_element(locator='.listing-header-container time', selector='css',
                                                       parent=header)
                self.job['job_posted_date'] = self.parse_posted_date(
                    element.get_attribute('datetime'))
                # Job Title
                element: WebElement = self.get_element(locator='.listing-header-container h1', selector='css',
                                                       parent=header)
                self.job['job_title'] = element.text if element else "N/A"
                # Salary Details
                element: list[WebElement] = self.get_element(selector='css', locator='a span.listing-tag',
                                                             parent=header, alls=True)
                self.extract_salary(
                    element[-1].text if element and element[-1] else '')
                # Job Type
                self.get_job_type(
                    job_type=element[0].text if element and element[0] else '')
        except Exception as e:
            saveLogs(e)

    def extract_values_from_content(self, content: Union[WebElement, None]):
        try:
            if content:
                # Job Description with Tags
                self.job['job_description_tags'] = content.get_attribute(
                    'innerHTML') if content else "N/A"
                # Job Description without Tags
                self.job['job_description'] = content.text if content else "N/A"
        except Exception as e:
            saveLogs(e)

    def extract_values_from_company_section(self, company_section: Union[WebElement, None]):
        try:
            element: Union[WebElement, List[WebElement], None]
            if company_section:
                # Company Name & Address
                element: WebElement = self.get_element(
                    locator='h2', selector='tag', parent=company_section)
                self.job['company_name'] = element.text if element else "N/A"
                # Company Address
                element: WebElement = self.get_element(selector='css', locator='h3:not(.listing-pill)',
                                                       parent=company_section)
                self.job['address'] = element.text if element else "Remote"
        except Exception as e:
            saveLogs(e)

    def tab_visited(self) -> bool:
        visited = False
        try:
            header: WebElement = self.get_element(locator='listing-header')
            content: WebElement = self.get_element(
                locator='section.job div.listing-container', selector='css')
            company: WebElement = self.get_element(locator='company-card')
            if header and company and content:
                sleeper()
                self.extract_values_from_header(header=header)
                self.extract_values_from_content(content=content)
                self.extract_values_from_company_section(
                    company_section=company)
                job = self.job.copy()
                self.scraped_jobs.append(job)
                visited = True
        except WebDriverException as e:
            saveLogs(e)
        return visited

    def find_jobs(self) -> None:
        try:
            urls: list[str] = self.extract_links()
            if len(urls) > 0:
                existing_jobs = previous_jobs(
                    source='weworkremotely', urls=urls)
                for url in urls:
                    if existing_jobs.get(url):
                        continue
                    try:
                        self.job['job_source_url'] = url
                        self.job['job_source'] = 'weworkremotely'
                        self.driver.get(url=url)
                        visited: bool = self.tab_visited()
                        if visited:
                            self.job.clear()
                        else:
                            continue
                    except Exception as e:
                        saveLogs(e)
                        continue
            if self.scraped_jobs:
                self.export_to_excel(
                    scraper_name=ScraperNaming.WE_WORK_REMOTELY,
                    job_source='WeWorkRemotely'
                )
        except Exception as e:
            saveLogs(e)


def weworkremotely(url: str, job_type: str) -> None:
    try:
        wwr_scraper = WeWorkRemotelyScraper(url=url, block_elements=['img'])
        wwr_scraper.find_jobs()
    except Exception as e:
        saveLogs(e)
    finally:
        wwr_scraper.delete_self()
