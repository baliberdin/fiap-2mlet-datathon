#!/bin/bash

pip install --upgrade pip
pip install prometheus-flask-exporter
mlflow ui --host 0.0.0.0 --expose-prometheus /opt/mlflow-server/log/prometheus