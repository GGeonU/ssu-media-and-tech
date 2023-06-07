from datetime import datetime
import hangul

add_library('sound')

questionSelections = []

# Constants for UI

###### first page ######
mainCharacterImageWidth = 225
mainCharacterImageHeight = 348


###### actor information ######
add_library('sound')

image_x = 60
image_y = 180

leftKeycode  = 37
rightKeycode = 39

pageIdx    = 0
maxPageIdx = 4

sample_sounds = []

isInformationActor = True


###### selection actor ######
selectionImageOffsetX = 719
selectionImageWidth = 463
selectionImageHeight = 81
selectionYesImageOffsetY = 353
selectionNoImageOffsetY = 464

startButtonMarginTop = 20
startButtonHeight = 81
inputBackgroundWidth = 463

nowName = ""
userName = ""
isNameRequired = True
isMain = True

# month english
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

# actor's SD Image and background color
actorInfo = {
    'ganglim': {
        'name' : '강림도령',
        'bg'   : '#32283f',
        'SDImg': './images/icon/SD_ganglim.png'
    },
    'haewon': {
        'name' : '해원맥',
        'bg'   : '#1e231c',
        'SDImg': './images/icon/SD_haewon.png'
    },
    'dukchun': {
        'name' : '이덕춘',
        'bg'   : '#42212f',
        'SDImg': './images/icon/SD_dukchun.png'
    },
    'sungjoo': {
        'name' : '성주신',
        'bg'   : '#462f25',
        'SDImg': './images/icon/SD_sungjoo.png'
    },
    'yumla': {
        'name' : '염라대왕',
        'bg'   : '#1e1e38',
        'SDImg': './images/icon/SD_yumla.png'
    }
}

def setup():
    global font
    global img, scrollX, setTime, profileBg, profileLeftBg
    global clickSave, setTime, boxY, hideSave, saveBtn, saveComplete, saveBtnW, saveBtnH
    global imgRight, imgRightGray, imgLeft, imgLeftGray
    global sample_sound, sample_sounds
    global canvasBackgroundImage, canvasCuteBackgroundImage, canvasCuteCloudImage
    global sandStorm, cuteBgX, cuteBgTurn, cursorIcon, cursorBlink, lastStepBtn, nextBoxY, showNextBtn
    
    size(1280, 720)
    
    font = createFont("Dialog-48", 32)
    textFont(font)
    
    ### actor information ###
    canvasBackgroundImage     = loadImage("./images/slide/canvas_background.png")
    canvasCuteBackgroundImage = loadImage("./images/slide/canvas_cute_background.png")
    canvasCuteCloudImage      = loadImage("./images/slide/canvas_cute_cloud.png")
    
    # 등장인물 배경 변수 세팅 
    for i in range(1, 6):
        globals()["hero{}".format(i)]     = loadImage("./images/slide/character_des_{}.png".format(i))
        globals()["heroCute{}".format(i)] = loadImage("./images/slide/character_des_cute_{}.png".format(i))
        globals()["cuteBg{}".format(i)]   = False
        
        filename     = "./sounds/vocal{}.mp3".format(i)
        sample_sound = SoundFile(this, filename)
        sample_sounds.append(sample_sound)
    
    # 큐트버전 구름 이동 변수 세팅 
    cuteBgX    = width / 2
    cuteBgTurn = 10
    
    sandStorm    = loadImage("./images/slide/sandStorm.png")
    
    imgLeft      = loadImage("./images/slide/left.png")
    imgLeftGray  = loadImage("./images/slide/leftGray.png")
    
    imgRight     = loadImage("./images/slide/right.png")
    imgRightGray = loadImage("./images/slide/rightGray.png")
    
    cursorIcon   = loadImage("./images/slide/cursor.png")
    cursorBlink  = False
    
    lastStepBtn  = loadImage("./images/slide/nextStepBtn.png")
    nextBoxY     = height
    showNextBtn  = False
    
    
    ### selection my actor ###
    img           = loadImage("./images/sandStorm.png")
    profileBg     = loadImage("./images/profile/sandBg.png")
    profileLeftBg = loadImage("./images/profile/myProfileTicket.png")
    saveBtn       = loadImage("./images/profile/saveBtn.png")
    saveComplete  = loadImage("./images/profile/saveCompleteInfo.png")
    
    clickSave = False
    setTime   = 0
    boxY      = height
    hideSave  = False
    saveBtnW  = 206
    saveBtnH  = 46

## get text width
def getTextWidth(word):
    return int(textWidth(word))

def convertKoreanLang(word):
    return word.decode('utf-8')

def draw():
    global setTime
    background(255)
    frameRate(30)

    if isMain:
        drawMain()
    elif isInformationActor:
        frameRate(3)
        drawInformationActor()
    elif isNameRequired:
        drawInputUserName()
    elif isSelectionRequired():
        drawQuestions()
    else:
        actorNickname = actorBySelections()
        selectMyActor(actorNickname, hangul.join_jamos(userName))

# show my actor
def selectMyActor(actor, userName):
    global profileBg, profileLeftBg
    global nowTime
    global clickSave, setTime, boxY, hideSave
    
    if not actorInfo[actor]:
        return
    
    nowTime = datetime.now()
    
    image(profileBg, 0, 0)
    image(profileLeftBg, 0, 0)
    
    setMyActorTicket()
    setMyActorProfile(actor, userName)
    
    if not clickSave:
        image(saveBtn, width / 4 * 3 - saveBtnW / 2, height - saveBtnH - 30, saveBtnW, saveBtnH)
    else:
        save("myActor.jpg")
        if (setTime <= 50):
            showCompleteSave()
            setTime += 1
        else:
            clickSave = False
            hideSave  = False
            boxY      = height
            setTime   = 0

## save complete info box
def showCompleteSave():
    global boxY, hideSave, saveComplete
    
    boxWidth  = 490
    boxHeight = 60
    boxX      = width / 2 - boxWidth / 2

    if (boxY >= height - (boxHeight + 20) and not hideSave):
        boxY -= 20
    elif setTime >= 35:
        hideSave = True
        boxY    += 20

    image(saveComplete, boxX, boxY, boxWidth, boxHeight)

def setMyActorTicket():
    global nowTime
    
    ## date time
    posterText = "DATE:\n%s %s\nFREE PASS\nDAY 1\n---\nPLACE EVENT\n%s"
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
    nowName = convertKoreanLang(actorInfo[actor]["name"])
    nowImg  = actorInfo[actor]["SDImg"]
    nowBg   = actorInfo[actor]["bg"]
    
    circleW = 300
    sdImg   = loadImage(nowImg)
    sdX     = width / 4 * 3
    sdY     = height / 2
    sdW     = circleW - 70
    
    ## your actor is Description
    fill(0)
    textSize(32)
    desc = ("[%s]" % userName) + convertKoreanLang("님과 가장 잘 어울리는 배역은...")
    textLen = (width / 4 * 3) - int(textWidth(desc) / 2)
    
    rect(width / 4 * 2 + 30, 60, width / 2 - 80, 3)
    text(desc, textLen, 105)
    rect(width / 4 * 2 + 30, 120, width / 2 - 80, 3)
    
    ## actor SD Image
    fill(nowBg)
    stroke(0)
    ellipse(sdX, sdY, circleW, circleW)
    
    image(sdImg, sdX - sdW / 2, sdY - sdW / 2, sdW, sdW)
    
    ## actor name
    textSize(48)
    fill(0)
    text(nowName, width / 4 * 3 - getTextWidth(nowName) / 2, height - 130)

# save my actor profile image
def saveMyActorProfile():
    global clickSave
    
    targetX = width / 4 * 3
    
    if (mouseX >= targetX - saveBtnW / 2 and mouseY >= height - saveBtnH - 30 and mouseX <= targetX + saveBtnW / 2 and mouseY <= height - 30):
        clickSave = True
    else:
        clickSave = False
    
def drawQuestions():
    imageMode(CORNER)
    textAlign(LEFT, BASELINE)
    
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

def drawInputUserName():
    
    startButtonMarginTop = 20
    startButtonHeight = 81
    
    backgroundImage = loadImage("./images/question_background.png")
    background(backgroundImage)
    
    imageMode(CENTER)
    backgroundNameImage = loadImage("./images/input_name/input_name_background.png")
    image(backgroundNameImage, width / 2, height / 2)
    
    inputNameImage = loadImage("./images/input_name/input_name.png")
    image(inputNameImage, width / 2, (height / 2) + (startButtonHeight / 2))
    
    startButtonImage = loadImage("./images/input_name/start_button_image.png")
    image(startButtonImage, width / 2, (height / 2) + (startButtonHeight / 2) + startButtonHeight + startButtonMarginTop)
    
    textAlign(CENTER, CENTER)
    font = createFont("Dialog-48", 24)
    
    if userName != "":
        fill(0)
        text(hangul.join_jamos(userName), width / 2, height / 2 + 35)
    else:
        # placeholder
        fill(224, 224, 224, 224)
        text(convertKoreanLang("이름을 입력하세요"), width / 2, height / 2 + 35)

def isSelectionRequired():
    return len(questionSelections) < 4

def didQuestionStartButtonPressed():
    global isNameRequired
    if (width / 2 - inputBackgroundWidth / 2) <= mouseX <= (width / 2 + inputBackgroundWidth / 2) and ((height / 2) + (startButtonHeight / 2) + startButtonMarginTop + startButtonHeight) - (startButtonHeight / 2) <= mouseY <= ((height / 2) + (startButtonHeight / 2) + startButtonMarginTop + startButtonHeight) + (startButtonHeight / 2):
        isNameRequired = False
        
def didMainStartButtonPressed():
    global isMain
    if (width / 2) - (mainCharacterImageWidth / 2) <= mouseX <= (width / 2) + (mainCharacterImageWidth / 2) and (height / 2) - (mainCharacterImageHeight / 2) <= mouseY <= (height / 2) + (mainCharacterImageHeight / 2):
        isMain = False
        
def drawMain():
    backgroundMain = loadImage("./images/main/main_background.png") 
    background(backgroundMain)

    imageMode(CENTER)
    if (width / 2) - (mainCharacterImageWidth / 2) <= mouseX <= (width / 2) + (mainCharacterImageWidth / 2) and (height / 2) - (mainCharacterImageHeight / 2) <= mouseY <= (height / 2) + (mainCharacterImageHeight / 2):
        animatedImage = loadImage("./images/main/main_animated_character.png")
        image(animatedImage, width / 2, height / 2) 
    else:
        originalImage = loadImage("./images/main/main_original_character.png")
        image(originalImage, width / 2, height / 2)

def drawInformationActor():
    imageMode(CENTER)
    
    background(canvasBackgroundImage)
    
    # 현재 이미지 슬라이드 노출 
    slideInformationActorImage(pageIdx)
    
    # 첫 번째 슬라이드는 왼쪽 버튼 미노출
    if pageIdx > 0:
        if dist(mouseX, mouseY, 30, height / 2) <= 50:
            image(imgLeft, 30, height / 2, 50, 50)
        else:
            image(imgLeftGray, 30, height / 2, 50, 50)

    # 큐트 버전 전환 후 다음 캐릭터로 이동 가능
    if globals()["cuteBg{}".format(pageIdx+1)] and pageIdx < maxPageIdx:
        if dist(mouseX, mouseY, 532, height / 2) <= 50:
            image(imgRight, 532, height / 2, 50, 50)
        else:
            image(imgRightGray, 532, height / 2, 50, 50)

# 현재 캐릭터 이미지 세팅해주는 함수 
def slideInformationActorImage(idx):
    global cuteBgX, cuteBgTurn
    global cursorBlink
    
    idx += 1
    
    img    = globals()["hero{}".format(idx)]
    cuteBg = globals()["cuteBg{}".format(idx)]
    
    if cuteBg:
        # 구름 좌우 움직임 제어 
        if width / 2 - 100 > cuteBgX or cuteBgX >= width / 2 + 100:
            cuteBgTurn *= -1
        
        cuteBgX += cuteBgTurn
        
        background(canvasCuteBackgroundImage)
        image(canvasCuteCloudImage, cuteBgX, height / 2)
        
        img = globals()["heroCute{}".format(idx)]
    else:
        background(canvasBackgroundImage)
    
    image(img, width / 2, height / 2, 1280, 720)
    
    if not cuteBg:
        # 이미지 클릭 버튼 깜빡임 효과 
        if cursorBlink:
            image(cursorIcon, 400, height - 200)
            cursorBlink = False
        else:
            cursorBlink = True
    
    if showNextBtn:
        showNextPageBtn()


# 마지막 페이지로 넘어가는 버튼 클릭 시 실행 함수
def showNextPageBtn():
    global nextBoxY
    
    nextBoxWidth = 490
    nextBoxHeight = 66
    
    if nextBoxY >= height - 50:
        nextBoxY -= 10
    
    image(lastStepBtn, width / 2, nextBoxY, nextBoxWidth, nextBoxHeight)


# 모든 사운드 정지 
def stopSoundsAll(sound_list):
    for sound in sound_list:
        sound.stop()

def mousePressed():
    if isMain:
        didMainStartButtonPressed()
    elif isNameRequired:
        didQuestionStartButtonPressed()
    elif isSelectionRequired():
        didSelectionPressed()
    
def mouseClicked():
    global isInformationActor
    global sample_sounds
    global image_x, image_y
    global pageIdx, showNextBtn
    
    if isInformationActor:
        nextBoxW = 490
        nextBoxH = 66
        
        if showNextBtn :
            if (width / 2 - nextBoxW / 2 <= mouseX <= width / 2 + nextBoxW / 2 and height - nextBoxH - 40 <= mouseY <= height - 40):
                isInformationActor = False
            
        isCuteBg = globals()["cuteBg{}".format(pageIdx+1)]
    
        # 특정 영역을 클릭했을 때
        if (image_x <= mouseX <= image_x + 428 and image_y <= mouseY <= image_y + 416):
            if not isCuteBg:
                image(sandStorm, width / 2, height / 2, 1280, 720)
                globals()["cuteBg{}".format(pageIdx+1)] = True
                
                stopSoundsAll(sample_sounds)
                sample_sounds[pageIdx].play()
                
                if pageIdx >= maxPageIdx and not showNextBtn:
                    showNextBtn = True
        
        # 왼쪽으로 이동 버튼 클릭 시
        elif dist(mouseX, mouseY, 30, height / 2) <= 50 and pageIdx > 0:
            pageIdx -= 1
            
            stopSoundsAll(sample_sounds)
            sample_sounds[pageIdx].play()
        
        # 오른쪽으로 이동 버튼 클릭 시
        elif dist(mouseX, mouseY, 532, height / 2) <= 50 and isCuteBg and pageIdx < maxPageIdx:
            pageIdx += 1
            
            stopSoundsAll(sample_sounds)
    else:
        saveMyActorProfile()
    
def keyPressed():
    global userName
    global sample_sound, pageIdx
    
    if isInformationActor:
        isCuteBg = globals()["cuteBg{}".format(pageIdx+1)]
        if keyCode == leftKeycode:
            if pageIdx > 0:
                image(imgLeft, 30, height / 2, 50, 50)
                stopSoundsAll(sample_sounds)
                
                pageIdx -= 1
                sample_sounds[pageIdx].play()
        elif keyCode == rightKeycode:
            if isCuteBg and pageIdx < maxPageIdx:
                image(imgRight, 532, height / 2, 50, 50)
                stopSoundsAll(sample_sounds)
                
                pageIdx += 1 
    elif isNameRequired:
        if key == BACKSPACE:
            userName = userName[:-1]
        elif type(key) is str:
            userName = hangul.sanitize_jamo(userName, key)