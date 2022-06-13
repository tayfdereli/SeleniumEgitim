import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class TestCheckFiltreCoffeShop(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get('https://filtrecoffeeshop.com/')
        self.driver.implicitly_wait(20)
        self.wait = WebDriverWait(self.driver, 10)

    def test_check_filtre_coffee_shop_login(self):
        self.driver.find_element(By.ID, '_desktop_user_info').click()
        self.driver.find_element(By.XPATH, '//ul//span[text()="Giris Yap"]').click()
        self.driver.find_element(By.NAME, 'email').send_keys('Selenium@testmail.com')
        self.driver.find_element(By.NAME, 'password').send_keys('SeleniumSessionTest123')
        self.driver.find_element(By.ID, 'submit-login').click()
        self.assertEqual('Kimlik doğrulama başarısız.', self.driver.find_element(By.CLASS_NAME, 'alert-danger').text)

        self.driver.find_element(By.NAME, 'email').clear()
        self.driver.find_element(By.NAME, 'email').send_keys('wabomej221@3dinews.com')
        self.driver.find_element(By.NAME, 'password').send_keys('SeleniumSessionTest123')
        self.driver.find_element(By.ID, 'submit-login').click()
        self.driver.find_element(By.ID, '_desktop_user_info').click()
        self.assertEqual('Selenium Session', self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '#header-menu-content .account span'))).text)

        self.driver.find_element(By.XPATH, '//a[contains(text(),"{}")]'.format('Kahvelerimiz')).click()
        self.assertIn('KAHVELERIMIZ', self.driver.find_element(By.CLASS_NAME, 'breadcrumb').text)
        self.assertEqual('KAHVELERIMIZ', self.driver.find_element(By.CSS_SELECTOR, 'li[itemprop]:last-child').text)

        self.driver.find_elements(By.CLASS_NAME, 'product-item')[0].click()
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, 'add-to-cart'))
        self.driver.find_element(By.CLASS_NAME, 'add-to-cart').click()
        self.assertIn('Ürün başarı ile sepete eklenmiştir', self.wait.until(EC.element_to_be_clickable(
            (By.ID, 'myModalLabel'))).text)
        self.driver.find_element(By.CSS_SELECTOR, '.cart-content-btn .btn-primary').click()

        self.assertEqual('ALIŞVERIŞ SEPETI', self.driver.find_element(By.TAG_NAME, 'h1').text)
        self.driver.find_element(By.CLASS_NAME, 'remove-from-cart').click()
        self.assertEqual('Sepetinizde ürün bulunmamaktadır.', self.driver.find_element(By.CLASS_NAME, 'no-items').text,
                         'Mesajın eşleşmedi')

    def tearDown(self):
        self.driver.quit()
