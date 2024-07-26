from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    if request.method=="POST":
        n=request.POST['name']
        m=request.POST['mail']
        p1=request.POST['psw1']
        p2=request.POST['psw2']
        if p1==p2:
            if User.objects.filter(username=n).exists():
                messages.info(request,"Username Exists")
                return render(request, "register.html")
            elif User.objects.filter(email=m).exists():
                messages.info(request,"Email Exists")
                return render(request, "register.html")
            else:
                user=User.objects.create_user(username=n,email=m,password=p2)
                user.save()
            return redirect('login')
        else:
            messages.info(request,"Password Not Matched")
            return render(request, "register.html")
    return render(request, "register.html")

def login(request):
    if request.method=="POST":
        n=request.POST['name']
        p2=request.POST['psw2']
        user=auth.authenticate(username=n,password=p2)
        if user is not None:
            auth.login(request,user)
            return redirect('/customer/index')
        else:
            messages.info(request,"Invalid Credentials")
            return render(request,"login.html")
    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect('/customer/index')

def sentimentdata(request):
    if request.method=="POST":
        unnamed=int(request.POST['unnamed'])
        texted=request.POST['texted']
        user=request.POST['user']
        platform=request.POST['platform']
        hashtags=request.POST['hashtags']
        retweets=int(request.POST['retweets'])
        likes=int(request.POST['likes'])
        country=request.POST['country']
        year=int(request.POST['year'])
        month=int(request.POST['month'])
        day=int(request.POST['day'])
        hour=int(request.POST['hour'])
        from sklearn.preprocessing import LabelEncoder
        l=LabelEncoder()
        texted1=l.fit_transform(texted)
        user1=l.fit_transform(user)
        platform1=l.fit_transform(platform)
        hashtags1=l.fit_transform(hashtags)
        country1=l.fit_transform(country)
        import pandas as pd
        df=pd.read_csv(r"static/dataset/sentiment_data.csv")
        print(df.head())
        print(df.isnull().sum())
        print(df.dropna(inplace=True))
        texted=l.fit_transform(df["texted"])
        user=l.fit_transform(df["User"])
        platform=l.fit_transform(df["Platform"])
        hashtags=l.fit_transform(df["Hashtags"])
        country=l.fit_transform(df["Country"])
        df=df.drop(["texted","User","Platform","Hashtags","Country"],axis=1)
        df["texted"]=texted
        df["User"]=user
        df["Platform"]=platform
        df["Hashtags"]=hashtags
        df["Country"]=country
        print(df.head())
        df=df.drop("Timestamp",axis=1)
        print(df.head())
        X=df.drop("Sentiment",axis=1)
        y=df["Sentiment"]
        from sklearn.model_selection import LogisticRegression
        log=LogisticRegression()
        log.fit(X,y)
        import numpy as np
        data=np.array([[unnamed,texted1,user1,platform1,hashtags1,retweets,likes,country1,year,month,day,hour]])
        sentiment=log.sentiment(data)
        print(sentiment)
        return render(request,"sentiment.html",{"unnamed":unnamed,"texted":texted,"user":user,"platform":platform,"hashtags":hashtags,"retweets":retweets,"likes":likes,"country":country,"year":year,"month":month,"day":day,"hour":hour,"sentiment":sentiment})
    return render(request, "sentimentdata.html")

def sentiment(request):
    return render(request,"sentiment.html")