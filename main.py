from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import string
import time

def generate_random_login():
    """Генерация случайного логина (телефон/email/СНИЛС)"""
    choice = random.randint(1, 3)
    
    if choice == 1:  # Телефон
        return f"+7{random.randint(900, 999)}{random.randint(1000000, 9999999)}"
    elif choice == 2:  # Email
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        domain = random.choice(['gmail.com', 'yandex.ru', 'mail.ru', 'rambler.ru'])
        return f"{username}@{domain}"
    else:  # СНИЛС
        part1 = random.randint(100, 999)
        part2 = random.randint(100, 999)
        part3 = random.randint(100, 999)
        control = random.randint(10, 99)
        return f"{part1:03d}-{part2:03d}-{part3:03d} {control:02d}"

def generate_random_password(length=12):
    """Генерация случайного пароля"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def setup_driver():
    """Настройка Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def fill_login_form(driver, url, iterations=1):
    """Заполнение формы логина случайными данными"""
    try:
        driver.get(url)
        
        # Ждем загрузки страницы
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login"))
        )
        
        for i in range(iterations):
            print(f"Итерация {i + 1}/{iterations}")
            
            # Генерируем случайные данные
            random_login = generate_random_login()
            random_password = generate_random_password()
            
            # Находим поля ввода
            login_field = driver.find_element(By.ID, "login")
            password_field = driver.find_element(By.ID, "password")
            
            # Очищаем поля (если нужно заполнять несколько раз)
            login_field.clear()
            password_field.clear()
            
            # Заполняем поля случайными данными
            login_field.send_keys(random_login)
            password_field.send_keys(random_password)
            
            print(f"Логин: {random_login}")
            print(f"Пароль: {random_password}")
            print("-" * 50)
            
            # Небольшая пауза между итерациями
            if i < iterations - 1:
                time.sleep(0)
                
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Оставляем браузер открытым для просмотра результата
        input("Нажмите Enter для закрытия браузера...")
        driver.quit()

def main():
    # URL вашей HTML-страницы (можно сохранить HTML в файл и указать путь)
    # Например: "file:///path/to/your/file.html"
    url = "https://rusdnevnik.com/login/"  # Замените на актуальный путь
    
    # Или если страница в интернете:
    # url = "https://ваш-сайт.ru"
    
    # Количество итераций заполнения
    iterations = 999999
    
    # Настраиваем и запускаем
    driver = setup_driver()
    fill_login_form(driver, url, iterations)

if __name__ == "__main__":
    main()