import time

workout_list = {'pullup':50 , 'pushup':50 , 'dumbbellcurl':50 }

def init_workout_files():
    for workout in workout_list.keys():
        with open('textfile/'+workout+'_tmp.txt', 'w', encoding = 'utf-8') as file:
            file.write('0')
        with open('textfile/'+workout+'_total.txt', 'w', encoding = 'utf-8') as file:
            file.write('0')

def checkday(date):#날짜가 달라지면 return 1
    
    tmp_date = int(time.strftime('%d', time.localtime(time.time())))
    if date != tmp_date:
        date = tmp_date
        return 1
    else:
        return 0
