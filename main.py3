import sys
from typing import List, Dict
from collections import Counter

def parse_log_line(line: str) -> Dict[str, str]:
    """
    Парсить рядок логу у словник з ключами: date, time, level, message.
    Формат рядка: "2024-01-22 08:30:01 INFO User logged in successfully."
    """
    parts = line.strip().split(' ', 3)  # Розділяємо на 4 частини: дата, час, рівень, повідомлення
    if len(parts) < 4:
        raise ValueError(f"Неправильний формат рядка логу: {line}")
    return {
        'date': parts[0],
        'time': parts[1],
        'level': parts[2].upper(),
        'message': parts[3]
    }

def load_logs(file_path: str) -> List[Dict[str, str]]:
    """
    Зчитує лог-файл і повертає список розпарсених записів.
    """
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    try:
                        log_entry = parse_log_line(line)
                        logs.append(log_entry)
                    except ValueError as ve:
                        # Можна записати або пропустити рядки з помилками
                        print(f"Пропускаємо рядок через помилку: {ve}", file=sys.stderr)
        return logs
    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Помилка при читанні файлу: {e}", file=sys.stderr)
        sys.exit(1)

def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    """
    Фільтрує логи за рівнем (case-insensitive).
    """
    level = level.upper()
    return list(filter(lambda log: log['level'] == level, logs))

def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Підраховує кількість записів для кожного рівня логування.
    """
    levels = [log['level'] for log in logs]
    return dict(Counter(levels))

def display_log_counts(counts: Dict[str, int]) -> None:
    """
    Виводить таблицю з кількістю записів для кожного рівня.
    """
    print(f"{'Рівень логування':<15} | {'Кількість':<8}")
    print('-'*15 + '-|-' + '-'*8)
    for level, count in sorted(counts.items()):
        print(f"{level:<15} | {count:<8}")

def display_logs(logs: List[Dict[str, str]], level: str) -> None:
    """
    Виводить деталі логів для певного рівня.
    """
    if logs:
        print(f"\nДеталі логів для рівня '{level.upper()}':")
        for log in logs:
            print(f"{log['date']} {log['time']} - {log['message']}")

def main():
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях_до_файлу_логу> [рівень_логування]", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    filter_level = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if filter_level:
        filtered_logs = filter_logs_by_level(logs, filter_level)
        display_logs(filtered_logs, filter_level)


if __name__ == "__main__":
    main()