import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.maximize_window()
    yield driver
    driver.quit()


def test_show_my_pets(driver):
    wdw(driver, 20).until(EC.presence_of_element_located((By.ID, 'email')))
    driver.find_element(By.ID, 'email').send_keys('_______')
    # вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('________')
    # нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'PetFriends'
    time.sleep(1)
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()
    time.sleep(2)
    # Проверяем количество питомцев
    pets_num = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    assert int(pets_num) == len(pets_count)

    images = driver.find_elements(By.XPATH, '//img[@class="card-img-top"]')
    names = driver.find_elements(By.XPATH,'//h5[@class="card-title"]')
    descriptions = driver.find_elements(By.XPATH,'//p[@class="card-text"]')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

def test_show_all_my_petty(driver):
    # Активируем неявные ожидания
    driver.implicitly_wait(10)
    # авторизуемся на сайте:
    driver.find_element(By.ID, 'email').send_keys('______')
    driver.find_element(By.ID, 'pass').send_keys('______')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    wdw(driver, 10).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))

    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
    data_my_pets = driver.find_elements(By.CSS_SELECTOR, 'tbody>tr')

    # Ожидаем, что данные всех питомцев видны на странице:
    for i in range(len(data_my_pets)):
        assert wdw(driver, 5).until(EC.visibility_of(data_my_pets[i]))

    # Ищем в таблице все фотографии питомцев и они видны на странице:
    image_my_pets = driver.find_elements(By.CSS_SELECTOR, 'img[style="max-width: 100px; max-height: 100px;"]')
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            assert wdw(driver, 5).until(EC.visibility_of(image_my_pets[i]))

    # Ищем в теле таблицы все имена питомцев:
    name_my_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    for i in range(len(name_my_pets)):
        assert wdw(driver, 5).until(EC.visibility_of(name_my_pets[i]))

    # Ищем в теле таблицы все породы питомцев:
    type_my_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
    for i in range(len(type_my_pets)):
        assert wdw(driver, 5).until(EC.visibility_of(type_my_pets[i]))

    # Ищем в теле таблицы все данные о возрасте питомцев:
    age_my_pets = driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
    for i in range(len(age_my_pets)):
        assert wdw(driver, 5).until(EC.visibility_of(age_my_pets[i]))

    all_statistics = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split("\n")
    statistics_pets = all_statistics[1].split(" ")
    all_my_pets = int(statistics_pets[-1])
    assert len(data_my_pets) == all_my_pets

    # Проверяем, что хотя бы у половины питомцев есть фото:
    m = 0
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            m += 1
    assert m >= all_my_pets / 2

    # Проверяем, что у всех питомцев есть имя:
    for i in range(len(name_my_pets)):
        assert name_my_pets[i].text != ''

    # Проверяем, что у всех питомцев есть порода:
    for i in range(len(type_my_pets)):
        assert type_my_pets[i].text != ''

    # Проверяем, что у всех питомцев есть возраст:
    for i in range(len(age_my_pets)):
        assert age_my_pets[i].text != ''

    # Проверяем, что у всех питомцев разные имена:
    list_name_my_pets = []
    for i in range(len(name_my_pets)):
        list_name_my_pets.append(name_my_pets[i].text)
    set_name_my_pets = set(list_name_my_pets)
    assert len(list_name_my_pets) == len(set_name_my_pets)

    # Проверяем, что в списке нет повторяющихся питомцев:
    list_data_my_pets = []
    for i in range(len(data_my_pets)):
        list_data = data_my_pets[i].text.split("\n")
        list_data_my_pets.append(list_data[0])
    set_data_my_pets = set(list_data_my_pets)
    assert len(list_data_my_pets) == len(set_data_my_pets)

