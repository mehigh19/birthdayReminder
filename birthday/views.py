from django.http import HttpResponse, HttpRequest, Http404
from django.template import loader
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, date
import os, time, threading, schedule
from django.core.mail import send_mail

def home(request):
    content = ""
    userSearch = ""
    records = birthDay.objects.all()
    if len(records) == 0:
        content="No data available"
    else:
        content=content+ f'''
            <div class="div_container fontF listBdays">
                <div class="div_line "> Name </div> 
                <div class="div_line ">Birthday Date </div>
            </div> <br>
                            '''
        
        for i in range(len(records)):
            content=content+ f'''
            <form method="GET">
                <div class="div_container fontF listBdays">
                    <div class="div_line "> {records[i].name} </div> 
                    <div class="div_line ">{str(records[i].bDayDate)}</div>
                    
                    <input type="submit" formaction="deleteBday" value="" class="delete-button action-button">
                    <input type="submit" formaction="editBdayHtml" value="" class="edit-button action-button">
                    
                    <input type="hidden" name="id" value="{records[i].id}">
                    <input type="hidden" name="nameBday" value="{records[i].name}">
                    <input type="hidden" name="dateBday" value="{str(records[i].bDayDate)}">
                </div>
            </form>
                            '''
    return render(request, 'birthday/index.html', {'content': content})

def addBdayHtml(request):
    template = loader.get_template('birthday/addBday.html')
    return HttpResponse(template.render({}, request))

def addBday(request: HttpRequest):
    name = request.GET.get('name')
    date = request.GET.get('date')

    if name and date:
        newBday = birthDay()
        newBday.name = name
        newBday.bDayDate = date
        newBday.save()
        return HttpResponse(f"Date Added:<br>Name: {name}<br>Birthday: {date} <br> <br> <a href='addBdayHtml'> BACK </a>")
    else:
        return HttpResponse("Missing name or date", status=400)

def deleteBday(request):
    idBday = request.GET.get('id')
    item = get_object_or_404(birthDay, id=idBday)
    item.delete()
    return redirect('/birthday')

def editBdayHtml(request):
    template = loader.get_template('birthday/editBday.html')
    return HttpResponse(template.render({}, request))


def editBday(request:HttpRequest):
    response=''

    idBday = request.GET.get('id')
    nameBday = request.GET.get('nameBday')
    dateBday = request.GET.get('dateBday')
    bDay = birthDay.objects.filter(id=idBday).first()
    bDay.name = nameBday
    bDay.bDayDate = dateBday
    bDay.save()

    response = response + 'Birthday Modified <br>' + nameBday + '<br>' + dateBday
    return redirect('/birthday')

def upComing(request):
    content = ""
    records = birthDay.objects.all()
    if len(records) == 0:
        content="No data available"
    else:
        content=content+ f'''
            <div class="div_container fontF listBdays">
                <div class="div_line"> Name </div> 
                <div class="div_line"> Birthday Date </div>
            </div> <br>
'''
        currentMonth = str(datetime.today()).split('-')[1]
        for i in range(len(records)):
            birthdayMonth = str(records[i].bDayDate).split('-')[1]
            if currentMonth == birthdayMonth:
                content=content+ f'''
                <form method="GET">
                    <div class="div_container fontF listBdays">
                        <div class="div_line "> {records[i].name} </div> 
                        <div class="div_line"> {str(records[i].bDayDate)} </div>

                        <input type="submit" formaction="deleteBday" value="" class="delete-button action-button">
                        <input type="submit" formaction="editBdayHtml" value="" class="edit-button action-button">
                        
                        <input type="hidden" name="id" value="{records[i].id}">
                        <input type="hidden" name="nameBday" value="{records[i].name}">
                        <input type="hidden" name="dateBday" value="{str(records[i].bDayDate)}">
                    </div>
                </form>
                                '''
                                
    return render(request, 'birthday/upComing.html', {'content': content})

def createTxtFile():
    while True:
        current_time = time.strftime("%H:%M:%S")

        if current_time == '21:40:00' or current_time == '00:00':
            time.sleep(1)
            file_name = f'dbdata_{date.today()}.txt'
            folder_path = os.path.join(os.path.dirname(__file__), 'db_data')
            file_path = os.path.join(folder_path, file_name)
            os.makedirs(folder_path, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as file:
                all_birthdays = birthDay.objects.all()
                for element in all_birthdays:
                    file.write(f"{element.name}, {element.bDayDate}\n")
                print(f'TXT FILE CREATED {file_name}')

def checkBday():
    today = str(date.today())
    today_day = today.split('-')[2]
    today_month = today.split('-')[1]
    current_month = datetime.now().strftime("%B")

    with open(fr'birthday\db_data\dbdata_{today}.txt', 'r') as file:
        for line in file:
            date_list = line.strip().split(',')[1]
            person_name = line.strip().split(',')[0]
            today_bday = date_list.split('-')[2]
            today_bmonth = date_list.split('-')[1]

            if today_bday == today_day and today_bmonth == today_month:
                send_mail(
                    subject='Happy Birthday!',
                    message=f"Today {current_month} {today_bday} is {person_name}'s birthday",
                    from_email='djangop34@gmail.com',
                    recipient_list=[f'{person_name}{today_bday}@exemplu.com'],
                    fail_silently=False
                )
                time.sleep(60)
            else:
                print('There is no-one who was born today')
                time.sleep(60)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every().day.at("21:41").do(checkBday)

t1 = threading.Thread(target=createTxtFile)
t2 = threading.Thread(target=run_schedule)
t1.start()
t2.start()