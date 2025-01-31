# Setup
**_NOTE_** This is currently a solo project aimed at providing a user agents that can monitor network hosts. It's currently in beta and will be updated frequently. It has not been security hardened so use at your own risk. 

## Create a .env folder in the root directory
Inside of the .env folder, create three files:
-   influxdb2-admin-password
-   influxdb2-admin-token
-   influxdb2-admin-username

In each file, update respectively. InfluxDB will use these files to create the initial admin user, password, and API token. 

## Create a .env file in the zontahnos/app/app directory
Populate this file with the fillowing:

<pre>
INFLUXDB_URL="http://influxdb2:8086"
INFLUXDB_TOKEN="The token you populated in the influxdb2-admin-token file"
ORG="netsmart"
BUCKET="network_monitoring"
GRAFANA_TOKEN="placeholder for later use"
</pre>

## Build
docker compose up --build

## InfluxDB login
You log in using the username and passwords created in the respective files above. 

URL: http://127.0.0.1:8083

## Grafana login
By default, it pulls the user/pass from the docker compose file. 

URL: http://127.0.0.1:8086
User: admin
pass: adminadmin

## API Docs
The API docs are located at:

URL: http://127.0.0.1:3000/docs

## Basic workflow
Create a new icmp monitoring DB entry using the http://127.0.0.1:8000/api/v1/icmp/create endpoint. This will return a secret whichh you should copy for use with the zontahnos agent located <placeholder>.

## I did say this is beta, right? 
Currently you will have to build out your own grafana dashboards but I will be providing some automation wrappers to do the heavy lifting shortly. 