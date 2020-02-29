import requests
from bs4 import BeautifulSoup

URL = "https://www.indeed.com/jobs?as_and=python&limit=50"


def get_last_page():
    html = requests.get(URL)
    soup = BeautifulSoup(html.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    pages = pagination.find_all("span", {"class": "pn"})

    page_list = []

    for page in pages[:-1]:
        page_num = page.get_text()
        page_list.append(page_num)

    last_page = page_list[-1]
    return int(last_page)


def get_job_info(job):
    job_name = job.find("div", {"class": "title"}).find(
        "a", {"class": "jobtitle"})["title"]
    company = job.find("div", {"class": "sjcl"}).find(
        "span", {"class": "company"})
    if company:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
    location = job.find("div", {"class": "sjcl"}).find(
        "span", {"class": "location"}).get_text()
    job_id = job["data-jk"]
    return {"job_name": job_name, "company": company,
            "location": location, "link": f"https://www.indeed.com/viewjob?jk={job_id}"}


def access_each_page(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        html = requests.get(f"{URL}&start={page * 50}")
        soup = BeautifulSoup(html.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

        for result in results:
            job = get_job_info(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = access_each_page(last_page)
    return jobs
