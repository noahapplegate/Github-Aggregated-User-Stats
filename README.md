# Github-Aggregated-User-Stats
<h4 style="margin-left:5%">Returns JSON containing a github user's total number of repos, total number of 
stargazers, total number of forks, average repo size in KB, and a list of languages used.</h4>
<h4>Hosted at: https://radiant-garden-83945.herokuapp.com/
<h3>How to use:</h3>
<div style="margin-left:5%">
  <p>To use this API visit https://radiant-garden-83945.herokuapp.com/{github_username}</p>
  <p>To filter out data from repositories that have been forked, 
                set the query string parameter 'forked=0'</p>
  <p>Example: https://radiant-garden-83945.herokuapp.com/fabpot?forked=0</p>
</div>
<h3>Running locally:</h3>
<div style="margin-left:5%">
  <ol>
    <li>Navigate to the project folder in a terminal.</li>
    <li>Create and start a virtual environment.
      <br><strong>python3 -m venv .venv</strong>
      <br><strong>source .venv/bin/activate</strong></li>
    <li>Install dependencies.
      <br><strong>pip3 install -r requirements.txt</strong></li>
    <li>Export the FLASK_APP environment variable.
      <br><strong>export FLASK_APP=githubaggregation</strong></li>
    <li>Run the Flask app.
      <br><strong>flask run</strong></li>
  </ol>
  <p>The app is now running on local host: http://127.0.0.1:5000/</p>
</div>
