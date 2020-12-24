import globals
from selenium.webdriver import Edge
from scrappers.tripadvisor import TripadvisorScrapper


def initSetup():
    globals.driver = Edge(globals.DRIVER_NAME)
    globals.driver.manage().window().maximize()


def exitProcess():
    globals.driver.quit()
    exit()


def scrapeContent():
    TripadvisorScrapper()


if __name__ == "__main__":
    initSetup()
    scrapeContent()
    # exitProcess()
