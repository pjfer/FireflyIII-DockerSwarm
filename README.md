# GIC_Project

The project is about providing a finance manager to a medium accounting firm, with 400 employes, where 200 of them will use the system, simultaneously.

## Getting Started

To smoothly run this project, please make sure you have the following prerequisites and software installed.

### Prerequisites

Since the project was built to run with [Python3](https://www.python.org/downloads/), you must have [Python3](https://www.python.org/downloads/) installed on your computer.

### Installing

It is necessary to install [Docker](https://docs.docker.com/get-docker/) to run our system.

## Deployment

For the postgreSQL database, you need to create the database, user and password to be used. We use docker secrets to do it, so to create the secrets, you **must** run, on the console, the following commands:

```
echo "firefly" | docker secret create firefly3-postgres-db -
echo "firefly" | docker secret create firefly3-postgres-user -
echo "secret_firefly_password" | docker secret create firefly3-postgres-passwd -
```

You'll also need to create the configs. Firstly, enter the docker folder and change the ip in the **proxy_set_header   X-Forwarded-Host** inside the **nginx.conf** file. Afterwards, still inside the docker folder, run:

```
docker config create firefly3-postgresql postgresql.conf
docker config create firefly3-pg_hba pg_hba.conf
docker config create firefly3-nginx nginx.conf
```

To start a swarm in docker swarm, run the following command on the console:

`docker swarm init --advertise-addr <MANAGER-IP>`

After creating the swarm, a command should be printed in the console, so you can add nodes to the created swarm. That command must be run in the machines that you want to add to the swarm.

If you need to change the type of a node, firstly run the following command to retrieve the node's id and save it into the node1_id variable:

`node1_id=$(docker node list | grep <HOSTNAME from the docker node list command> | awk '{print $1}')`

Then, if you want to make the node the leader of the swarm, run:

`docker node update --label-add type=primary ${node1_id?}`

Otherwise, run:

`docker node update --label-add type=replica ${node1_id?}`

Then, inside the docker folder, run:

`docker stack deploy -c docker-compose.yml <APP_NAME>`

To review the status of the services, run:

`docker service ls`

To stop and remove all services and containers, run:

`docker stack rm <APP_NAME>`

## Testing

Before running our script, you **must** the **BASE_URL**, **AUTHORIZE_URL** and **ACCESS_TOKEN_URL** to **your** ip or domain.
To use the script that we created to test our system, simply go to the loadSimulator folder and run:

`./script.sh <NUMBER_CLIENTS>`

Then, pay attention to the generated files inside the credentials and logs folders, once they are used for debugging. If everything goes smoothly, the files inside the credentials folder must contain something like

`{"email": "user2@mail.com", "client_id": 10, "client_secret": "tWSdvvWILtrBGddpms3aE2IT6LoYuGioBme2OgNv"}`

And the files inside the logs folder, must contain a series of lines reporting the status of the client, like this:

```
Client created
Accounts created
Category created
...
Expense transaction created
Expenses transactions created
Revenue transaction created
Enter the Reports
Client lifecycle ended.
```

It's normal if this files take a while to be fulfilled, after the script terminates.

## Built With

* Python3
* Docker, Docker Compose

## Authors

* **Pedro Ferreira**
* **Rafael Teixeira**