
# Zarządzanie Subskrypcjami

Aplikacja webowa służąca do zarządzania subskrypcjami oraz monitorowania wydatków związanych z usługami abonamentowymi.

## Funkcjonalności

* rejestracja i logowanie użytkowników,
* zarządzanie subskrypcjami,
* zarządzanie metodami płatności,
* rejestrowanie płatności,
* śledzenie terminów odnowienia subskrypcji,
* generowanie raportów wydatków,
* powiadomienia o zbliżających się płatnościach,
* panel administracyjny Django.

## Technologie

### Backend

* Python 3.13
* Django
* Django REST Framework
* PostgreSQL

### Frontend

* React
* Vite

Backend aplikacji został zaimplementowany w Django oraz Django REST Framework, natomiast interfejs użytkownika przygotowano w React i osadzono bezpośrednio w aplikacji Django.

---

# Instalacja

## Wymagania

* Python **3.13.5** lub nowszy
* PostgreSQL **17** lub nowszy

## Konfiguracja

Przed uruchomieniem aplikacji utwórz w katalogu projektu plik `.env`:

```env
SECRET_KEY=twoj_sekretny_klucz
DEBUG=True

DB_NAME=nazwabazy
DB_USER=nazwauzytkownika
DB_PASSWORD=haslo
DB_HOST=localhost
DB_PORT=5432

ACCESS_TOKEN_LIFETIME_MIN=15
REFRESH_TOKEN_LIFETIME_DAYS=7
```

## 1. Utworzenie środowiska wirtualnego

```bash
python -m venv venv
```

## 2. Aktywacja środowiska

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 3. Instalacja zależności

```bash
pip install -r requirements.txt
```

---

# Inicjalizacja bazy danych

## Wykonanie migracji

```bash
python manage.py migrate
```

## Utworzenie danych początkowych

```bash
python manage.py seed
```

Komenda utworzy:

* podstawowe platformy,
* konto administratora.

## Domyślne konto administratora

```text
Login: admin
Email: admin@test.com
Hasło: admin123
```

---

# Uruchomienie aplikacji

```bash
python manage.py runserver
```

Po uruchomieniu aplikacja będzie dostępna pod adresem:

```text
http://127.0.0.1:8000/
```

## API

Endpointy API są dostępne pod adresem:

```text
http://127.0.0.1:8000/api/v1/
```
