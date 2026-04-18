# Selenium Automation Project

Bu proje, grup çalışması için hazırlanmış başlangıç düzeyinde bir Python + Selenium + pytest otomasyon framework'üdür. Amaç; ortak bir temel yapı kurmak, Chrome ve Firefox desteğini hazır hale getirmek ve ekip arkadaşlarının arama, sonuç seçme ve assertion senaryolarını bu yapı üstüne ekleyebilmesini sağlamaktır.

---

## 🚀 Proje amacı ve kapsam

* Python, Selenium WebDriver ve pytest ile sade bir test otomasyon iskeleti sunar.
* Chrome ve Firefox browser desteği içerir.
* `sleep` kullanmaz, explicit wait yaklaşımını temel alır.
* Page Object Model (POM) yapısına uygundur.
* Ekip çalışmasına uygun modüler yapı sunar.

---

## 💻 Ön koşullar

* Python 3.11+
* Google Chrome
* Mozilla Firefox
* İnternet bağlantısı (Selenium Manager için)

---

## ⚙️ Kurulum

### Windows (PowerShell)

```bash
python --version
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📁 Proje yapısı

```text
selenium-automation-project/
├── README.md
├── requirements.txt
├── .gitignore
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   └── home_page.py          # (2. kişi ekledi)
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py
│   └── wait_helpers.py
└── tests/
    ├── conftest.py
    ├── test_smoke_setup.py
    └── test_home_navigation.py   # (2. kişi ekledi)
```

---

## 🧱 Framework bileşenleri

### driver_factory.py

* Chrome ve Firefox driver başlatır
* Selenium Manager kullanır

### wait_helpers.py

* Explicit wait fonksiyonları içerir
* visibility / clickable / presence

### base_page.py

* Ortak page metodları
* click, type, wait gibi işlemler

---

## 🆕 HomePage (2. kişi)

* Siteyi açar
* Sayfa yüklenmesini bekler (explicit wait)
* Title doğrulaması yapar

---

## 🧪 Testler

### Smoke test

```bash
pytest -v
```

### Chrome

```bash
pytest -v --browser chrome
```

### Firefox

```bash
pytest -v --browser firefox
```

---

## 🔍 Browser seçimi

* `chrome`
* `firefox`
* `all` (default)

---

## 🔄 Git workflow

* main → stabil
* feature/navigation → 2. kişi
* feature/search → 3. kişi
* feature/result-selection → 4. kişi

---

## 👨‍💻 2. kişinin yaptığı işler

* HomePage Page Object oluşturuldu
* Navigation (site açma) implemente edildi
* Explicit wait kullanıldı
* Title doğrulaması eklendi
* Testler Chrome + Firefox’ta çalıştırıldı

---

## 📈 Genişletme

* search_results_page.py eklenebilir
* ürün seçme akışı eklenebilir
* assertion standardı geliştirilebilir

---

## 📝 Yapılacaklar

* Search senaryosu (3. kişi)
* Result validation (4. kişi)
* Ortak assertion standardı
