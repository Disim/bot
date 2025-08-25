from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
    return ''.join(random.choice(characters) for _ in range(length)) + 'A1a!'

def setup_driver():
    """Настройка Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def click_login_button(driver):
    """Нажатие на кнопку Войти с различными стратегиями"""
    try:
        # Попытка 1: По ID (самый надежный способ)
        login_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, "validateButton"))
        )
        login_button.click()
        print("Кнопка найдена по ID")
        return True
        
    except TimeoutException:
        try:
            # Попытка 2: По тексту на кнопке
            login_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти')]"))
            )
            login_button.click()
            print("Кнопка найдена по тексту")
            return True
            
        except TimeoutException:
            try:
                # Попытка 3: По классу
                login_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.plain-button"))
                )
                login_button.click()
                print("Кнопка найдена по классу")
                return True
                
            except TimeoutException:
                try:
                    # Попытка 4: По type="submit" или type="button"
                    login_button = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' or @type='button']"))
                    )
                    login_button.click()
                    print("Кнопка найдена по type")
                    return True
                    
                except Exception as e:
                    print(f"Не удалось найти кнопку: {e}")
                    return False

def fill_login_form(driver, url, iterations=1):
    """Заполнение формы логина случайными данными"""
    try:
        driver.get(url)
        
        # Ждем загрузки страницы
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        for i in range(iterations):
            print(f"\nИтерация {i + 1}/{iterations}")
            
            # Обновляем страницу для новой попытки (кроме первой)
            if i > 0:
                driver.refresh()
                time.sleep(2)
            
            # Ждем появления полей ввода
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "login"))
                )
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "password"))
                )
            except TimeoutException:
                print("Поля ввода не найдены, пропускаем итерацию")
                continue
            
            # Генерируем случайные данные
            random_login = generate_random_login()
            random_password = generate_random_password()
            
            # Находим и заполняем поля ввода
            try:
                login_field = driver.find_element(By.ID, "login")
                password_field = driver.find_element(By.ID, "password")
                
                # Очищаем поля
                login_field.clear()
                password_field.clear()
                
                # Заполняем поля случайными данными
                login_field.send_keys(random_login)
                time.sleep(0.1)  # Небольшая пауза между вводом
                password_field.send_keys(random_password)
                
                print(f"Логин: {random_login}")
                print(f"Пароль: {random_password}")
                
                # Нажимаем на кнопку "Войти"
                if click_login_button(driver):
                    print("Кнопка 'Войти' нажата успешно!")
                    
                    # Ждем возможной реакции (перенаправление, сообщение об ошибке и т.д.)
                    time.sleep(2)
                    
                    # Проверяем, изменился ли URL (произошел ли вход)
                    current_url = driver.current_url
                    if "login" not in current_url.lower():
                        print(f"Возможно успешный вход! Новый URL: {current_url}")
                    else:
                        print("Вход не удался или остались на странице логина")
                
            except NoSuchElementException as e:
                print(f"Ошибка при поиске элементов: {e}")
            
            print("-" * 50)
            
            # Пауза между итерациями
            if i < iterations - 1:
                time.sleep(random.uniform(1, 3))  # Случайная пауза
                
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Оставляем браузер открытым для просмотра результата
        input("Нажмите Enter для закрытия браузера...")
        driver.quit()

def main():
    # URL для тестирования
    url = "https://rusdnevnik.com/login/"
    
    # Количество итераций заполнения
    iterations = 9999999999999999999  # Уменьшил для тестирования
    
    # Настраиваем и запускаем
    driver = setup_driver()
    fill_login_form(driver, url, iterations)

if __name__ == "__main__":
    main()