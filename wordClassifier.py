import re
import string
from prettytable import PrettyTable

# Membuat Function untuk mengecek apakah suatu kata cocok dengan suatu regex
def isMatch(regex,word):
    return True if re.match(regex,word) else False

# terima_kasih --> terimakasih
def removeUnderscore(userInputDirty):
    cleanUserInput = []
    for word in userInputDirty:
        word = word.replace('_','')
        cleanUserInput.append(word)
    return cleanUserInput

# buku -->  alphanumerik, objek
# samuel --> alphanumerik, nama
def classify(userInput: list,regexDict: dict):
    # membuat list untuk menyimpan output
    output = []
    # iterasi semua kata satu per satu dan mengecek apakah kata tersebut "belong" dalam suatu regex
    for word in userInput:
        # karena satu kata bisa termasuk satu atau lebih regex maka buat list category untuk menampung semua kemungkinan yang mungkin
        category = []
        # proses matching
        for (regex,reStr) in regexDict.items():
            if isMatch(regex,word):
                category.append(reStr)
        # jika list category kosong, maka kata tersebut tidak termasuk ke kelas manapun
        if len(category) == 0:
            category.append('unknown')
        output.append(category)
    return output

# menampilkan input dan output dalam format tabel
def detailOutput(userInput: list,output: list):
    outputTable = PrettyTable(["Input","Output"])
    for word,outputList in zip(userInput,output):
        outputTable.add_row([word,outputList])
    return outputTable

# remove semua white space yang ada pada file txt
def removeWhiteSpace(text:list):
    noSpacePartikel = []
    for word in text:
        word = word.replace(' ','')
        noSpacePartikel.append(word)
    return noSpacePartikel


def generateUpperCaseList():
    upperCaseLetters = string.ascii_uppercase
    upperCaseLetters = [letter for letter in upperCaseLetters]
    return upperCaseLetters

def readTxtFile(txtFileName):
    with open(txtFileName) as f:
        theFile = f.readlines()
    return theFile

def processTxtFile(theFile):
    cleanFile = []
    for word in theFile:
        word = word.replace('\n',' ')
        cleanFile.append(word)
    return cleanFile

def convertToRegex(finalCleanObject:list):
    finalCleanObject = set(list(finalCleanObject))
    regex = ''
    for word in finalCleanObject:
        word = word.lower() 
        regex += word+'|'
    regex = regex[:-1]
    regex+=')$'
    depan = '^('
    regex = depan + regex
    return regex
    
def makePartikelRegex(txtFile):
    upperCaseLetters = generateUpperCaseList()
    partikel = readTxtFile(txtFile)
    cleanPartikel = processTxtFile(partikel)
    noSpacePartikel = removeWhiteSpace(cleanPartikel)
    finalPartikel = [word for word in noSpacePartikel if word not in upperCaseLetters]
    theRegex = convertToRegex(finalPartikel)
    return theRegex

def makeObjectRegex(txtFile):
    objects = readTxtFile(txtFile)
    cleanObjects = processTxtFile(objects)
    noSpaceObjects = removeWhiteSpace(cleanObjects)
    theRegex = convertToRegex(noSpaceObjects)
    return theRegex

def makePredicateRegex(txtFile):
    predicate = readTxtFile(txtFile)
    predicate = processTxtFile(predicate)
    predicate = removeWhiteSpace(predicate)
    theRegex = convertToRegex(predicate)
    return theRegex

def makeSubjectRegex(txtFile):
    subject = readTxtFile(txtFile)
    subject = processTxtFile(subject)
    subject = removeWhiteSpace(subject)
    theRegex = convertToRegex(subject)
    return theRegex

if __name__ == '__main__':
    # membuat semua regex dan memasukkan nya kedalam dictionary regexDict
    bulatRE = '^((\-[0-9]+)|(\+[0-9]+)|([0-9]+))$'
    pecahRE = '^((\-[0-9]+\.[0-9]+)|(\+[0-9]+\.[0-9]+)|([0-9]+\.[0-9]+))$'
    emailRE = '^([a-z0-9_]+@gmail\.com)$'
    alphanumRE = '^(\w+)$'
    bulanRE = '''^(((J|j)((A|a)(N|n)(U|u)(A|a)(R|r)|(U|u)(N|n|L|l))(I|i))|((M|m)((A|a)(R|r)(E|e)(T|t)|(E|e)(I|i)))|((((S
    |s)(E|e)(P|p)(T|t))|((N|n)(O|o)(V|v))|((D|d)(E|e)(S|s)))((E|e)(M|m))((B|b)(E|e)(R|r)))|((F|f)(E|e)(B
    |b)(R|r)(U|u)(A|a)(R|r)(I|i))|((O|o)(K|k)(T|t)(O|o)(B|b)(E|e)(R|r))|((A|a)((G|g)(U|u)(S|s)(T|t)(U|u)(
    S|s)|(P|p)(R|r)(I|i)(L|l))))$'''
    hariRE = '^(senin|selasa|rabu|kamis|jumat|sabtu|minggu)$'
    temanRE = '^(samuel|evan|stephen|stefannus|jason)$'
    ibukotaRE = '^(jakarta|banda aceh|ajang|padang|pekanbaru|jambi|palembang|bengkulu|bandar lampung|pangkal pinang|tanjung pinang|yogyakarta|bandung|semarang|surabaya|serang|denpasar|kupang|mataram|pontianak|palangka raya|banjarmasin|samarinda|tanjung selor|manado|palu|makassar|kendari|mamuju|gorontalo|ambon|sofifi|jayapura|manokwari)$'
    subjectRE = makeSubjectRegex('./txtFiles/subject.txt')
    predicateRE = makePredicateRegex('./txtFiles/predikat.txt')
    objectRE = makeObjectRegex('./txtFiles/object.txt')
    partikelRE = makePartikelRegex('./txtFiles/partikel.txt')
    
    regexDict = {bulatRE:'angka_bulat',pecahRE:'angka_pecahan',emailRE:'email',alphanumRE:'alphanumeric',bulanRE:'bulan',hariRE:'hari',temanRE:'nama',ibukotaRE:'ibu_kota',subjectRE:'subyek',predicateRE:'predikat',objectRE:'obyek',partikelRE:'partikel'}
    
    print('\nCara Input: Kata yang terpisah di pisah dengan "_". Contoh: terima_kasih')
    # userInput = input('Enter Your Text: ').lower()
    userInput = 'Samuel pergi ke Yogyakarta tanggal 10 juni sambil membawa buku kerikil orang entitas fisik objek fisik pinata tempat planet proyektil proyektil Properti wadah memprotes maka makanya makin malah manakala manalagi mangkanya manira mari maupun jakarta kendari mamuju menggoda menakuti uji terima_kasih mencair berpikir bintang_neutron stefannus14'
    userInput = userInput.lower()
    userInputSplit = userInput.split(' ')
    userInputSplit = removeUnderscore(userInputSplit)
    output = classify(userInputSplit,regexDict)
    print(f'\nInput:\n{userInput}\n')
    print(f'Output:\n{output}\n')
    print('Detail Output:')
    detailOutputTable = detailOutput(userInputSplit,output)
    print(detailOutputTable)
    print()


