# grafana-influx-docker

Docker-compose to deploy Grafana and InfluxDB docker containers, with pre-configured datasources and dashboards

## Configuration
- Grafana/InfluxDB config is done using environment vars as well as mounted volumes.
- For grafana config note the volumes that are used for config.
```
    volumes:
      # datasource - All pre-configured data sources will go here
      - "./config/provisioning:/etc/grafana/provisioning"
      # grafana server configuration file
      - "./config/grafana/custom.ini:/etc/grafana/custom.ini"
      # dashboards - All pre-configured dashboards will go here
      - "./config/grafana/dashboards:/var/lib/grafana/dashboards"
```
- InfluxDB config is done using env vars, but mounted volumes can also be used if this is not sufficient, just like
grafana.
- NOTE: The data drive of influxdb "/var/lib/influxdb" can be mounted to local drive if need to persist data between
restarts.
- Container "configure_stack" is a short lived container where the main service is the configure_stack.sh script which
enables the user to put custom configuration code/scripts that cannot be performed using already provided hooks. Using
a python container here so that it allows you to use python scripts too, but can be any container.

## Startup
To deploy the docker stack, use the command:
```
docker-compose -f docker-compose.yml up
```