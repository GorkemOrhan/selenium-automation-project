# Selenium Automation Project

Bu proje, grup çalışması için hazırlanmış başlangıç düzeyinde bir Python + Selenium + pytest otomasyon framework'üdür. Amaç; ortak bir temel yapı kurmak, Chrome ve Firefox desteğini hazır hale getirmek ve ekip arkadaşlarının arama, sonuç seçme ve assertion senaryolarını bu yapı üstüne ekleyebilmesini sağlamaktır.

## Proje amacı ve kapsam

- Python, Selenium WebDriver ve pytest ile sade bir test otomasyon iskeleti sunar.
- Chrome ve Firefox browser desteği içerir.
- `sleep` kullanmaz, explicit wait yaklaşımını temel alır.
- Page Object yapısına uygun genişletilebilir bir temel sağlar.
- GitHub üzerinde ekipçe çalışmaya uygun klasör düzeni içerir.

## macOS ön koşulları

- Python 3.11 veya üzeri yüklü olmalı.
- Google Chrome kurulu olmalı.
- Mozilla Firefox kurulu olmalı.
- Terminal üzerinden `python3` komutu çalışmalı.
- İlk Selenium çalıştırmasında Selenium Manager driver çözümlemesi için internet erişimi gerekebilir.

## Kurulum adımları

1. Proje klasörüne girin.
2. Python sürümünü kontrol edin.
3. Sanal ortam oluşturun.
4. Sanal ortamı aktive edin.
5. `pip` sürümünü güncelleyin.
6. Bağımlılıkları yükleyin.

## Terminal komutları

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -v
pytest -v --browser chrome
pytest -v --browser firefox
```

## Proje klasör yapısı

```text
selenium-automation-project/
├── README.md
├── requirements.txt
├── .gitignore
├── pages/
│   ├── __init__.py
│   └── base_page.py
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py
│   └── wait_helpers.py
└── tests/
    ├── conftest.py
    └── test_smoke_setup.py
```

## Framework yapısı

### `utils/driver_factory.py`

- Browser adına göre Chrome veya Firefox driver başlatır.
- Selenium Manager sayesinde ekstra driver paketi gerektirmez.
- Sayfa yükleme timeout'unu ayarlar.
- Uygun olduğunda pencereyi büyütmeye çalışır.

### `utils/wait_helpers.py`

- Explicit wait fonksiyonlarını merkezi olarak toplar.
- Görünürlük, tıklanabilirlik ve DOM içinde var olma beklemeleri içerir.

### `pages/base_page.py`

- Ortak page metodlarını barındırır.
- Yeni page class'ları bu sınıftan türetilebilir.

### `tests/conftest.py`

- `pytest` için ortak fixture'ları tanımlar.
- `--browser` parametresi ile testlerin hangi browser'da çalışacağını belirler.
- Varsayılan olarak testleri hem Chrome hem Firefox üzerinde koşturur.

### `tests/test_smoke_setup.py`

- Framework kurulumunu doğrulayan temel smoke testtir.
- Hepsiburada ana sayfasını açar.
- Sayfa başlığının boş olmadığını kontrol eder.

## Testleri çalıştırma

Tüm browser'larda çalıştırmak için:

```bash
pytest -v
```

Sadece Chrome için:

```bash
pytest -v --browser chrome
```

Sadece Firefox için:

```bash
pytest -v --browser firefox
```

Hem Chrome hem Firefox için açık şekilde belirtmek isterseniz:

```bash
pytest -v --browser all
```

## Browser seçme mantığı

- `--browser chrome`: yalnızca Chrome çalışır.
- `--browser firefox`: yalnızca Firefox çalışır.
- `--browser all`: aynı test seti iki browser'da da çalışır.
- Parametre verilmezse varsayılan değer `all` olur.

## GitHub branch önerileri

- Ana branch: `main`
- Framework kurulumu için: `feature/framework-setup`
- Arama senaryoları için: `feature/search`
- Sonuç seçme akışı için: `feature/result-selection`
- Assertion ve doğrulama işleri için: `feature/assertions`

Önerilen akış:

1. Her ekip üyesi kendi feature branch'i üzerinde çalışsın.
2. Tamamlanan iş için pull request açılsın.
3. Kod incelemesi sonrası `main` branch'ine merge yapılsın.
4. Ortak framework dosyalarında değişiklik yaparken çakışma riskine dikkat edilsin.

## Genişletme önerisi

- `pages/` klasörü içine `home_page.py`, `search_results_page.py` gibi yeni page object dosyaları eklenebilir.
- Ortak locator ve yardımcı metodlar gerektiğinde `BasePage` içinde büyütülebilir.
- İleride `pytest.ini`, logging, screenshot alma ve CI entegrasyonu eklenebilir.

## Yapılacaklar

- Hepsiburada ana sayfası için ilk gerçek page object sınıfını ekleyin.
- Arama kutusu ve arama sonucu akışını ayrı test senaryolarına bölün.
- Assertion yapısını ekip içinde ortak bir standarda bağlayın.
