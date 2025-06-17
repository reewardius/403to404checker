import argparse
import requests
import os
import urllib3
from requests.exceptions import RequestException

# Подавляем предупреждения InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_target(target, output_file=None):
    try:
        # Проверяем основной URL, игнорируя HTTPS ошибки
        response = requests.get(target, timeout=5, verify=False)
        if response.status_code == 403:
            # Проверяем URL с /test, игнорируя HTTPS ошибки
            test_url = f"{target.rstrip('/')}/test"
            test_response = requests.get(test_url, timeout=5, verify=False)
            if test_response.status_code == 404:
                # Выводим только URL в консоль
                print(target)
                # Если указан output_file, сохраняем таргет в файл
                if output_file:
                    with open(output_file, 'a') as f:
                        f.write(target + '\n')
    except RequestException:
        # Игнорируем все сетевые ошибки, включая NameResolutionError
        pass

def main():
    parser = argparse.ArgumentParser(description='Check targets for specific response pattern')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='File containing target URLs')
    group.add_argument('-d', '--domain', help='Single target domain')
    parser.add_argument('-o', '--output', help='Output file for matching targets')

    args = parser.parse_args()

    # Если указан выходной файл, очищаем его
    if args.output and os.path.exists(args.output):
        os.remove(args.output)

    if args.file:
        try:
            with open(args.file, 'r') as f:
                # Читаем строки и удаляем дубликаты с помощью множества
                targets = list(set(line.strip() for line in f if line.strip()))
            for target in targets:
                check_target(target, args.output)
        except FileNotFoundError:
            pass  # Игнорируем ошибку, если файл не найден
    elif args.domain:
        check_target(args.domain, args.output)

if __name__ == "__main__":
    main()
