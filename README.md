
# expass — Password Strength Tester CLI

**expass** — удобная командная утилита для оценки надёжности паролей.
Она вычисляет энтропию, оценивает время brute-force при разных скоростях,
проверяет пароль по локальному словарю и по Have I Been Pwned (k-Anonymity).

## Возможности
- Интерактивный ввод пароля (скрыто) — рекомендуемый режим.
- Оценка энтропии (в битах) и примерное время перебора при нескольких скоростях.
- Проверка по списку распространённых паролей (пользовательский словарь).
- Проверка утечек через HIBP (опция `--check-hibp`, требует интернет).

## Быстрая установка (локально, venv)
```bash
# распакуй архив и перейди в папку проекта
cd expass_password_checker
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools
pip install -r requirements.txt
# установить как команда expass (editable)
pip install -e .

# запустить (интерактивно -- ввод пароля скрыт):
expass --interactive

# или (не рекомендуется: пароль будет в истории shell):
expass --password "MyP@ssw0rd!" --check-hibp
```

## Установка глобально (для всех пользователей)
```bash
# осторожно: установка с sudo изменит системный Python-packages
sudo python3 -m pip install .
```

## Без установки: запуск модуля напрямую
```bash
# из корня проекта
python -m src.pwcheck --interactive
```

## Советы по безопасности
- **НЕ** передавай пароль в командной строке — используй `--interactive` или stdin.
- HIBP использует k-Anonymity (отправляет только SHA1-префикс), но всё равно требует интернет.
- Не запускай под `sudo`, если нет необходимости.

## Файлы в проекте
- `src/` — исходники пакета `pwcheck`
- `requirements.txt` — зависимости
- `setup.py` — для установки/entry-point `expass`
- `run.sh` — удобный wrapper для запуска
- `README.md`, `LICENSE`

## Лицензия
MIT
