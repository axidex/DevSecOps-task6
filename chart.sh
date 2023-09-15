#!/bin/bash

CHART_NAME=$1

# Проверяем, существует ли релиз
if helm list | grep -q $CHART_NAME; then
  # Релиз уже существует, выполняем обновление
  python3.10 imageUpdater.py upgrade $CHART_NAME
else
  # Релиз не существует, выполняем установку
  python3.10 imageUpdater.py install $CHART_NAME
fi