# s31404-to-do-app

Aplikacja typu to-do z logowaniem, rejestracją i zapisem danych w MongoDB. Użytkownik może dodawać zadania z datą i kolorem, a także oznaczać je jako wykonane.

## Instrukcja uruchomienia

1. Sklonuj repo
```bash
git clone https://github.com/katriniix/s31404-to-do-app.git
cd s31404-to-do-app
```
2. Zainstaluj requirements.txt
```bash
pip install -r requirements.txt
```
3. Utwórz plik .env na podstawie .env.example i wprowadź swój URI do MongoDB Atlas
```bash
cp .env.example .env
```
4. Uruchom aplikację 
```bash
python main.py
```

## Uruchomienie w Dockerze

1. Zbuduj i uruchom kontener
```bash
docker build -t to-do-app .
docker run -p 5000:5000 to-do-app
```
2. Otwórz w przeglądarce
```bash
http://localhost:5000
```

## Testowanie

1. Uruchom testy jednostkowe
```bash
pytest -q
```

