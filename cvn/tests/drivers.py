import functools


def test_drivers(pool_name='drivers', target_attr='selenium'):
    """
    Run tests with `target_attr` set to each instance in the `WebDriverPool`
    named `pool_name`.

    For example, in you setUpClass method of your LiveServerTestCase:

        # Importing the necessaries:
        from selenium import webdriver

        ### In your TestCase:

        # Be sure to add a place holder attribute for the driver variable
        selenium = None

        # Set up drivers
        @classmethod
        def setUpClass(cls):
            cls.drivers = WebDriverList(
                webdriver.Chrome(),
                webdriver.Firefox(),
                webdriver.Opera(),
                webdriver.PhantomJS,
            )
            super(MySeleniumTests, cls).setUpClass()

        # Tear down drivers
        @classmethod
        def tearDownClass(cls):
            cls.drivers.quit()
            super(MySeleniumTests, cls).tearDownClass()

        # Use drivers
        @test_drivers()
        def test_login(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/'))
            self.assertEquals(self.selenium.title, 'Awesome Site')

    This will run `test_login` with each of the specified drivers as the
    attribute named "selenium"

    """
    def wrapped(test_func):
        @functools.wraps(test_func)
        def decorated(test_case, *args, **kwargs):
            test_class = test_case.__class__
            web_driver_pool = getattr(test_class, pool_name)
            for web_driver in web_driver_pool:
                setattr(test_case, target_attr, web_driver)
                test_func(test_case, *args, **kwargs)
        return decorated
    return wrapped


class WebDriverList(list):
    """
    A sequence tat has a `.quit` method that will run on each item
    in the list.
    Used to easily "quit" a list of WebDrivers.
    """

    def __init__(self, *drivers):
        super(WebDriverList, self).__init__(drivers)

    def quit(self):
        for driver in self:
            driver.quit()
