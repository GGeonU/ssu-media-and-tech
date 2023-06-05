from datetime import datetime

questionSelections = []

# Constants for UI

selectionImageOffsetX = 719
selectionImageWidth = 463
selectionImageHeight = 81
selectionYesImageOffsetY = 353
selectionNoImageOffsetY = 464

nowName = ""

def transMonth():
    monthList = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
    }
    
    return monthList

def setup():
    global img, scrollX, setTime, chInfo, profileBg, profileLeftBg
    global monthList
    global clickSave, setTime, boxY, hideSave, saveBtn

        
    size(1280, 720)
    
    img           = loadImage("./images/sandStorm.png")
    profileBg     = loadImage("./images/sandBg.png")
    profileLeftBg = loadImage("./images/myProfileTicket.png")
    saveBtn       = loadImage("./images/icon/saveBtnTemp.png")
    
    clickSave = False
    monthList = transMonth()
    chInfo    = getCharacterInfo()

    clickSave = False
    setTime   = 0
    boxY      = height
    hideSave  = False

# get actor's SD Image and background color
def getCharacterInfo():
    info = {
        'ganglim': {
            'name' : 'GANG LIM',
            'bg'   : '#32283f',
            'SDImg': './images/icon/SD_ganglim.png'
        },
        'haewon': {
            'name' : 'HAE WON MAC',
            'bg'   : '#1e231c',
            'SDImg': './images/icon/SD_haewon.png'
        },
        'dukchun': {
            'name' : 'DUK CHUN',
            'bg'   : '#42212f',
            'SDImg': './images/icon/SD_dukchun.png'
        },
        'sungjoo': {
            'name' : 'SUNG JOO SIN',
            'bg'   : '#462f25',
            'SDImg': './images/icon/SD_sungjoo.png'
        },
        'yumla': {
            'name' : 'YUM LA KING',
            'bg'   : '#1e1e38',
            'SDImg': './images/icon/SD_yumla.png'
        }
    }
    
    return info

## get text width
def getTextWidth(word):
    return int(textWidth(word))

def draw():
    global setTime
    background(255)
    
    if len(questionSelections) >= 4:
        # show my actor ticket page
        actorNickname = actorBySelections()
        userName = 'ar.kwon'
        selectMyActor(actorNickname, userName)
    else:
        drawQuestions()

# show my actor
def selectMyActor(actor, userName):
    global chInfo, profileBg, profileLeftBg
    global nowTime
    global clickSave, setTime, boxY, hideSave
    
    if not chInfo[actor]:
        return
    
    nowTime = datetime.now()
    
    image(profileBg, 0, 0)
    image(profileLeftBg, 0, 0)
    
    setMyActorTicket()
    setMyActorProfile(actor, userName)
    
    if not clickSave:
        textSize(24)
        fill(255)
        text("SAVE", width / 4 * 3 - getTextWidth("SAVE") / 2, height - 40)
    else:
        clickSave = False
        save("myProfile.jpg")
        if (setTime <= 60):
            showCompleteSave()
            setTime += 1
        else:
            clickSave = False
            hideSave  = False
            boxY      = height
            setTime   = 0

## save complete info box
def showCompleteSave():
    global boxY, hideSave, saveBtn
    
    boxWidth = 400
    boxHeight = 80
    boxX = width / 2 - boxWidth / 2
    saveText = "SAVED!"

    if (boxY >= height - (boxHeight + 20) and not hideSave):
        boxY -= 20
    elif setTime >= 40:
        hideSave = True
        boxY += 20

    image(saveBtn, boxX, boxY, boxWidth, boxHeight)

def setMyActorTicket():
    global monthList, nowTime
    
    ## date time
    posterText = """
    DATE:
    %s %s
    FREE PASS
    DAY 1
    ---
    PLACE EVENT
    %s
    """
    
    transMonth = monthList[nowTime.strftime("%m")]
    if int(nowTime.strftime("%H")) >= 12:
        localeType = "PM"
    else:
        localeType = "AM"
    
    fill(0)
    textSize(18)
    text(posterText % (transMonth, nowTime.strftime("%d. %Y"), "%s%s" % (nowTime.strftime("%I"), localeType)), 40, 140)
    
    ## month and year
    textSize(42)
    text("%s %s" % (transMonth, nowTime.strftime("%Y")), 115, height - 115)
    
def setMyActorProfile(actor, userName):
    global chInfo
    global nowName
    
    actorInfo = chInfo[actor]
    
    nowName = actorInfo["name"]
    nowImg  = actorInfo["SDImg"]
    nowBg   = actorInfo["bg"]
    
    circleW = 300
    sdImg   = loadImage(nowImg)
    sdX     = width / 4 * 3
    sdY     = height / 2
    sdW     = circleW - 70
    
    ## your actor is Description
    fill(0)
    textSize(32)
    desc    = "[%s], your actor is.." % userName
    textLen = (width / 4 * 3) - int(textWidth(desc) / 2)
    
    rect(width / 4 * 2 + 30, 60, width / 2 - 60, 3)
    text(desc, textLen, 100)
    rect(width / 4 * 2 + 30, 120, width / 2 - 60, 3)
    
    ## actor profile
    fill(nowBg)
    stroke(0)
    ellipse(sdX, sdY, circleW, circleW)
    
    image(sdImg, sdX - sdW / 2, sdY - sdW / 2, sdW, sdW)
    
    ## actor profile name
    textSize(48)
    fill(0)
    text(nowName, width / 4 * 3 - getTextWidth(nowName) / 2, height - 100)
    
def drawQuestions():
    
    # background
    
    backgroundImage = loadImage("./images/question_background.png")
    background(backgroundImage)
    
    # progress
    
    progressBackgroundImage = loadImage("./images/question_progress_background.png")
    image(progressBackgroundImage, 0, 0)
    
    for i in range(0, 4):
        if i <= len(questionSelections):
            progressImage = loadImage("./images/progress/question_progress_%d.png" % (i + 1))
            image(progressImage, 69, 134 + (i * (55 + 89)))
        else:
            progressImage = loadImage("./images/progress/question_progress_empty.png")
            image(progressImage, 69, 134 + (i * (55 + 89)))
            
    index = len(questionSelections) + 1
    questionImage = loadImage("./images/question/question_%d.png" % index)
    image(questionImage, 673, 83)
    
    # selections
    
    selectionYesImage = loadImage("./images/selection/selection_yes.png")
    selectionNoImage = loadImage("./images/selection/selection_no.png")
    
    image(selectionYesImage, selectionImageOffsetX, selectionYesImageOffsetY)
    image(selectionNoImage, selectionImageOffsetX, selectionNoImageOffsetY)
    
def didSelectionPressed():
    global questionSelections
    if selectionImageOffsetX <= mouseX <= (selectionImageOffsetX + selectionImageWidth):
        if selectionYesImageOffsetY <= mouseY <= (selectionYesImageOffsetY + selectionImageHeight):
            questionSelections.append(True)
        elif selectionNoImageOffsetY <= mouseY <= (selectionNoImageOffsetY + selectionImageHeight):
            questionSelections.append(False)
            
def actorBySelections():
    results = []
    for index, selection in enumerate(questionSelections):
        if index == 0:
            if selection:
                results.append("sungjoo")
                results.append("dukchun")
            else:
                results.append("ganglim")
                results.append("haewon")
        elif index == 1:
            if selection:
                results.append("ganglim")
                results.append("sungjoo")
            else:
                results.append("haewon")
                results.append("dukchun")
        elif index == 2:
            if selection:
                results.append("sungjoo")
                results.append("sungjoo")
                results.append("dukchun")
            else:
                results.append("ganglim")
        elif index == 3:
            if selection:
                results.append("haewon")
                results.append("dukchun")
            else:
                results.append("sungjoo")
                results.append("ganglim")
            
    return max(results, key=results.count)
            
def mousePressed():
    didSelectionPressed()
    
def mouseClicked():
    global nowName
    global clickSave
    
    if (mouseX >= width / 4 * 3 - getTextWidth(nowName) and mouseY >= height - 100):
        clickSave = True
    else:
        clickSave = False
    
