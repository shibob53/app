def driversetup():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("lang=en")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    browserstack_username = os.getenv('BROWSERSTACK_USERNAME')
    browserstack_access_key = os.getenv('BROWSERSTACK_ACCESS_KEY')
    
    desired_capabilities = options.to_capabilities()
    desired_capabilities.update({
        'os': 'Windows',
        'os_version': '10',
        'browser': 'Chrome',
        'browser_version': 'latest',
        'name': 'Heroku Test',
        'build': 'Flask-Selenium',
        'browserstack.user': browserstack_username,
        'browserstack.key': browserstack_access_key,
        'browserstack.debug': 'true',
        'browserstack.console': 'errors',
        'browserstack.networkLogs': 'true'
    })

    driver = webdriver.Remote(
        command_executor='https://hub-cloud.browserstack.com/wd/hub',
        desired_capabilities=desired_capabilities
    )
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    return driver
