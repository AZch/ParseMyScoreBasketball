from selenium import webdriver
import time
from LastGame import LastGame
from Game import Game
import traceback
from Constants import XPath
import ExecReq
import datetime

def parseLastCntWin(elems, isFirstTeam):
    countElem = 0
    listRes = list()
    while 5 > len(listRes) and countElem < len(elems):
        elems[countElem].click()
        driver.switch_to.window(driver.window_handles[2])
        print("----------------------------")
        kf = ExecReq.getKF(driver)
        if kf == False or (kf[0] < 1.3 or kf[1] < 1.3):
            countElem += 1
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            continue
        scoreFirst = ExecReq.getElemByXPath("//*[@class='odd']", driver)
        scoreSec = ExecReq.getElemByXPath("//*[@class='even']", driver)
        timeStart = time.time()
        while len(scoreFirst.text.split()) < 6 or len(scoreSec.text.split()) < 6:
            if time.time() - timeStart > 5:
                break
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            elems[countElem].click()
            driver.switch_to.window(driver.window_handles[2])
            scoreFirst = ExecReq.getElemByXPath("//*[@class='odd']", driver)
            scoreSec = ExecReq.getElemByXPath("//*[@class='even']", driver)
        if (len(scoreFirst.text.split()) < 6 or len(scoreSec.text.split()) < 6):
            countElem += 1
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            continue
        lastGame = LastGame("", [scoreFirst.text, scoreSec.text])
        print("----------------------------")
        if lastGame.isCleanScore(isFirstTeam=isFirstTeam):
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            print("this game bad")
            return False
        listRes.append(lastGame)
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        countElem += 1
    driver.switch_to.window(driver.window_handles[1])
    return listRes

def skip(i, driver, countSkip = 2):
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return  i + countSkip

def parseMaths(driver, XPathBtn, dropLigue):
    try:
        driver.get('https://www.myscore.ru/basketball/')
        ExecReq.clickGetElem(driver, XPathBtn)
        time.sleep(1)
        elemsLigue = driver.find_elements_by_xpath("//table[@class='basketball']")
        j = 0
        lstGame = list()
        i = 0
        elems = ExecReq.getElemsByXPath(XPath.allGame, driver)
        while j < len(elemsLigue):
            ligueName = elemsLigue[j].text.split('\n')[1]
            print(ligueName)
            countGame = elemsLigue[j].text[len(elemsLigue[j].text.split('\n')[0] + "\n" + ligueName):].count(':')
            print(countGame)
            startI = i
            while i < startI + (countGame) * 2 and i < len(elems):
                resCmd = elems[i].text + elems[i + 1].text
                elemBase = elems[i]
                resCmd = resCmd.translate({ord(c): None for c in '\n'})
                if len(resCmd.split('(Ж)')) > 1:
                    i += 2
                    continue
                timeGame = resCmd.split()[0].split(":")
                timeGame = int(timeGame[0]) * 60 + int(timeGame[1])
                print(resCmd)
                try:
                    dropLigue.index(ligueName)
                    i += 2
                    print('drop')
                    continue
                except:
                    pass
                ExecReq.clickElem(elems[i])
                driver.switch_to.window(driver.window_handles[1])

                kf = ExecReq.getKF(driver)
                if kf == False or (kf[0] < 1.3 or kf[1] < 1.3):
                    i = skip(i, driver)
                    continue
                elif kf[0] > kf[1]:
                    isFirstTeam = False
                elif kf[1] > kf[0]:
                    isFirstTeam = False
                else:
                    isFirstTeam = True
                    print("kf team equel")

                ''''''
                ExecReq.clickGetElem(driver, XPath.clickH2H)
                ExecReq.clickGetElem(driver, XPath.clickHomeGame)
                while ExecReq.clickGetElem(driver, XPath.clickMoreHomeGame):
                   pass

                elem = ExecReq.getElemsByXPath(XPath.homeGame, driver)
                home = parseLastCntWin(elems=elem, isFirstTeam=isFirstTeam)
                if home == False:
                    i = skip(i, driver)
                    continue
                ''''''
                ''''''
                print('away')
                ExecReq.clickGetElem(driver, XPath.clickAwayGame)
                while ExecReq.clickGetElem(driver, XPath.clickMoreAwayGame):
                   pass

                elem = ExecReq.getElemsByXPath(XPath.awayGame, driver)
                away = parseLastCntWin(elems=elem, isFirstTeam=isFirstTeam)
                if away == False:
                    i = skip(i, driver)
                    continue
                ''''''
                newGame = Game(timeMin=timeGame, teams=resCmd, lstHome=home, lstAway=away, elemBase = elemBase)
                lstGame.append(newGame)
                print('add')

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                i += 2
            j += 1
        return lstGame
    except:
        print('Ошибка:\n', traceback.format_exc())


driver = webdriver.Chrome("C:\\Users\\anton\\Desktop\\chromedriver.exe")
#lstGame = parseMaths(driver, XPath.btnToday)
lstGame = list()
goGameNextDay = True
while True:
    if (datetime.datetime.now().hour >= 1):
        goGameNextDay = True
    if (datetime.datetime.now().hour >= 20):
        lstGame.extend(parseMaths(driver, XPath.btnNextDay, ['США: НБА']))
        goGameNextDay = False
    while len(lstGame) > 0:
        for game in lstGame:
            if game.checkTime():
                print(game.teams)
                try:
                    lstGame.remove(game)
                except:
                    print('Ошибка:\n', traceback.format_exc())

driver.close()

                # clickElem(driver, game.elemBase)
                # driver.switch_to.window(driver.window_handles[1])
                # kf = getElemByXPath("//*[@id='tab-prematch-odds']", driver)
                # floatKfFirst = 0.0
                # floatKfSec = 0.0
                # try:
                #     floatKfFirst = float(kf.text.split('\n')[1])
                #     floatKfSec = float(kf.text.split('\n')[3])
                # except:
                #     print('Ошибка1111:\n', traceback.format_exc())
                #     driver.close()
                #     driver.switch_to.window(driver.window_handles[0])
                #     try:
                #         lstGame.remove(game)
                #     except:
                #         print('Ошибка:\n', traceback.format_exc())
                #     continue
                # driver.close()
                # driver.switch_to.window(driver.window_handles[0])
                # if (game.checkGame(floatKfFirst, floatKfSec)):
                #     print(game.teams)
                # else:
                #     print("nope" + str(game.teams))