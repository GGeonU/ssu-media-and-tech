from datetime import datetime

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
    global clickSave
        
    size(1280, 720)
    
    img           = loadImage("./images/sandStorm.png")
    profileBg     = loadImage("./images/sandBg.png")
    profileLeftBg = loadImage("./images/myProfileTicket.png")
    
    clickSave = False
    monthList = transMonth()
    chInfo    = getCharacterInfo()


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
    
    # show my actor ticket page
    selectMyActor('ganglim', 'ar.kwon')


# show my actor
def selectMyActor(actor, userName):
    global chInfo, profileBg, profileLeftBg
    global nowTime
    global clickSave
    
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
