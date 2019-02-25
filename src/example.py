from github_summariser import GitHubRepository, GitHubOrganisation


def main():
    access_token = "PLACE YOUR API KEY HERE"
    org_url = "ORG URL HERE"
    org = GitHubOrganisation(url, access_token)
    print(org.get_info())

    url = "REPO URL HERE"
    repo = GitHubRepository(url, access_token)
    print(repo.summarise())

if __name__ == "__main__":
    main()
