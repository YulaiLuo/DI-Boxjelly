# Self defined github runner

Replace <Token> with github runner token

sudo docker run -d --restart always --name github-runner \
  -e REPO_URL="https://github.com/COMP90082-2023-SM1/DI-Boxjelly" \
  -e RUNNER_NAME="di-github-runner-1" \
  -e RUNNER_TOKEN=<Token> \
  -e RUNNER_WORKDIR="/DI-Boxjelly/_runner_workdir" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /DI-Boxjelly/_runner_workdir:/DI-Boxjelly/_runner_workdir \
  myoung34/github-runner:latest