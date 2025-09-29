# expass - Password Strength Tester CLI

**expass** - удобная командная утилита для оценки надёжности паролей.  
Она вычисляет энтропию, оценивает время brute-force при разных скоростях,  
проверяет пароль по локальному словарю и по базе утечек *Have I Been Pwned* (k-Anonymity).

---

## ✨ Возможности
- Интерактивный ввод пароля (**скрытый**) - безопасный режим.
- Подсчёт энтропии (в битах).
- Оценка времени brute-force при разных скоростях перебора.
- Проверка по списку распространённых паролей (пользовательский словарь).
- Проверка утечек через HIBP (`--check-hibp`, требует интернет).

---

## 🚀 Быстрая установка и запуск

> ⚠️ Внимание: **не** передавайте пароль в командной строке (например `expass --password "..."`) — он попадёт в историю shell и может быть виден в списке процессов. Всегда предпочтительнее `--interactive`.

### Linux / macOS
```bash
# 1) Клонируем репозиторий и переходим в папку
git clone https://github.com/ExTallentt88/expass-cli.git
cd expass-cli

# 2) Создаём и активируем виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 3) Устанавливаем зависимости и ставим пакет в editable-режиме
python -m pip install --upgrade pip setuptools
pip install -r requirements.txt
pip install -e .

# 4) Запуск (интерактивный ввод пароля)
expass --interactive

# 5) Пример с HIBP (потребуется интернет)
expass --interactive --check-hibp
