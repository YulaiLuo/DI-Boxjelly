# Deploy a self-hosted github actions runner as container

Run the following command on the instance your want to deploy the instance

**Note**: 
1. Replace *\<Runner Token>* with github runner token, you can get the runner token on repository setting actions page
2. The following command is only to set up a repository runner, more details about set up a org/enterprise runner can be accessed [here](https://github.com/myoung34/docker-github-actions-runner/wiki/Usage).

        sudo docker run -d --restart always --name github-runner \
            -e REPO_URL="https://github.com/COMP90082-2023-SM1/DI-Boxjelly" \
            -e RUNNER_NAME="github-runner" \
            -e RUNNER_TOKEN=<Runner Token> \
            -e RUNNER_WORKDIR="/DI-Boxjelly/_runner_workdir" \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -v /DI-Boxjelly/_runner_workdir:/DI-Boxjelly/_runner_workdir \
            myoung34/github-runner:latest

Script behavior:
    By running the above script on a instance, you will have a github action self-hosted runner as a Docker container on this instance. This runner will be connected to the **REPO_URL**, which is *https://github.com/COMP90082-2023-SM1/DI-Boxjelly* in this case. The runner will be named as **RUNNER_NAME**, the working directory of this runner will be named as **RUNNER_WORKDIR**. The container will have two volumns outside the container.

