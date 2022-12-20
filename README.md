# datastone-test

## Getting Started

> **Important** : In order to use the service, a third party service is required. You have to get an API Key [here](https://apilayer.com/marketplace/exchangerates_data-api?_gl=1*tgrwx*_ga*NTA1NTk3MDM4LjE2NzE1NDUzMzk.*_ga_HGV43FGGVM*MTY3MTU3MDIzMi4zLjAuMTY3MTU3MDIzMi42MC4wLjA.#pricing) and then get access to [Exchangerates API](https://exchangeratesapi.io/documentation/) services.

1. Clone the repository

    * _SSH_

        ```bash
        git clone git@github.com:LucasVmigotto/datastone-test.git
        ```

    * _HTTPS_

        ```bash
        git clone https://github.com/LucasVmigotto/datastone-test.git
        ```

    * GitHub CLI

        ```bash
        gh repo clone LucasVmigotto/datastone-test
        ```

2. Copy and rename `.env.sample` to `.env`

    > Customize the values as needed

3. Prepare and initialize the [Docker](https://www.docker.com/) environment

    1. Start the API Docker Compose Service

        ```bash
        docker compose run --rm ds-api bash
        ```

    2. Once inside the container, create the python [virtual env (venv)](https://docs.python.org/3/library/venv.html)

        ```bash
        python3 -m venv ds-api-venv
        ```

    3. Active the virtual env

        ```bash
        source ds-api-venv/bin/activate
        ```

    4. Install the dependencies

        ```bash
        pip install -r requirements.txt
        ```

    5. With the dependencies installed, exit the virtual env

        ```bash
        deactivate
        ```

    6. Exit the container

        ```bash
        exit
        ```

4. Start the services

    * [REDIS](https://redis.io/)

        ```bash
        docker compose up [-d] ds-redis
        ```

    * _API_

        ```bash
        docker compose up [-d] ds-api
        ```

    > Use the `-d` flag to run the containers in detach mode

    * Use the following one-line command  to do  the last two steps at once:

        ```bash
        docker compose rm -f --stop && docker compose up -d ds-redis && docker compose up ds-api && docker compose logs -f ds-api
        ```
