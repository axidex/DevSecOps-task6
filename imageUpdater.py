import subprocess, sys, json

def docker_inspect(container_name_or_id):
    try:
        # Выполняем docker inspect с помощью subprocess и сохраняем вывод в переменную
        result = subprocess.run(["docker", "inspect", container_name_or_id], capture_output=True, text=True, check=True)

        # Разбираем JSON-ответ
        container_info = json.loads(result.stdout)[0]

        return container_info
    except subprocess.CalledProcessError as e:
        # Обработка ошибок, если контейнер не найден и другие
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    installUpgrade = str(sys.argv[1])
    chartName = str(sys.argv[2])
    container_name_or_id = "axidex/api1"
    container_info = docker_inspect(container_name_or_id)
    sha = container_info["RepoDigests"][0]#.split(':')[-1]
    command = f"helm {installUpgrade} {chartName} ./cdx-chart --set image.name={sha}"
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result)
    