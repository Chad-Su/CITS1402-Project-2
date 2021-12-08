def readfile(inputFile):
    '''
    :param inputFile: takes the file name as an argument
    :return: a list of all rows

    If the file can be opened, reads the data in the file. Otherwise the
    prompt cannot findthe file and returns None
    After reading the file, the readFile () adjusts the title on the first
    line of the file in case and order, and if all titles are met, stores
    each row in a list and return a large list which contain all the sublist
    '''
    try:
        input_data = open(inputFile, 'r')
    except:
        print("File Nod Found")
        return None
    inputdata = input_data.read()
    input_data.close()
    data = list(inputdata.strip().split('\n'))
    data[0] = data[0].split(',')
    new =[]
    for i in data[0]:
        i = i.lower()
        new.append(i)
    data[0] = new
    header = ['locid','latitude','longitude','category','reviews','rankreview']
    if not set(header).issubset(set(data[0])):
        print('Some necessary columns are missing.')
        return None

    locid_idx = 0
    latitude_idx = 1
    longitude_idx = 2
    category_idx = 3
    reviews_idx = 4
    rankReview_idx = 5
    headerls = []
    for item in range(len(data[0])):
        if data[0][item].lower() == "locid":
            headerls.append(locid_idx)
        elif data[0][item].lower() == 'latitude':
            headerls.append(latitude_idx)
        elif data[0][item].lower() == 'longitude':
            headerls.append(longitude_idx)
        elif data[0][item].lower() == 'category':
            headerls.append(category_idx)
        elif data[0][item] == 'reviews':
            headerls.append(reviews_idx)
        elif data[0][item].lower() == 'rankreview':
            headerls.append(rankReview_idx)
    datals = []
    for i in range(1 ,len(data)):
        data[i] = data[i].split(',')
        tmp = []
        for j in headerls:
            tmp.append(data[i][j])
        datals.append(tmp)
    return datals

def findLocdtl(filedata, locid):
    '''
    :param filedata: a list contain the all data.
    :param locid: the name of the location where we want to query.
    :return: a list of all information on the row.

    FindLocdtl (filedata, locid) checks whether the location number
    at index = 0 in each row is the same as the entered location number.
    If so, it returns a list of all information on the row where the
    locid resides.
    '''
    for item in filedata:
        if item[0].upper() == locid:
            loc = item
            return loc

def findCategory(locls):
    '''
    :param locls: A filtered list that contains the entire line of information
                  for all the specified LocId in the file.
    :return: A dictionary， that takes all location category information as
             keys and the number of occurrences of the corresponding
             location category in the argument list as value.
    '''
    dic = {}
    cat = ['P', 'H', 'R', 'C', 'S']
    for i in cat:
        counter = 0
        for item in locls:
            if item[3].upper() == i:
                counter += 1
            dic[i] = counter
    return dic

def calculate(loc_x,loc_y,target_x,target_y):
    '''
    :param loc_x: Latitude of the main function location argument locIDx.
    :param loc_y: Longitude of the main function location argument locIDx.
    :param target_x: The latitude of the point to be calculated.
    :param target_y: The longitude of the point to be calculated.
    :return: A flost number, which is  euclidean distrance bewteen two
             locations.
    '''
    loc_x = float(loc_x)
    loc_y = float(loc_y)
    target_x = float(target_x)
    target_y = float(target_y)
    distance = ((abs(loc_x - target_x) ** 2 + abs(loc_y - target_y) ** 2) ** 0.5)
    return distance

def findLocs(filedata,locid,radius):
    '''
    :param filedata: a list contain the all data.
    :param locid: The central location number ’LocId‘ of the circular area
                  to be calculated.
    :param radius: The radius of the circular region to be calculated.
    :return: If LocId exists, return a list of all points in the circle
             with LocId as the center and radius argument as the radius of
             the circle.
             If LocId does not exist, None is returned

    If the center coordinates exist,
    call the calculate(loc_x,loc_y,target_x,target_y) function to
    calculate and obtain all the points within  circular region。
    '''
    loc = findLocdtl(filedata, locid)
    if loc is not None:
        loc_x, loc_y = loc[1],loc[2]
        locls = []
        for item in filedata:
            if calculate(loc_x, loc_y,item[1], item[2]) <= radius:
                locls.append(item)
        return locls
    else:
         return None

def findLDCount(filedata,locids,radius):
    '''
    :param filedata: The name of the CSV file containing the information and
                     record about the location points which need to be analysed.
    :param locids: an input parameter that accepts a list of two strings
                   which represent two location IDs.
    :param radius: the numeric input parameter that defines a circular boundary
                   around the location IDs provided in queryLocId.
    :return: Return a list containing two dictionaries, where the keys in the
             dictionaries are the location categories, and their values contain the
             number of locations for respective category in their regions.

    If the locids contain both location IDs, the result is returned,
    otherwise None is returned
    '''
    loc1ls = findLocs(filedata,locids[0],radius)
    loc2ls = findLocs(filedata,locids[1],radius)
    if (loc1ls and loc2ls) is not None :
        dict1 = findCategory(loc1ls)
        dict2 = findCategory(loc2ls)
        res = []
        res.append(dict1)
        res.append(dict2)
        return res
    else:
        return None

def findSimcore(filedata,locids,radius):
    '''
    :param filedata: The name of the CSV file containing the information and
                     record about the location points which need to be analysed.
    :param locids: an input parameter that accepts a list of two strings
                   which represent two location IDs.
    :param radius: the numeric input parameter that defines a circular boundary
                   around the location IDs provided in queryLocId.
    :return: Return the float type cosine similarity of the regions C1 and C2
             based on the category-wise number of locations identified inside
             each region.
    '''
    dictls = findLDCount(filedata,locids,radius)

    dict1_values = list(dictls[0].values())
    dict2_values = list(dictls[1].values())
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
    res =round(float( melo / ((deno1 ** 0.5) * (deno2 ** 0.5))),4)
    return res

def findDCommon(filedata, locid, radius):
    '''
    :param filedata: The name of the CSV file containing the information and
                     record about the location points which need to be analysed.
    :param locids: an input parameter that accepts a list of two strings
                   which represent two location IDs.
    :param radius: the numeric input parameter that defines a circular boundary
                   around the location IDs provided in queryLocId.
    :return: Return a dictionary of category based on the common location IDs
             existing in the regions C1 and C2.
    '''
    regionC1 = findLocs(filedata, locid[0], radius)
    regionC2 = findLocs(filedata, locid[1], radius)
    interls = []
    for item in regionC1:
        if item in regionC2:
            interls.append(item)
    cat = ['P', 'H', 'R', 'C', 'S']
    dict = {}
    for i in cat:
        res = []
        for item in interls:
            item[3] = item[3].upper()
            if item[3] == i:
                res.append(item[0])
        dict[i] = res
    return dict



def alldistance(locls,loc):
    '''

    :param locls: A list of all points in the circle of LocId.
    :param loc: The center LocId of a circular area
    :return: A dictionary which contain the category as key, position ID
             and distance as value of all points in the circular region
             from the center point.
    '''
    cat = ['P', 'H', 'R', 'C', 'S']
    loc_x = loc[1]
    loc_y = loc[2]
    dic = {}
    for i in cat:
        valuels = []
        for item in locls:
            item[3] = item[3].upper()
            if item[3] == i and item[0] != loc[0]:
                target_x = item[1]
                target_y = item[2]
                dis= round(calculate(loc_x,loc_y,target_x,target_y), 4)
                tmp = (item[0],dis)
                valuels.append(tmp)
        if len(valuels) != 0:
            dic[i] = valuels
    return dic

def sortdic(dic):
    '''
    :param dic: A dictionary which contain the distance and position IDS
                of all points in the circular region from the center point.
    :return: The closest distance and location ids from each location
             category to the center point in the circular region.
    '''
    for key in dic:
        values = dic.get(key)
        sorted_by_second = sorted(values, key=lambda tup: tup[1])
        dic[key] = sorted_by_second[0]
    return dic

def findclose(filedata, locids, radius):
    '''
    filedata: The name of the CSV file containing the information and
              record about the location points which need to be analysed.
    :param locids: An input parameter that accepts a list of two strings
                   which represent two location IDs.
    :param radius: the numeric input parameter that defines a circular boundary
                   around the location IDs provided in queryLocId.
    :return: The closest distance and location ids from each location category
             to the center point in the circular region.
    By call findLocs(filedata, locid, radius) function to get the center
    location information.
    By call  alldistance(locls,loc) to get the distance and position IDS
    of all points in the circular region from the center point.
    By call sortdic(dic) to get closest distance and location ids from
    each location category to the center point in the circular region.
    '''
    loc1ls = findLocs(filedata, locids[0], radius)
    loc2ls = findLocs(filedata, locids[1], radius)
    alldis1 = alldistance(loc1ls,findLocdtl(filedata, locids[0]))
    alldis2 = alldistance(loc2ls, findLocdtl(filedata, locids[1]))
    sorted1 = sortdic(alldis1)
    sorted2 = sortdic(alldis2)
    return sorted1, sorted2

def main(inputFile = '',locids = '',radius = ''):
    if (not isinstance(inputFile,str)\
            or not isinstance(locids, list)\
            or not isinstance(radius,(int,float))):
        print("Invelld input arguments")
        return None, None, None, None
    else:
        filedata = readfile(inputFile)
        if filedata is not None:
            if len(locids) != 2:
                print("LocId list input may wrong")
                return None, None, None, None
            elif radius < 0:
                print("Radius must large or equal to 0")
                return None, None, None, None
            else:
                findLDCountres = findLDCount(filedata, locids, radius)
                if findLDCountres is None:
                    print("Can not find locids in C1 or C2 ")
                    return None, None, None, None,
                else:
                    findSimcoreres = findSimcore(filedata, locids, radius)
                    findDCommonres = findDCommon(filedata, locids, radius)
                    findcloseres = findclose(filedata, locids, radius)
                    return findLDCountres, findSimcoreres, findDCommonres,findcloseres
        else:
            return None, None, None, None

'''if __name__ == '__main__':
     LDCount1, simScore1, DCommon1, LDClose1 = main("Locations.txt", ["L89", "L15"],4.3)
     print('LDCount1\n',LDCount1,'\n','simScore1\n',simScore1,'\n', 'DCommon1\n',DCommon1,'\n', 'LDClose1\n',LDClose1)'''

