import tabula
import csv
import json
import requests
from collections import defaultdict

# Extaer los datos del pdf al DataFrame
# df = tabula.read_pdf("Words_of_the_Champions_Printable_FINAL.pdf")
# lo convierte en un csv llamdo out.csv codificado con utf-8
# df.to_csv('out.csv', sep='\t', encoding='utf-8')


#df = tabula.read_pdf("Words_of_the_Champions_Printable_FINAL.pdf", encoding='utf-8', spreadsheet=True, pages='4-8')
#print ('read complete')
#print (df)
#df.to_csv('output.csv', encoding='utf-8')
#df.to_csv('output.csv', sep=',',encoding='utf-8')

tabula.convert_into("words-3.pdf", "output.csv", output_format="csv", pages='1-6')
print ('read complete')

f = open('output.csv')
csv_f = csv.reader(f)

wordslist = list()
extras = list()

file1 = open("apikey.txt","a") 

for row in csv_f:
    for word in row:
        print(word)
        if len(word) != 0 and "*" not in word and "OR " not in word:
            print("inside if")
            worddict = defaultdict()
            worddict['definition'] = list()

            req = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?" + file1.readline()
            resp = requests.get(req)
            data = resp.json()

            if  "meta" in data[0]:
                worddict['word'] = word
                
                for d in data:
                    if len(d['shortdef']) != 0:
                        worddict['definition'].append(d['shortdef'][0])
                        #print(d['shortdef'][0])
                    else:
                        worddict['definition'].append("None")

                temp = data[0]['hwi'].get('prs', 'None')
                if temp != 'None':
                    worddict['pronounciation'] = data[0]['hwi']['prs'][0]['mw']
                else:
                    worddict['pronounciation'] = "None"
                
                temp = data[0].get('et', 'None')
                if temp != 'None':
                    worddict['etymology'] = temp[0][1]
                else:
                    worddict['etymology'] = "None"

                wordslist.append(worddict)
            else:
                extras.append(word)

#keys = wordslist[0].keys()
#print(wordslist)
#print(keys)
keys = ['word', 'definition', 'pronounciation', 'etymology']
with open('wordswithdef3.csv', 'w', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(wordslist)

print('extras:')
print(extras)
         

""" resp = requests.get(req)
data = resp.json()


wordslist = defaultdict()
wordslist['word'] = "extraterrestrial"
wordslist['definition'] = list()
for d in data:
    
    wordslist['definition'].append(d['shortdef'][0])
wordslist['pronounciation'] = data[0]['hwi']['prs'][0]['mw']
temp = data[0].get('et', 'None')
if temp != 'None':
    wordslist['etymology'] = temp[0][1]
else:
    wordslist['etymology'] = "None" """