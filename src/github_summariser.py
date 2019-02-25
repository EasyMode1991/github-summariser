import requests
from bs4 import BeautifulSoup
# http

import json
import re
# standard lib

# helper functions
def get_text(link):
    try:
        return str(link.text.encode('utf-8'))
    except Exception as e:
        return e

def formatted(raw_total):
    try:
        return int(''.join(ele for ele in raw_total if ele.isdigit()))
    except Exception as e:
        return e

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    return links

class GithubPage(object):

    def __init__(self, url, access_token):
        assert "github" in url
        self.url = url
        self.identity = self._url_identity()
        self.access_token = access_token
        self._org_or_repo()

    def _url_identity(self):
        return re.sub("https://github.com/", "", self.url)

    def _org_or_repo(self):
        if "/" not in self.identity:
            self.org = self.identity
            self.repo = ""
            return

        self.org = self.identity[:self.identity.find("/")]
        print("org - " + self.org)

        self.repo = self.identity[self.identity.find("/") + 1:]
        print("repo - " + self.repo)


    def _access_api(self, endpoint):
        url = "https://api.github.com" + endpoint + "?access_token=" + self.access_token
        print(url)
        response = requests.get(url)
        result = json.loads(response.text)
        return result


    def summarise(self):
        raise NotImplemented

class GitHubRepository(GithubPage):

    def get_numbers(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('span', class_ = "num text-emphasized")
        numbers = list(map(formatted, list(map(get_text, links))))
        return {"Total Commits":numbers[0],
                "Branches":numbers[1],
                "Releases":numbers[2],
                "Total Contributers":numbers[3]}


    def total_merged_pull_requests(self):
        try:
            raw_total =  list(filter(lambda x: 'Total' in x, list(map(get_text, get_links(
                "https://github.com/{}/{}/pulls?q=is%3Apr+is%3Amerged".format(self.org, self.repo))))))[0]
        except Exception as e:
            print(e)
            raw_total = '0000'

        return formatted(raw_total)

    def get_stars(self):
        response = requests.get(self.url + "/stargazers")

    def last_year_weekly_commits(self):
        return self._access_api("/repos/{0}/{1}/stats/commit_activity".format(self.org, self.repo))

    def last_four_weeks_commits(self):
        return self.last_year_weekly_commits()[-4:]

    def total_year_commits(self):
        return sum(list(filter(lambda x: x != None, list(map(lambda x: x["total"], self.last_year_weekly_commits())))))

    def milestones(self):
        return self._access_api("/repos/{}/{}/milestones".format(self.org, self.repo))

    def punch_card(self):
        # this shows the commits per hour per day
        return self._access_api("/repos/{}/{}/stats/punch_card".format(self.org, self.repo))

    def pull_requests(self):
        return self._access_api("/repos/{}/{}/pulls".format(self.org, self.repo))

    def events(self):
        return self._access_api("/repos/{}/{}/issues/events".format(self.org, self.repo))

    def participation(self):
        return self._access_api("/repos/{}/{}/stats/participation".format(self.org, self.repo))

    def code_frequency(self):
        return self._access_api("/repos/{}/{}/stats/code_frequency".format(self.org, self.repo))

    def commit_activity(self):
        return self._access_api("/repos/{}/{}/stats/commit_activity".format(self.org, self.repo))

    def info(self):
        return self._access_api("/repos/{}/{}".format(self.org, self.repo))

    def contributors(self):
        return self._access_api("/repos/{}/{}/contributors".format(self.org, self.repo))

    def contributors_stats(self):
        return self._access_api("/repos/{}/{}/stats/contributors".format(self.org, self.repo))

    def summarise(self):
        i = self.info()
        full_name = i["full_name"]
        try:
            stats  = {"Watchers":i["watchers_count"],
                      "Open Issues":i["open_issues_count"],
                      "Last Update":i["updated_at"],
                      "Forks":i["forks"],
                      "Language":i["language"],
                      "Description":i["description"],
                      "Size":i["size"],
                      "Owner":full_name[:full_name.find('/')],
                      "Name":full_name[full_name.find('/') + 1:]}
            numbers = self.get_numbers()
            return {**numbers, **stats}

        except Exception as e:
            return {"Exception":e}

class GitHubOrganisation(GithubPage):

    def get_info(self):
        return self._access_api("/orgs/" + self.org)

    # def summarise(self):
    #     i = self.get_info()
    #     result = {"Watchers":,
    #               "Open Issues":,
    #               "Last Update":,
    #               "Forks":,
    #               "Language":,
    #               "Description":,
    #               "Fork":,
    #               "Size":,
    #               "Repo":,
    #               "Owner":,}
    #     raise result


class GitHubUser(object):
    def __init__(self, username):
        self.name = username

    def _access_api(self, endpoint):
        url = "https://api.github.com" + endpoint + "?access_token=" + self.access_token
        print(url)
        response = requests.get(url)
        result = json.loads(response.text)
        return result

    def get_info(self):
        return self._access_api("/users/" + self.username)

    def get_followers(self):
        info = self.get_info()
        return _access_api(info['followers_url'])

    def get_orgs(self):
        info = self.get_info()
        return _access_api(info["organisations_url"])

    def get_events(self):
        return self._access_api("/users/{}/events/public".format(self.username))

    def get_repos(self):
        return self._access_api("/users/{}/repos".format(self.username))



def main():
    print("This is a module")

if __name__ == "__main__":
    main()
