import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


def pytest_addoption(parser):
    # Опция для выбора браузера
    parser.addoption(
        "--browser_name",
        action="store",
        default="firefox",
        help="Choose browser: chrome or firefox"
    )
    # pytest --browser_name=chrome --language=es test_items.py  - команда для запуска тестов)

    parser.addoption(
        "--language",
        action="store",
        default="en",  # Установлено значение по умолчанию
        help="Choose language: es., en, ru, fr, etc."
    )


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")

    if browser_name == "firefox":
        print("\nstart firefox browser for test..")
        profile = FirefoxProfile()
        profile.set_preference("intl.accept_languages", user_language)
        options = FirefoxOptions()
        options.profile = profile
        browser = webdriver.Firefox(options=options)

    elif browser_name == "chrome":
        print("\nstart chrome browser for test..")
        options = ChromeOptions()
        options.add_argument(f"--lang={user_language}")
        browser = webdriver.Chrome(options=options)

    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    yield browser
    print("\nquit browser..")
    browser.quit()
