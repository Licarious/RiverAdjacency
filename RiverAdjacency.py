from PIL import Image
from os import path

class ProvinceDefinition:
    id = 0
    red = 0
    green = 0
    blue = 0
    name = ""
    other_info = ""
    lastKnownY = -1

riverList = []
seaList = []
impasableList = []
tmpRiverList = []
riverProvList = []
seaProvList = []
provList = []
mapDefinition = open("Input/definition.csv")
defaultMap = open("Input/default.map")
provMap = Image.open("Input/provinces.png")
landedTitles = open("Input/00_landed_titles.txt",'r',encoding='utf-8',errors='ignore')
borderIDList = []
total=0
removeCostal = True
regenerateMats = True
includeLakes = False

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
def getRangeList(line, tmpList):
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
            tmpList.append(i)
        #print("%s,%s"%(x1,x2))
    elif "LIST" in line:
        words = line.split(" ")
        for word in words:
            if "#" in word:
                break
            else:
                try:
                    tmpList.append(int(word))
                except:
                    pass
    pass
def getRiverProvinces():
    for line in defaultMap:
        if line.strip().startswith("#"):
            pass
        elif line.strip().startswith("sea_zones"):
            getRangeList(line, seaList)
        elif line.strip().startswith("river_provinces"):
            getRangeList(line, riverList)
        elif includeLakes and line.strip().startswith("lakes"):
            getRangeList(line, riverList)
        elif line.strip().startswith("impassable_mountains"):
            getRangeList(line, impasableList)
    pass      
def drawMat(riverProvList,name):
    xRange= range(0,provMap.size[0],1)
    yRange= range(0,provMap.size[1],1)
    drawReader = provMap.load()
    drawingMap = Image.open("Input/provinces.png")
    drawingMap.putalpha(0)
    riverMat = drawingMap.load()
    z=0
    dis = 5

    tupleList = []
    for prov in riverProvList:
        tupleList.append((prov.red,prov.green,prov.blue))

    #print(tupleList)

    for y in yRange:
        if y%128 ==0:
            print("%i%%"%((y*100)/provMap.size[1]))
        for x in xRange:
            if drawReader[x,y] in tupleList:
                riverMat[x,y] = (0,0,0)
    drawingMap.save("Output/%s.png"%name)
def drawBorderMat(name):
    xRange= range(0,provMap.size[0],1)
    yRange= range(0,provMap.size[1],1)
    if "River" in name:
        tmpDrawingMap = Image.open("Output/RiverMat.png")
    else:
        tmpDrawingMap = Image.open("Output/SeaMat.png")
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
                if y<provMap.size[1]-1:
                    if not drawReader[x,y+1] == (0,0,0,255):
                        riverBorderMat[x,y+1] = (0,0,0)
                if x>0:
                    if not drawReader[x-1,y] == (0,0,0,255):
                        riverBorderMat[x-1,y] = (0,0,0)
                if x<provMap.size[0]-1:
                    if not drawReader[x+1,y] == (0,0,0,255):
                        riverBorderMat[x+1,y] = (0,0,0)
                #print("%s - %i,%i"%(prov.name,x,y))
    drawingBorderMap.save("Output/%s.png"%name)
def getBorderIDs(name):
    xRange= range(0,provMap.size[0],1)
    yRange= range(0,provMap.size[1],1)
    drawReader = provMap.load()
    if "river" in name:
        borderMat = Image.open("Output/RiverBorderMat.png")
    else:
        borderMat = Image.open("Output/SeaBorderMat.png")
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
                if "river" in name:
                    borderIDList.append(prov.id)
                else:
                    try:
                        borderIDList.remove(prov.id)
                    except:
                        pass
                break;
    pass
def writeBarronyNames():
    barronyList = open("Output/barronyList.txt", "w", encoding='utf-8-sig')
    indintation = 0
    tmpTitle = ""
    tmpEmpire = ""
    tmpKingdon = ""
    for line in landedTitles:
        if indintation == 0:
            if line.strip().startswith("e_"):
                print(line.split(" ")[0])
                #barronyList.write("#%s\n"%line.split(" ")[0])
                tmpEmpire = line.split(" ")[0]
        if indintation == 1:
            if line.strip().startswith("k_"):
                tmpKingdon = line.strip().split(" ")[0]
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
                            if tmpEmpire != "":
                                barronyList.write("#%s\n"%tmpEmpire)
                                tmpEmpire = ""
                            if tmpKingdon != "":
                                barronyList.write("\t#%s\n"%tmpKingdon)
                                tmpKingdon = ""
                            barronyList.write("\t\tthis = title:%s.title_province\n"%tmpTitle)
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
def removeImpasible(tmpList, impasableList):
    for id in impasableList:
        try:
            tmpList.remove(id)
        except:
            pass
    pass    
readProvinceDeff()
getRiverProvinces()
riverList = list(dict.fromkeys(riverList))
removeImpasible(riverList, impasableList)
for id in riverList:
    for prov in provList:
        if id == prov.id:
            #print(prov.name)
            riverProvList.append(prov)
            break
    pass
total = len(riverProvList)
print(total)
if regenerateMats or not path.exists("Output\RiverMat.png"):
    drawMat(riverProvList,"RiverMat")
if regenerateMats or not path.exists("Output\RiverBorderMat.png"):
    drawBorderMat("RiverBorderMat")
getBorderIDs("river")

#for removeing baronies that border seas from the list
if removeCostal:
    seaList = list(dict.fromkeys(seaList))
    removeImpasible(seaList, impasableList)
    for id in seaList:
        for prov in provList:
            if id == prov.id:
                #print(prov.name)
                seaProvList.append(prov)
                break
        pass
    total = len(seaProvList)
    print(total)
    if regenerateMats or not path.exists("Output\SeaMat.png"):
        drawMat(seaProvList, "SeaMat")
    if regenerateMats or not path.exists("Output\SeaBorderMat.png"):
        drawBorderMat("SeaBorderMat")
    getBorderIDs("sea")

writeBarronyNames()