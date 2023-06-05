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
        
    size(1280, 720)
    
    img = loadImage("./images/sandStorm.png")
    profileBg = loadImage("./images/sandBg.png")
    profileLeftBg = loadImage("./images/myProfileTicket.png")
    scrollX = -500
    setTime = 0
    
    monthList = transMonth()
    
    chInfo = getCharacterInfo()


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
    

def draw():
    global setTime
    background(255)
    
    ## load to sand storm
    if (setTime <= 60):
        loadSandStorm()
        setTime += 1
    
    selectMyActor('yumla')
    

# sand storm
def loadSandStorm():
    global scrollX
    scrollX += 3
    image(img, scrollX, 0, 2400, 1200)


# show my actor
def selectMyActor(actor):
    global chInfo, profileBg, profileLeftBg
    global monthList
    
    actorInfo = chInfo[actor]
    nowTime = datetime.now()
    
    if not actorInfo:
        return
    
    image(profileBg, 0, 0)
    
    image(profileLeftBg, 0, 0)
    
    ### left ###
    
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
    
    textSize(18)
    text(posterText % (transMonth, nowTime.strftime("%d. %Y"), nowTime.strftime("%I%p")), 40, 150)
    
    ## month and year
    textSize(40)
    text("%s %s" % (transMonth, nowTime.strftime("%Y")), 150, height - 150)
    
    ### right ### 
    circleW = 300
    sdImg = loadImage(actorInfo["SDImg"])
    sdX = width / 4 * 3
    sdY = height / 2
    sdW = circleW - 70
    
    ## your actor is Description
    fill(0)
    textSize(32)
    desc = "[%s], your actor is.." % "TEST"
    textLen = (width / 4 * 3) - int(textWidth(desc) / 2)
    
    rect(width / 4 * 2 + 30, 60, width / 2 - 60, 3)
    text(desc, textLen, 100)
    rect(width / 4 * 2 + 30, 120, width / 2 - 60, 3)
    
    ## actor profile
    fill(actorInfo['bg'])
    stroke(0)
    ellipse(sdX, sdY, circleW, circleW)
    
    image(sdImg, sdX - sdW / 2, sdY - sdW / 2, sdW, sdW)
    
    ## actor profile name
    textSize(48)
    fill(0)
    text(actorInfo["name"], width / 4 * 3 - int(textWidth(actorInfo["name"]) / 2), height - 100)
    
    ## save My Actor
    #save("myProfile.jpg")
    
