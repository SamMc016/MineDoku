import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


LOCALHOST = "http://127.0.0.1:5000"


class SeleniumTests(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        self.driver.quit()

    def test_login_page_loads(self):
        self.driver.get(f"{LOCALHOST}/login")

        title = self.driver.find_element(By.TAG_NAME, "h2")

        self.assertEqual(title.text, "Login")
    
    def test_signup_page_loads(self):
        self.driver.get(f"{LOCALHOST}/signup")

        title = self.driver.find_element(By.TAG_NAME, "h2")

        self.assertEqual(title.text, "Sign Up")

    def test_login_to_signup_navigation(self):
        self.driver.get(f"{LOCALHOST}/login")

        signup_link = self.driver.find_element(By.LINK_TEXT, "Sign up!")
        signup_link.click()

        title = self.driver.find_element(By.TAG_NAME, "h2")

        self.assertEqual(title.text, "Sign Up")

    def test_login_back_to_game_button(self):
        self.driver.get(f"{LOCALHOST}/login")

        back_button = self.driver.find_element(By.CLASS_NAME, "btn")
        back_button.click()

        self.assertIn("/", self.driver.current_url)