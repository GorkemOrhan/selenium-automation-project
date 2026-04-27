# Selenium Automation Project

Bu proje, Python tabanli bir Selenium UI test otomasyon iskeletidir. `pytest` ile calisir, `Page Object Model (POM)` yapisini izler ve Chrome ile Firefox uzerinde temel web senaryolari kosturmak icin hazir bir temel sunar.

Mevcut durumda proje, Hepsiburada ana sayfasina yonelik smoke, navigation ve arama akisi testleri icerir. Amac; ekip calismasinda buyutulebilecek sade, okunabilir ve tekrar kullanilabilir bir framework olusturmaktir.

## Ozet

- Python + Selenium WebDriver + pytest kullanir
- Chrome ve Firefox destegi vardir
- `sleep` yerine explicit wait yaklasimi kullanilir
- POM yapisiyla sayfa davranislari testlerden ayrilir
- Yeni test ve page object eklemeye uygun moduler klasor yapisi sunar

## Kullanilan Teknolojiler

- Python 3.11+
- Selenium 4
- pytest 8+
- pytest-rerunfailures 16+

## Proje Yapisi

```text
selenium-automation-project/
|-- README.md
|-- requirements.txt
|-- pages/
|   |-- __init__.py
|   |-- base_page.py
|   `-- home_page.py
|-- utils/
|   |-- __init__.py
|   |-- driver_factory.py
|   `-- wait_helpers.py
`-- tests/
    |-- conftest.py
    |-- test_smoke_setup.py
    |-- test_home_navigation.py
    `-- test_search_flow.py
```

## Klasorler Ne Ise Yarar

### `pages/`

Sayfaya ozel davranislar burada tutulur.

- `base_page.py`: Ortak Selenium yardimcilari bulunur
- `home_page.py`: Ana sayfa acma, yuklenme bekleme ve title kontrolu gibi akislari icerir

### `utils/`

Tekrar kullanilan altyapi yardimcilari burada yer alir.

- `driver_factory.py`: Browser tipine gore WebDriver olusturur
- `wait_helpers.py`: Explicit wait fonksiyonlarini saglar

### `tests/`

Pytest testleri ve fixture tanimlari burada bulunur.

- `conftest.py`: `driver`, `base_url`, `--browser` parametresini ve cookie banner kapatma fixture'ini tanimlar
- `test_smoke_setup.py`: Sayfa title'inin bos gelmedigini kontrol eden temel smoke testi
- `test_home_navigation.py`: Ana sayfa navigation ve title dogrulamasi yapan test
- `test_search_flow.py`: Arama kutusu ile urun arama akisini test eden senaryo

## Kurulum

### Windows PowerShell

```powershell
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

## Gereksinimler

- Python 3.11 veya ustu
- Google Chrome ve/veya Mozilla Firefox
- Internet baglantisi

Not: Selenium 4 ile birlikte Selenium Manager kullanildigi icin cogu durumda driver binary dosyalarini manuel indirmeniz gerekmez.

## Testleri Calistirma

Tum testleri varsayilan browser secimiyle calistirmak icin:

```bash
pytest -v
```

Sadece Chrome icin:

```bash
pytest -v --browser chrome
```

Sadece Firefox icin:

```bash
pytest -v --browser firefox
```

Tum desteklenen browser'larda ayni testleri kosturmak icin:

```bash
pytest -v --browser all
```

Flaky testleri otomatik yeniden calistirmak icin:

```bash
pytest -v --browser all --reruns 3 --reruns-delay 1
```

## Browser Secim Mantigi

Proje `pytest` custom argument yapisi kullanir:

- `chrome`: Testler sadece Chrome uzerinde calisir
- `firefox`: Testler sadece Firefox uzerinde calisir
- `all`: Her test hem Chrome hem Firefox icin parametrize edilir

Varsayilan deger `all` oldugu icin `pytest -v` komutu her iki browser'i da hedefler.

## Mevcut Test Senaryolari

### 1. Smoke Setup Testi

`tests/test_smoke_setup.py`

Bu test:

- Browser'i acar
- Hepsiburada ana sayfasina gider
- Sayfa title bilgisinin bos olmadigini dogrular

### 2. Home Navigation Testi

`tests/test_home_navigation.py`

Bu test:

- Ana sayfayi acar
- Title icinde `Hepsiburada` gecene kadar bekler
- Sayfanin beklenen sekilde yuklendigini dogrular

### 3. Search Flow Testi

`tests/test_search_flow.py`

Bu test:

- Ana sayfayi acar ve cookie banner'ini kapatir
- Arama kutusuna urun adi yazar ve arama yapar
- URL'nin arama sonuc sayfasina yonlendigini dogrular
- Birden fazla keyword ile parametrize testler icerir (`telefon`, `laptop`, `kulaklık`)
- Chrome ve Firefox uzerinde calisir

Teknik notlar:

- Hepsiburada cookie banner'i Shadow DOM (`efilli-layout-dynamic`) icinde oldugu icin JavaScript ile kapatilir
- Arama kutusu onundeki wrapper div nedeniyle `ActionChains` kullanilir
- Firefox render timing farkindan kaynaklanan flaky durumlar `pytest-rerunfailures` ile yonetilir

### 4. Arama Sonucu Dogrulama Testi

`tests/test_search_result.py`

> **Not:** Bu senaryo gelistirilme asamasindadir.

Bu test:

- Arama yapildiktan sonra sonuc sayfasinin yuklendigini dogrular
- Sonuc listesindeki ilk urunu bulur ve gorunur oldugunu kontrol eder (`result.is_displayed()`)
- Test tamamlandiktan sonra driver'i kapatir (`driver.quit()`)

## Framework Davranisi

### Driver yonetimi

`utils/driver_factory.py` dosyasi secilen browser'a gore ilgili WebDriver'i olusturur:

- `chrome` icin `webdriver.Chrome()`
- `firefox` icin `webdriver.Firefox()`

Ayrica:

- Sayfa yuklenme zaman asimi `30` saniye olarak ayarlanir
- Mumkun oldugunda pencere maximize edilir
- Chrome ve Firefox'ta bildirim izin popup'lari varsayilan olarak devre disi birakilir

### Wait yaklasimi

`utils/wait_helpers.py` icindeki yardimcilar explicit wait kullanir:

- `wait_for_visibility`
- `wait_for_clickable`
- `wait_for_presence`
- `wait_for_url_to_contain`

Varsayilan timeout degeri `10` saniyedir.

### Base Page

`pages/base_page.py` ortak Selenium islemlerini merkezilestirir:

- `open`
- `find_visible`
- `find_clickable`
- `find_present`
- `click`
- `type_text`
- `get_text`
- `get_title`
- `current_url`
- `wait_for_url_to_contain`

Bu yapi sayesinde testler daha okunabilir kalir ve locator/etkilesim mantigi page object katmaninda toplanir.

### Cookie Banner Yonetimi

Hepsiburada cookie banner'i Shadow DOM icinde yuklenir. `conftest.py` icindeki `handle_popup` fixture'i her test oncesinde otomatik olarak calisir ve banner'i JavaScript ile kapatir:

```python
document.querySelector('efilli-layout-dynamic')
    .shadowRoot.querySelector('#hb-accept-all').click()
```

## Yeni Test veya Page Object Ekleme

Projeyi buyutmek icin tipik akis su sekildedir:

1. `pages/` altina yeni bir page object ekleyin
2. Sayfaya ozel locator ve davranislari bu dosyada toplayin
3. `tests/` altinda yeni pytest dosyasi olusturun
4. Testte page object'i kullanarak senaryoyu yazin
5. Gerekiyorsa ortak helper'lari `utils/` altina ekleyin

## Faydali Notlar

- Testler gercek browser acarak calisir
- UI testleri, site tasarimi veya title davranisi degistiginde guncelleme gerektirebilir
- Bu iskelet, ileri seviyede raporlama, screenshot alma, logging veya CI entegrasyonu ile genisletilebilir

## Gelistirme Fikirleri

Ileride su iyilestirmeler eklenebilir:

- Ortam bazli `base_url` yonetimi
- `.env` veya config yapisi
- Screenshot capture on failure
- HTML test report
- CI/CD entegrasyonu
- Locator sabitlerinin daha sistematik yonetimi

## Lisans

Bu repo icin lisans bilgisi tanimli degilse, ihtiyaca gore bir `LICENSE` dosyasi eklenebilir.