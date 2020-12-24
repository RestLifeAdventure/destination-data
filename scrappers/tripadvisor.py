from selenium.webdriver.remote.webelement import WebElement
import globals


class XPath:
    searchResult = '//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div/div/div/div'
    # ---------------- For locations ---------------- #
    placeType = '//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/span[2]'
    locationName = '//*[@id="lithium-root"]/main/div[1]/div/h1/span/span[2]'
    locationDesc = '//*[@id="lithium-root"]/main/div[7]/div/div[1]/div/div[2]/div'
    locationOpenPhotos = '//*[@id="lithium-root"]/main/div[5]/div/div/div[2]/button'
    locationPhoto = '//*[@id="lithium-root"]/main/div[5]/div/div/div[3]/div/div[2]/div/div[2]/div/div[1]/div/div/div[{index}]/div/div/div/img'
    # ---------------- For places ---------------- #
    placeName = '//*[@id="HEADING"]'
    placeOpenPhotos = '//*[@id="component_21"]/div/div/div[2]/div/div/div[2]/div/div/div[6]/div/button'


class TripadvisorScrapper:
    places = []  # type: list[str]
    baseUrl = "https://tripadvisor.com"  # type: str
    _placeType = None  # type:str

    def __init__(self) -> None:
        self.places = globals.PLACES
        self.start()

    def byXpath(self, xpath: str) -> WebElement:
        return globals.driver.find_element_by_xpath(xpath=xpath)

    def start(self) -> None:
        for place in self.places:
            # try:
            self.visitDestinationAboutPage(place=place)
            self.extractData()
        # except:
        # pass

    def visitDestinationAboutPage(self, place: str) -> None:
        globals.driver.get(f"{self.baseUrl}/Search?q={place}")
        globals.driver.implicitly_wait(3)
        # ---------------- Get Place Type ---------------- #
        self._placeType = self.byXpath(
            xpath=XPath.placeType).text.lower()  # type: str
        # ---------------- Clicking on search result ---------------- #
        self.byXpath(xpath=XPath.searchResult).click()
        # ---------------- Switch to new tab opened ---------------- #
        globals.driver.switch_to.window(globals.driver.window_handles[-1])

    def extractData(self) -> None:
        # ---------------- Getting Data ---------------- #
        placeImages = []
        # Check: If it's location
        if "location" in self._placeType:
            placeName = self.byXpath(
                xpath=XPath.locationName).text  # type: str
            placeAbout = self.byXpath(
                xpath=XPath.locationDesc).text  # type: str
            placeImages = self.extractLocationImages()
        else:
            placeName = self.byXpath(xpath=XPath.placeName).text  # type: str
            placeAbout = None  # type: None
            placeImages = self.extractPlaceImages()
        # ---------------- Saving Data ---------------- #
        self.saveData(placeName, placeAbout, placeImages)

    def extractLocationImages(self) -> list[str]:
        self.byXpath(xpath=XPath.locationOpenPhotos).click()
        totalPhotos = self.byXpath(
            xpath=XPath.locationPhoto.split("{")[0].removesuffix("/div[")).find_elements_by_xpath("div")
        print(f"[Total] {totalPhotos}")
        for i in range(10):
            print(XPath.locationPhoto.format(index=i))

    def extractPlaceImages(self) -> list[str]:
        pass

    def saveData(self, *data) -> None:
        print(f"[Data] {data}")
