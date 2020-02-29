import csv


def save_to_file(jobs):
    file = open("jobs.csv", mode="w", encoding="utf-8", newline="")
    writer = csv.writer(file)
    # csv file에 기록
    writer.writerow(["title", "company", "location", "link"])
    # csv 일에 행을 입력
    for job in jobs:
        writer.writerow(list(job.values()))
    # dictionary형 자료의 value들을 리스트화 하여 csv에 입력
