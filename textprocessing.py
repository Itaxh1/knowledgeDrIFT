
#_________________________________TEXT CLEANING AND PREPROCESSING_____________________________________________
def txtclean(text):
    keyword=['who','when','what','where','how','?','!','...','please','?','#','thanks', 'RIP', 'love', 'thank','helpful']
    text = text.split('\n')
    count = 0
    count1 = 0
    str4 = ''
    #print(len(text))
    for i in text:
        clean = True
        if(len(i)>5):
            count += 1
            #str4 += i + '\n\n'
            for word in keyword:
                if word in i.lower():
                    clean = False
            if clean == True:
                count1 += 1
                str4 += i + '\n\n'
    #print(count)

    #cleddprint(count1)
    return str4


