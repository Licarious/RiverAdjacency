from PIL import Image

class ProvinceDefinition:
    id = 0
    red = 0
    green = 0
    blue = 0
    name = ""
    other_info = ""
    lastKnownY = -1

riverList = []
tmpRiverList = []
riverProvList = []
provList = []
mapDefinition = open("Input/definition.csv")
defaultMap = open("Input/default.map")
provMap = Image.open("Input/provinces.png")
landedTitles = open("Input/00_landed_titles.txt",'r',encoding='utf-8',errors='ignore')
borderIDList = []
total=0

def readProvinceDeff():
    for province in mapDefinition:
        if province.strip().startswith("#"):
            pass
        else:
            tmpline = province.strip().split(';')
            try:
                province = ProvinceDefinition()
                province.red = int(tmpline[1])
                province.id = int(tmpline[0].lstrip("#"))
                province.green = int(tmpline[2])
                province.blue = int(tmpline[3])
                province.name = tmpline[4]
                provList.append(province)
            except:
                pass
    pass
def getRiverProvinces():
    for line in defaultMap:
        if line.strip().startswith("#"):
            pass
        elif line.strip().startswith("river_provinces"):
            if "RANGE" in line:
                x1=0
                x2=0
                #print(line)
                words = line.split(" ")
                for word in words:
                    if "#" in word:
                        break
                    else:
                        try:
                            if x1 == 0:
                                x1 = int(word)
                            elif x2 == 0:
                                x2 = int(word)
                        except:
                            pass
                for i in range(x1,x2+1):
                    riverList.append(i)
                #print("%s,%s"%(x1,x2))
            elif "LIST" in line:
                words = line.split(" ")
                for word in words:
                    if "#" in word:
                        break
                    else:
                        try:
                            riverList.append(int(word))
                        except:
                            pass
                #print(line)
    pass      
def drawRiverMat(riverProvList):
    xRange= range(0,provMap.size[0],1)
    yRange= range(0,provMap.size[1],1)
    drawReader = provMap.load()
    drawingMap = Image.open("Input/provinces.png")
    drawingMap.putalpha(0)
    riverMat = drawingMap.load()
    z=0
    for prov in riverProvList:
        provinceEnd = False
        z+=1
        print("%s \t-\t %s/%s"%(prov.name,z,total))
        for y in yRange:
            if provinceEnd:
                break
            else:
                for x in xRange:
                    if drawReader[x,y] == (prov.red, prov.green, prov.blue):
                        riverMat[x,y] = (0,0,0)
                        prov.lastKnownY = y
                        #print("%s - %i,%i"%(prov.name,x,y))
                if prov.lastKnownY > -1 and y > prov.lastKnownY + (provMap.size[1] * 1/256):
                    provinceEnd = True
    drawingMap.save("Output/RiverMat.png")
def drawRiverBorderMat():
    xRange= range(0,provMap.size[0],1)
    yRange= range(0,provMap.size[1],1)
    tmpDrawingMap = Image.open("Output/RiverMat.png")
    drawReader = tmpDrawingMap.load()
    drawingBorderMap = Image.open("Input/provinces.png")
    drawingBorderMap.putalpha(0)
    riverBorderMat = drawingBorderMap.load()
    for y in yRange:
        for x in xRange:
            if drawReader[x,y] == (0,0,0,255):
                #print("%s,%s"%(x,y))
                if y>0:
                    if not drawReader[x,y-1] == (0,0,0,255):
                        riverBorderMat[x,y-1] = (0,0,0)
                if y<provMap.size[1]:
                    if not drawReader[x,y+1] == (0,0,0,255):
                        riverBorderMat[x,y+1] = (0,0,0)
                if x>0:
                    if not drawReader[x-1,y] == (0,0,0,255):
                        riverBorderMat[x-1,y] = (0,0,0)
                if x<provMap.size[0]:
                    if not drawReader[x+1,y] == (0,0,0,255):
                        riverBorderMat[x+1,y] = (0,0,0)
                #print("%s - %i,%i"%(prov.name,x,y))
    drawingBorderMap.save("Output/RiverBorderMat.png")
def getBorderIDs():
    xRange= range(0,provMap.size[0],1)
    yRange= range(0,provMap.size[1],1)
    drawReader = provMap.load()
    borderMat = Image.open("Output/RiverBorderMat.png")
    riverBorderMat = borderMat.load()
    colorList = []
    for y in yRange:
        for x in xRange:
            if riverBorderMat[x,y] == (0,0,0,255):
                if not provMap.getpixel((x,y)) in colorList:
                    colorList.append(provMap.getpixel((x,y)))
                    print(provMap.getpixel((x,y)))
    for color in colorList:
        for prov in provList:
            if color[0] == prov.red and color[1] == prov.green and color[2] == prov.blue:
                print(prov.name)
                borderIDList.append(prov.id)
                break;
    pass
def writeBarronyNames():
    barronyList = open("Output/barronyList.txt", "w", encoding='utf-8-sig')
    indintation = 0
    tmpTitle = ""
    for line in landedTitles:
        if indintation == 0:
            if line.strip().startswith("e_"):
                print(line.split(" ")[0])
                barronyList.write("#%s\n"%line.split(" ")[0])
        if indintation == 4:
            if line.strip().startswith("b_"):
                tmpTitle = line.strip().split(" ")[0]
                #print("\t%s"%line.strip().split(" ")[0])
        if indintation == 5:
            if line.strip().startswith("province"):
                for word in line.strip().split(" "):
                    try:
                        tmpID = int(word)
                        if tmpID in borderIDList:
                            print("\t%s"%tmpTitle)
                            barronyList.write("\tthis = title:%s.title_province\n"%tmpTitle)
                    except:
                        pass

        if "{" in line or "}" in line:
            #print("l: "+line)
            for element in list(line.strip()):
                if "{" in element:
                    indintation +=1
                    #print("s: "+element)
                elif "}" in element:
                    indintation -=1
                    #print("e: "+element)
                elif "#" in element:
                    #print("c: "+element)
                    break
    pass

readProvinceDeff()
getRiverProvinces()
riverList = list(dict.fromkeys(riverList))
total = len(riverList)
print(total)
for id in riverList:
    for prov in provList:
        if id == prov.id:
            #print(prov.name)
            riverProvList.append(prov)
            break
drawRiverMat(riverProvList)
drawRiverBorderMat()
getBorderIDs()
writeBarronyNames()