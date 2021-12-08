def findLocs(datals, locid):
    locid1 = locid[0]
    locid2 = locid[1]
    loc1 = []
    loc2 = []
    for item in datals:
        if item[0] == locid1:
            loc1 = item
        if item[0] == locid2:
            loc2 = item
    if len(loc1) == 0 or len(loc2) == 0:
        print("Can not find all locId")
        return None, None
    else:
        return loc1,loc2

def findInnerloc(datals,locid,radius):
    loc1,loc2 = findLocs(datals, locid)
    if loc1 is not None and loc2 is not None:
        loc1_x,loc1_y = float(loc1[1]),float(loc1[2])
        loc2_x,loc2_y = float(loc2[1]),float(loc2[2])
        loc1ls = []
        loc2ls = []
        for item in datals:
            x = float(item[1])
            y = float(item[2])
            dis1 = ((abs(loc1_x - x) ** 2 + abs(loc1_y - y)** 2)** 0.5)
            dis2 = ((abs(loc2_x - x) ** 2 + abs(loc2_y - y)** 2)** 0.5)
            if dis1 <= float(radius):
                loc1ls.append(item)
            if dis2 <= float(radius):
                loc2ls.append(item)
        return loc1ls,loc2ls
    else:
        print("Can not find all locId")
        return None, None

def findLDCount(datals,locid,radius):
    loc1ls, loc2ls = findInnerloc(datals,locid,radius)
    if (loc1ls is not None and  loc2ls is not None )\
               and (len(loc1ls) != 0 and len(loc2ls) != 0):
        dict1 = {}
        dict2 = {}
        cat = ['P','H','R','C','S']
        res = []
        for i in cat:
            counter = 0
            for item in loc1ls:
                if item[3] == i:
                    counter += 1
                dict1[i] = counter
        res.append(dict1)
        for i in cat:
            counter = 0
            for item in loc2ls:
                if item[3] == i:
                    counter += 1
                dict2[i] = counter
        res.append(dict2)
        return res
    else:
        print("There is no point in the region C1 or C2")
        return None

def findSimcore(LDCountres):
    dict1_values = list(LDCountres[0].values())
    dict2_values = list(LDCountres[1].values())
    melo = 0
    for i in range(len(dict1_values)):
        mult = dict1_values[i] * dict2_values[i]
        melo +=mult
    deno1 = 0
    deno2 = 0
    for item in dict1_values:
        deno1 += item **2
    for item in dict2_values:
        deno2 += item **2
    res =format( melo / ((deno1 ** 0.5) * (deno2 ** 0.5)), '.4f')
    return res

def findDCommon(datals, locid, radius):
    loc1, loc2 = findLocs(datals, locid)
    loc1_x, loc1_y = float(loc1[1]), float(loc1[2])
    loc2_x, loc2_y = float(loc2[1]), float(loc2[2])
    locls = []

    for item in datals:
        x = float(item[1])
        y = float(item[2])
        dis1 = ((abs(loc1_x - x) ** 2 + abs(loc1_y - y) ** 2) ** 0.5)
        dis2 = ((abs(loc2_x - x) ** 2 + abs(loc2_y - y) ** 2) ** 0.5)
        if dis1 <= float(radius) and dis2 <= float(radius):
            locls.append(item)
    cat = ['P', 'H', 'R', 'C', 'S']
    dict = {}
    print(locls)
    for i in cat:
        res = []
        for item in locls:
            if item[3] == i:
                res.append(item[0])
        dict[i] = res
    return dict









def main(inputFile,locid,radius):
    try:
        input_data = open(inputFile, 'r')
    except:
        print("File Nod Found")
        return None, None, None, None
    inputdata = input_data.read()
    input_data.close()
    data = list(inputdata.strip().split('\n'))
    data[0] = data[0].split(',')
    header = ['LocId', 'Latitude', 'Longitude', 'Category', 'Reviews', 'RankReview']

    if not set(header).issubset(set(data[0])):
        print('Some necessary columns are missing.')
        return None, None, None, None
    locid_idx = 0
    latitude_idx = 1
    longitude_idx = 2
    category_idx = 3
    reviews_idx = 4
    rankReview_idx = 5
    headerls = []
    for item in range(len(data[0])):
        if data[0][item] == "LocId":
            headerls.append(locid_idx)
        elif data[0][item] == 'Latitude':
            headerls.append(latitude_idx)
        elif data[0][item] == 'Longitude':
            headerls.append(longitude_idx)
        elif data[0][item] == 'Category':
            headerls.append(category_idx)
        elif data[0][item] == 'Reviews':
            headerls.append(reviews_idx)
        elif data[0][item] == 'RankReview':
            headerls.append(rankReview_idx)
    datals = []
    for i in range(1 ,len(data)):
        data[i] = data[i].split(',')
        tmp = []
        for j in headerls:
            tmp.append(data[i][j])
        datals.append(tmp)

    LDCountres = findLDCount(datals, locid, radius)
    SimScoreres = findSimcore(LDCountres)
    DCommonres =  findDCommon(datals, locid, radius)



main("Locations.csv", ["L26", "L52"], 3.5)