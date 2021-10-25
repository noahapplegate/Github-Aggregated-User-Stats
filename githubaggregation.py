from flask import Flask, jsonify, request
import requests
from temp_auth import auth  # Used to authenticate github api requests

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def update_language_stats(language_counts, languages_url):
    # Get a list of languages used in this repo
    language_list = requests.get(languages_url, auth=auth).json().keys()

    # Update language_counts
    for language in language_list:
        language_counts[language] = language_counts.get(language, 0) + 1


def aggregate_github_stats(username):
    # Create variables to hold github statistics
    repo_count = 0
    stargazers_count = 0
    forks_count = 0
    avg_repo_size = 0
    language_counts = {}

    # Make requests to get a list of the user's repos
    # We start at the first page and get max number of repos per request (100)
    repos_url = f'https://api.github.com/users/{username}/repos'
    params = dict(page=1, per_page=100)

    # Make initial request
    repo_json_obj = requests.get(repos_url, params, auth=auth).json()

    # Continue requesting and aggregating stats while the returned data is not empty
    # Note: json_obj is falsy <=> json_obj == {}
    while repo_json_obj:
        repo_count += len(repo_json_obj)
        for repo_dict in repo_json_obj:
            stargazers_count += repo_dict['stargazers_count']
            forks_count += repo_dict['forks_count']
            avg_repo_size += repo_dict['size']
            update_language_stats(language_counts, repo_dict['languages_url'])

        # Request the next page of repos
        params['page'] += 1
        repo_json_obj = requests.get(repos_url, params).json()

    # Calculate average repo size
    avg_repo_size /= repo_count

    # Sort languages by their counts
    language_list = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)

    # We have aggregated data from all repos, build and return a dict containing these stats
    aggregate_data_response = dict(
        repo_count=repo_count,
        stargazers_count=stargazers_count,
        forks_count=forks_count,
        avg_repo_size=avg_repo_size,
        language_list=language_list
    )

    return aggregate_data_response


@app.route('/<string:username>')
def github_user_stats(username):
    response = aggregate_github_stats(username)
    return jsonify(response)

