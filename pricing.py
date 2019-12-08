from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import re

counterRefreshed = 0
counterSkipped = 0


def elem(id):
    return driver.find_element_by_id(id)

def findallByClassName(className, regex):
    rawElem = driver.find_element_by_class_name(className)
    rawText = str(rawElem.get_attribute("innerHTML"))
    return re.findall(regex, rawText)

def setTextForId(id, text):
    element = elem(id)
    element.clear()
    element.send_keys(text)

def login():
    print("Entering credentials")
    setTextForId("username", "lieutenant.frank7@googlemail.com")
    setTextForId("password", "dpr3zq5m")
    print("Logging in")
    elem("password").send_keys(Keys.ENTER)
    if "Free" in driver.title:
        login()


def getRoutes():
    print("Getting Routes:")
    routes = findallByClassName("priceTable", "/\w{9}/\w{7}/[0-9]{3,10}")
    print(len(routes))
    return routes

def refreshPrice(route):
    print("Working on Route: " + route.split("/")[3])
    driver.get("https://tycoon.airlines-manager.com" + route)

    try:
        waittime = int(driver.find_element_by_xpath("/html/body/div[3]/div/div[5]/div[2]/div[2]/div/div[2]/div[7]/div[2]/p[2]/span").get_attribute("data-timeremaining"))
        if waittime > 0:
            print(f"Timer is still running!\n{waittime} seconds left!\nNothing to do here")
            global counterSkipped
            counterSkipped += 1
            return
    except:
        pass

    driver.get("https://tycoon.airlines-manager.com" + route + "?fromPricing=1")
    try:
        findallByClassName("box1", "\$[0-9]{1,},?[0-9]{1,3}")
    except:
        driver.get("https://tycoon.airlines-manager.com/marketing/internalaudit/line/" + route.split("/")[3] + "?fromPricing=1")
        pass

    ideals = []
    for ideal in findallByClassName("box1", "\$[0-9]{1,},?[0-9]{1,3}"):
        if "," in ideal:
            ideals.append(int(ideal.replace("$","").replace(",","")))
        else:
            ideals.append(int(ideal.replace("$","")))

    setTextForId("line_priceEco", ideals[0])
    setTextForId("line_priceBus", ideals[1])
    setTextForId("line_priceFirst", ideals[2])
    setTextForId("line_priceCargo", ideals[3])

    elem("line_priceCargo").send_keys(Keys.ENTER)

    global counterRefreshed
    counterRefreshed += 1


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://tycoon.airlines-manager.com/marketing/pricing/?airport=0")
    if "Free" in driver.title:
        login()
    if "Price" in driver.title:
        routes = getRoutes()
        for i in range(0, len(routes)):
            refreshPrice(routes[i])
            print(f"Refreshed {counterRefreshed} line(s)")
            print(f"Skipped {counterSkipped} line(s)")
            print(f"Scanned {counterRefreshed + counterSkipped} out of {len(routes)} so far!")
            print()
