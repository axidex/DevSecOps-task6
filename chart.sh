#!/bin/bash

CHART_NAME=$1

# Проверяем, существует ли релиз
if helm list | grep -q $CHART_NAME; then
  # Релиз уже существует, выполняем обновление
  helm upgrade $CHART_NAME ./$CHART_NAME-chart
else
  # Релиз не существует, выполняем установку
  helm install $CHART_NAME ./$CHART_NAME-chart
fi