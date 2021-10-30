import requests
import yagmail


def get_owner_repo(ghurl):
    owner = repo = None

    response_list = ghurl.split('/')
    owner = response_list[3]
    repo = response_list[4]
    return owner, repo


def get_languages_used(ghurl): 
    owner, repo = get_owner_repo(ghurl)
    languages = []

    api_url = f"https://api.github.com/repos/{owner}/{repo}/languages"

    response = requests.get(api_url)

    if response.status_code != 200:
        print("failed to get the languages")
        return

    languages = response.json()

    return list(languages.keys())


def get_repo_stats(ghurl):
    owner, repo = get_owner_repo(ghurl)
    issues_count = 0
    pr_count = 0
    open_issues_list = get_open_issues(ghurl)
    issues_count = len(open_issues_list)

    pr_issues_list = get_open_pulls(ghurl)
    pr_count = len(pr_issues_list)
    
    s1 = "issues count"
    s2 = "pr count"
    
    s3=issues_count
    s4 = pr_count

    s = f'{s1}={s3} , {s2}={s4}'

    return s
    

def get_open_issues(ghurl):
    owner, repo = get_owner_repo(ghurl)
    open_issues_list = []

    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    r = requests.get(api_url)

    response_open_issues_list = r.json()
    count = 1
    for item in response_open_issues_list:
        if 'pull_request' not in item:
            open_issues_list.append(f"{count}: {item['title']}")
            count += 1

    return (open_issues_list)



def get_open_pulls(ghurl):
    owner, repo = get_owner_repo(ghurl)
    pr_issues_list = []

    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    pull_response = requests.get(api_url)

    pull_requests_list = pull_response.json()
    count=1
    for item in pull_requests_list:
        if 'issues' not in item:
            pr_issues_list.append(f"{count}: {item['title']}")
            count+=1
    return pr_issues_list


def get_subscriber(ghurl):
    owner ,repo = get_owner_repo(ghurl)

    subscriber_list = []
    api_url= f"https://api.github.com/repos/{owner}/{repo}/subscribers"
    sub_list = requests.get(api_url)
    response_list=sub_list.json()
    count=1
    for item in response_list:
            subscriber_list.append(f"{count}: {item['login']}")
            count+=1
    return subscriber_list    



def save_email(email):
    print('save email',email)
    with open('emails.txt', 'a') as f:
            f.write(email + '\n')
        



def send_mail(body):
    emails = []
    lines_list = open('emails.txt').readlines()
    for line in lines_list:
        emails.append(line.replace('\n', ''))   
    yag = yagmail.SMTP('testspike5251')
    for email in emails:
        yag.send(to= emails, subject='test subject',
        contents=body, 
        attachments=['lang_data.txt',
                     'repo_data.txt', 
                     'issue_data.txt', 
                     'pr_data.txt']
                    )
if __name__ == '__main__':
    send_mail(body = """this is a skillaura internship program !!.
                    The following mail consists information of a github repository.
                    Please refer to the below documents for more details""")