from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def update_language_stats(language_counts, languages_url):
    # Get a list of languages used in this repo
    language_list = requests.get(languages_url).json().keys()

    # Update language_counts
    for language in language_list:
        language_counts[language] = language_counts.get(language, 0) + 1


def aggregate_github_stats(username, show_forked):
    # Create variables to hold aggregated statistics
    total_repo_count = 0
    total_stargazers_count = 0
    total_forks_count = 0
    avg_repo_size = 0
    language_counts = {}

    # Make initial request
    # Note: 100 is the maximum value for the per_page parameter
    repos_url = f'https://api.github.com/users/{username}/repos'
    params = dict(page=1, per_page=100)

    repo_json_obj = requests.get(repos_url, params).json()

    # Continue requesting and aggregating stats while the returned data is not empty
    # If show_forked is false and forks_count == 0 we skip that repo
    # Note: json_obj is falsy <=> json_obj == {}
    while repo_json_obj:
        for repo_dict in repo_json_obj:
            forks_count = repo_dict['forks_count']
            if show_forked or forks_count == 0:
                total_repo_count += 1
                total_stargazers_count += repo_dict['stargazers_count']
                total_forks_count += forks_count
                avg_repo_size += repo_dict['size']
                update_language_stats(language_counts, repo_dict['languages_url'])

        # Request the next page of repos
        params['page'] += 1
        repo_json_obj = requests.get(repos_url, params).json()

    # Calculate average repo size
    if total_repo_count != 0:
        avg_repo_size /= total_repo_count

    # Sort languages by their counts and store it as a list
    language_list = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)

    # We have aggregated data from all repos, build and return a dict containing these stats
    aggregate_data_response = dict(
        repo_count=total_repo_count,
        stargazers_count=total_stargazers_count,
        forks_count=total_forks_count,
        avg_repo_size=avg_repo_size,
        language_list=language_list
    )

    return aggregate_data_response


@app.route('/')
def home():
    return '''<h2>Github user's aggregate stats</h2>
              <h4 style="margin-left:5%">Returns JSON containing a github user's total number of repos, total number of 
              stargazers, total number of forks, average repo size in KB, and a list of languages used.</h4>
              <h3>How to use:</h3>
              <div style="margin-left:5%">
                <p>To use this API visit https://radiant-garden-83945.herokuapp.com/{username}</p>
                <p>To filter out data from repositories that have been forked, 
                set the query string parameter 'forked=0'</p>
                <p>Example: https://radiant-garden-83945.herokuapp.com/fabpot?forked=0</p>
              </div>'''


@app.route('/<string:username>')
def github_user_stats(username):
    # Validate the username
    # Return Github's missing user JSON if the user does not exist
    r = requests.get(f'https://api.github.com/users/{username}').json()
    if 'message' in r:
        return r, 404

    show_forked = bool(request.args.get('forked', default=1, type=int))
    stats_dict = aggregate_github_stats(username, show_forked)
    return jsonify(stats_dict), 200
