import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

LOCALHOST = "http://127.0.0.1:5000"

class SeleniumTests(unittest.TestCase):

    def setUp(self): # Creates a new instance of the Google Chrome browser
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=options)

    def tearDown(self): # Destroys the previously created instance of Chrome so that it can be set back up safely
        self.driver.quit()


    """ SYSTEM TEST #1: TESTS THAT THE LOGIN PAGE LOADS CORRECTLY """
    def test_login_page_loads(self):
        self.driver.get(f"{LOCALHOST}/login") 
        title = self.driver.find_element(By.TAG_NAME, "h2") # Finds the text inside the h2 tag

        self.assertEqual(title.text, "Login",  "<h2> tag in login page should be Login")
    

    """ SYSTEM TEST #2: TESTS THAT THE SIGNUP PAGE LOADS CORRECTLY """
    def test_signup_page_loads(self):
        self.driver.get(f"{LOCALHOST}/signup")
        title = self.driver.find_element(By.TAG_NAME, "h2") # Finds the text inside the h2 tag

        self.assertEqual(title.text, "Sign Up",  "<h2> tag in signup page should be Signup")


    """ SYSTEM TEST #3: TESTS THAT NAVIGATION FROM LOGIN TO SIGNUP WORKS """
    def test_login_to_signup_navigation(self):
        self.driver.get(f"{LOCALHOST}/login")
        signup_link = self.driver.find_element(By.LINK_TEXT, "Sign up!") # Finds the hyperlink for the signup page on the login page and clicks it
        signup_link.click()

        title = self.driver.find_element(By.TAG_NAME, "h2")

        self.assertEqual(title.text, "Sign Up", "Should be on the signup page and <h2> tag in signup page should be Signup")


    """ SYSTEM TEST #4: TESTS THAT NAVIGATION FROM LOGIN TO GAME WORKS """
    def test_login_back_to_game_button(self):
        self.driver.get(f"{LOCALHOST}/login")
        back_button = self.driver.find_element(By.CLASS_NAME, "btn") # Finds the button for the puzzle page on the login page and clicks it
        back_button.click()

        self.assertIn("/", self.driver.current_url, "Should be on the game page and current url should be /")


    """ SYSTEM TEST #5: TESTS THAT GIVE UP BUTTON CHANGES WHEN PRESSED """
    def test_give_up_button_colour_change(self):
        self.driver.get(f"{LOCALHOST}/")
        give_up_btn = self.driver.find_element(By.ID, "give-up") # Finds the give up button and clicks it 
        give_up_btn.click()

        green_rgba = "rgba(59, 177, 67, 1)" # Expected colour it should change to 
        button_text = give_up_btn.text 

        try: 
            WebDriverWait(self.driver, 5).until( # Prevents previous timeout errors 
                lambda d: green_rgba in give_up_btn.value_of_css_property("background-color")
            )
        except TimeoutException:
            actual_colour = give_up_btn.value_of_css_property("background-color")
            self.fail(f"Button never turned green. Stayed at: {actual_colour}") # fails if the button doesnt change colour
        
        button_colour = give_up_btn.value_of_css_property("background-color") 

        self.assertIsNotNone(button_colour, "Button should not have no colour")
        self.assertIn(green_rgba, button_colour, "Button should be green")
        self.assertEqual(button_text, "View Results?", "Button text should no longer be 'Give Up?'")


    """ SYSTEM TEST #6: TESTS THAT VIEW RESULTS REDIRECTS TO THE CORRECT PAGE """
    def test_results_button_redirect(self):
        self.driver.get(f"{LOCALHOST}/")
        give_up_btn = self.driver.find_element(By.ID, "give-up") # Finds the give up button 

        give_up_btn.click() # clicks the button twice
        give_up_btn.click()
    
        WebDriverWait(self.driver, 5).until(expected_conditions.url_contains("/end_game"))
        self.assertIn("/end_game", self.driver.current_url, "Redirect should go to end game page")


    """ SYSTEM TEST #7: TESTS THAT CLICKING ON A SQUARE BRINGS UP THE INVENTORY PANEL """
    def test_inventory_panel_appear(self):
        self.driver.get(f"{LOCALHOST}/")
        square = self.driver.find_element(By.ID, "1") # Finds top left square of gameboard and clicks it 
        square.click()
        inventory_panel = self.driver.find_element(By.ID, "inventory-overlay") # Finds the inventory panel full of blocks
        block = self.driver.find_element(By.CLASS_NAME, "inventory-grid") # Finds the first block in the grid of blocks

        self.assertTrue(inventory_panel.is_displayed(), "Inventory panel should appear")
        self.assertIsNotNone(block, "A block should occupy the grid space")


    """ SYSTEM TEST #8: TESTS THAT CLICKING ON A SQUARE AND PLACING A BLOCK WORKS """
    def test_place_block(self):
        self.driver.get(f"{LOCALHOST}/")
        square = self.driver.find_element(By.ID, "1") # Finds top left square of gameboard and clicks it
        square.click() 

        durability_element = self.driver.find_element(By.ID, "durability-score")
        initial_durability = int(durability_element.text.split("/")[0])

        inventory_panel = self.driver.find_element(By.ID, "inventory-overlay") # Finds the inventory panel 
        self.assertTrue(inventory_panel.is_displayed(), "Inventory panel should appear")
        block_to_place = self.driver.find_element(By.CSS_SELECTOR, "[data-block-id='1']") # Finds the first block in the grid of blocks and clicks it
        block_to_place.click()

        expected_durability = f"{initial_durability - 1}/"

        WebDriverWait(self.driver, 5).until(expected_conditions.text_to_be_present_in_element((By.ID, "durability-score"), expected_durability))
        WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#inventory-overlay.hidden")))

        new_durability = int(durability_element.text.split("/")[0])

        self.assertEqual(new_durability, initial_durability - 1, "Durability should be one less after block placement")
        self.assertFalse(inventory_panel.is_displayed(), "Inventory panel should no longer be visible")

