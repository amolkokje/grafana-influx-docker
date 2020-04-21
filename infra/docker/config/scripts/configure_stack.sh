#!/bin/bash

# Wait for Grafana to start up before doing anything.
until curl -G http://grafana:${GRAFANA_HTTP_PORT}/api/health -o /dev/null; do
    echo "Waiting for Grafana ..."
    sleep 1
done
echo "Grafana is Up."

# Wait for InfluxDB to start up before doing anything.
until curl -G http://influxdb:${INFLUXDB_DATA_PORT}/ping -o /dev/null; do
    echo "Waiting for InfluxDB ..."
    sleep 1
done
echo "InfluxDB is Up."

echo "Grafana: Add a guest user"
curl -XPOST -H "Content-Type: application/json" -d '{
  "name":"Guest",
  "email":"user@graf.com",
  "login":"guest",
  "password":"guest"
}' http://admin:admin@grafana:3000/api/admin/users