from prettytable import PrettyTable
S = ["*DBF" , "/DBF" , "+DBF" , "-DBF" , "_VEK" , "_EK"]
B = ["*DBFW" , "/DBFW" , "+DBFW" , "-DBFW" , "(EMW" , "_VEKW" , "_EKW" , "(JTW" , "*DBF" , "/DBF" , "+DBF" , "-DBF" , "(EM" , "_VEK" , "_EK" , "(JT" , "0W" , "1W" , "2W" , "3W" , "4W" , "5W" , "6W" , "7W" , "8W" , "9W" , "0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9"]
W = ["*DBFW" , "/DBFW" , "+DBFW" , "-DBFW" , "(EMW" , "_VEKW" , "_EKW" , "(JTW" , "*DBF" , "/DBF" , "+DBF" , "-DBF" , "(EM" , "_VEK" , "_EK" , "(JT" , "0W" , "1W" , "2W" , "3W" , "4W" , "5W" , "6W" , "7W" , "8W" , "9W" , "0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9", "*DBFWW" , "/DBFWW" , "+DBFWW" , "-DBFWW" , "(EMWW" , "_VEKWW" , "_EKWW" , "(JTWW" , "0WW" , "1WW" , "2WW" , "3WW" , "4WW" , "5WW" , "6WW" , "7WW" , "8WW" , "9WW"]
D = ["_V" , "_"]
V = ["_VV" , "_V" , "_"]
E = ["*DB" , "/DB" , "+DB" , "-DB"]
F = ["_VB" , "_B"]
H = [")"]
J = ["_VE" , "_E"]
K = ["_VBD" , "_BD"]
M = ["_VBH" , "_BH"]
T = ["_VBDH" , "_BDH","_BH"]


bridge = {"S":S, "B":B, "W":W, "D":D, "V":V, "E":E, "F":F, "H":H, "J":J, "K":K, "M":M, "T":T}

pdaDict = ["S", "B", "W", "D", "V", "E", "F", "H", "J", "K", "M", "T"]

def validate(inputString, thestack):
    global isAccept
    # kalau string input sudah kosong dan juga stack kosong maka return True
    if len(inputString) == 0:
        if len(thestack) == 0:
            isAccept = True
        else:
            pass

    else:
        # kalau engga masuk sini

        # kalau stack kosong tapi string inputan belum kosong bomat
        if len(thestack) == 0:
            pass

        # jika string paling awal dari stack adalah non-terminal, maka  dipecah menjadi terminal yang depannya sama dengan depan string
        elif thestack[0] in pdaDict:
            # ini iterasinya
            for i in bridge[thestack[0]]:
                if i[0] == inputString[0]:
                    validate(inputString, i+thestack[1:])

        # jika string paling awal dari stack adalah terminal, dan cocok dengan string awal stack, maka pop
        else:
            if inputString[0] == thestack[0]:
                validate(inputString[1:], thestack[1:])
            
            else:
                pass

def isAccepted(inputString, thestack):
    global isAccept
    isAccept = False
    validate(inputString,thestack)
    return isAccept

def makeTableOutput(testCases, outputList, checkList, expectedList,MathOutput,ExpectedMathOutput,polishChecker):
    outputTable = PrettyTable(["No","Input String","Is Accepted","Should Be Accepted","Check Accepted","Math Output","Expected Math Output","Math Check"])
    index = [i+1 for i in range(len(testCases))]
    testCases = [string.replace('_'," ") for string in testCases]
    for i,inputs,outputs,checks, expecteds, maths, expectmaths,polish in zip(index,testCases, outputList, checkList, expectedList,MathOutput,ExpectedMathOutput,polishChecker):
        outputTable.add_row([i,inputs,outputs,checks,expecteds,maths,expectmaths,polish])
    return outputTable

def makeOutputListAndCheckList(testCases,expected):
    hasil = [isAccepted(test,'S') for test in testCases]
    checkList = []
    for output,expected in zip(hasil,expected):
        if output == expected:
            benerga = '✅'
        else:
            benerga = '❌'
        checkList.append(benerga)
    return hasil,checkList

def calculatePolishNotation(hasil,inputString):
    output = []
    for h,string in zip(hasil,inputString):
        if h:
            string = string.replace("(", "")
            string = string.replace(")", "")
            string = string.replace("_", " ")
            temp = string.split()
            while len(temp) != 1:
                for i in range(len(temp)):
                    try:
                        if temp[i] == "+":
                            hasil = float(temp[i + 1]) + float(temp[i + 2])
                            temp = temp[:i] + [hasil] + temp[i + 3 :]
                        elif temp[i] == "-":
                            hasil = float(temp[i + 1]) - float(temp[i + 2])
                            temp = temp[:i] + [hasil] + temp[i + 3 :]
                        elif temp[i] == "*":
                            hasil = float(temp[i + 1]) * float(temp[i + 2])
                            temp = temp[:i] + [hasil] + temp[i + 3 :]
                        elif temp[i] == "/":
                            hasil = float(temp[i + 1]) / float(temp[i + 2])
                            temp = temp[:i] + [hasil] + temp[i + 3 :]
                    except:
                        continue
            output.append(temp[0])
        else:
            output.append('Rejected')

    return output

def polishChecker(mathOutput, expectedMathOutput):
    output = []
    for math,expected in zip(mathOutput, expectedMathOutput):
        if math == expected:
            output.append('✅')
        else:
            output.append('❌')
    return output

if __name__ == "__main__":
    testCases = [
        '3_+_4', # False
        '+_3_4', # True
        '-_3_4', # True
        '+_(*_3_2)_4', # True
        '-_40_30', # True
        '-_3_2_1', # False
        '*_12_13', # True
        '/_6_8', # True
        '3_*_2_+_4', # False
        '+_(*_3_2)_4', # True
        '+_(_*_3_2_)_4', # True
        '+_*_3_4_2', # True
        '+_(*_3_(-_2_7))_4', # True
        '+_(_*_3_2)_4', # True
        '*_+_1_2_+_3___4', # True
        '+_+_1_*_2_3_4', # True
        '7/6', # False
        '1+2+3', # False
        '+_1_*_2_+_3_4',# True
        '+_*_+_1_2_3_4',# True
        'S', # False
        '+_3_(*_2_3)', # True
        '+_(*_3_2)_4'# True
    ]
    expectedPolish = [
        'Rejected',
        7.0,
        -1.0,
        10.0,
        10.0,
        'Rejected',
        156.0,
        0.75,
        'Rejected',
        10.0,
        10.0,
        14.0,
        -11.0,
        10.0,
        21.0,
        11.0,
        'Rejected',
        'Rejected',
        15.0,
        13.0,
        'Rejected',
        9.0,
        10.0
    ]
    expected = [False,True,True,True,True,False,True,True,False,True,True,True,True,True,True,True,False,False,True,True,False,True,True]
    hasil,checkList = makeOutputListAndCheckList(testCases,expected)
    MathOutput = calculatePolishNotation(hasil,testCases)
    polishCheckerOutput = polishChecker(MathOutput,expectedPolish) 
    outputTable = makeTableOutput(testCases,hasil,expected,checkList,MathOutput,expectedPolish,polishCheckerOutput)
    print(outputTable)