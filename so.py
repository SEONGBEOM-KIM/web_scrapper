import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=python"


def get_last_page():
    html = requests.get(URL)
    soup = BeautifulSoup(html.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"})
    pages = pagination.find_all("span")[:-1]
    page_list = []

    for page in pages:
        page_num = page.get_text()
        page_list.append(page_num)

    last_page = page_list[-1]
    return int(last_page)

# recursive = False <-- child node는 가져오지 않음


def get_job_info(job):
    job_name = job.find("a", {"class": "s-link"})["title"]
    company, location = job.find("h3").find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = job["data-jobid"]
    return {"job_name": job_name, "company": company, "location": location, "link": f"https://stackoverflow.com/jobs/{job_id}/"}


def access_each_page(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        html = requests.get(f"{URL}&pg={page + 1}")
        soup = BeautifulSoup(html.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})

        for result in results:
            job = get_job_info(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = access_each_page(last_page)
    return jobs
