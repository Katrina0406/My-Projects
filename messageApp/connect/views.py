from django.shortcuts import render, HttpResponse
import pymysql.cursors

url = "127.0.0.1"
username = 'root'
password="FXZDYTlhy2580,./"
database = 'student'

#connect database
db = pymysql.connect(host=url, user=username, password=password, db=database,
                         port=3306, charset="utf8")
cursor=db.cursor()
sql = "SELECT user_name, password FROM user"
cursor.execute(sql)
username1, password1 = cursor.fetchone()

# Create your views here.
def logindb(request):
    if request.method == 'POST':
        username_ = request.POST.get('username')
        password_ = request.POST.get('password')
        if username_ == username1 and password_ == password1:
            return render(request, "index.html")
        else:
            return HttpResponse('login fail:(')
    return render(request, "user.html")