import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


@pytest.fixture(scope="module")
def driver():
    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope="module")
def authenticated_driver(driver):
    # Открываем страницу авторизации
    driver.get('https://www.saucedemo.com/')

    # Авторизуемся
    username_input = driver.find_element(By.XPATH, "//input[@placeholder='Username']")
    password_input = driver.find_element(By.XPATH, "//input[@placeholder='Password']")

    username_input.send_keys('standard_user')
    password_input.send_keys('secret_sauce')
    sleep(1)

    login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
    login_button.click()


    sleep(2)
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"


    return driver


def test_open(authenticated_driver):

    assert authenticated_driver.current_url == "https://www.saucedemo.com/inventory.html"


def test_add_to_cart(authenticated_driver):
    # Работаем с авторизованным драйвером
    add_cart_button = authenticated_driver.find_element(By.XPATH, "//button[@name='add-to-cart-sauce-labs-backpack']")
    add_cart_button.click()

    sleep(1)

    move_in_cart = authenticated_driver.find_element(By.XPATH, "//a[@class='shopping_cart_link']")
    move_in_cart.click()

    cart_backpack = authenticated_driver.find_element(By.XPATH, "//*[text()='Sauce Labs Backpack']")

    assert cart_backpack.text == 'Sauce Labs Backpack'


def test_open_menu(authenticated_driver):

    menu_button = authenticated_driver.find_element(By.XPATH, "//button[@id='react-burger-menu-btn']")
    menu_button.click()
    sleep(1)
    link_in_menu = authenticated_driver.find_element(By.XPATH, "//a[@id='inventory_sidebar_link']")

    assert link_in_menu.text == "All Items"


def test_go_to_about(authenticated_driver):

    #menu_button = authenticated_driver.find_element(By.XPATH, "//button[@id='react-burger-menu-btn']")
    #menu_button.click()
    sleep(1)

    about_link_menu = authenticated_driver.find_element(By.XPATH, "//a[@id='about_sidebar_link']")
    about_link_menu.click()
    sleep(2)

    assert authenticated_driver.current_url == "https://saucelabs.com/"