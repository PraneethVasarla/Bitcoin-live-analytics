from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import quandl, math, datetime
import numpy as np
from sklearn import preprocessing, svm,  model_selection
from sklearn.linear_model import LinearRegression
import webbrowser
import tkinter.simpledialog as dialog
import tkinter.messagebox as msgbox
import smtplib
from sentiment import *
from Gif import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText
from email.mime.base import  MIMEBase
from email import encoders
from Wordcloud import *


def donothing():
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()

def showTrend():
    webbrowser.open("https://trends.google.com/trends/explore/GEO_MAP?q=bitcoin&hl=en-US&sni=2")

def showTrend2():
    webbrowser.open('https://trends.google.com/trends/explore/TIMESERIES?date=today+5-y&q=bitcoin&hl=en-US&sni=2')

df=quandl.get("BCHARTS/LOCALBTCINR", authtoken="fsdVx3hHeZnaGysZE_hA")


#mailId= StringVar
def about():
    info= msgbox.showinfo('About','This Application has been created and developed by Praneeth Vasarla')

def help():
    help=Toplevel(root)
    text2=Text(help)
    file= open('README.txt')
    text2.insert(INSERT,file.read())
    text2.insert(END,'')
    text2.pack()


def show_fake():
    text=Text(root)
    text.insert(INSERT,'FAKE TEXT!!!')
    text.insert(END,'ENDED')
    text.pack()

def show_data():
    #print(df)
    abc = Toplevel(root)
    text=Text(abc)
    text.insert(INSERT,df)
    text.insert(END,'The end of data')
    text.pack()




def source():
    webbrowser.open('https://www.quandl.com/data/BCHARTS/LOCALBTCINR-Bitcoin-Markets-localbtcINR')


def BTC_predict():
    df = quandl.get("BCHARTS/LOCALBTCINR", authtoken="fsdVx3hHeZnaGysZE_hA")
    # df=pd.read_csv('btc.csv')
    df['HL_pct'] = (df['High'] - df['Low']) / df['Low'] * 100
    df['PCT_Change'] = (df['Close'] - df['Open']) / df['Open'] * 100

    df = df[['Close', 'HL_pct', 'PCT_Change']]
    forecast_col = 'Close'
    df.fillna(-99999, inplace=True)
    forecast_out = 20
    df['label'] = df[forecast_col].shift(-forecast_out)
    #print(df.tail())

    X = np.array(df.drop(['label'], 1))
    X = preprocessing.scale(X)
    X_lately = X[-forecast_out:]
    X = X[:-forecast_out]

    df.dropna(inplace=True)
    y = np.array((df['label']))
    y = np.array(df['label'])

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)
    # clf = svm.SVR(kernel='linear')
    clf = LinearRegression()
    clf.fit(X_train, y_train)
    accuracy = math.ceil((clf.score(X_test, y_test) * 100))
    forecast_set = clf.predict(X_lately)




    msgmain = "The approximate BTC price in INR for the next 20 days is expected to be " + str(
        forecast_set).strip('[]') + " with an accuracy of " + str(accuracy) + "%"
    df['Forecast'] = np.nan
    ld = df.iloc[-1].name
    lu = ld.timestamp()
    od = 86400
    nu = lu + od



    for i in forecast_set:
        nd = datetime.datetime.fromtimestamp(nu)
        nu += od
        df.loc[nd] = [np.nan for _ in range(len(df.columns) - 1)] + [i]


    df['Close'].plot()
    df['Forecast'].plot()
    prediction = Toplevel(root)
    text = Text(prediction)
    text.insert(INSERT, msgmain)
    text.insert(END, '\n\n')
    text.pack()
    plt.legend(loc=4)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.savefig('Bitcoin_Prediction', bbox_inches='tight')
    plt.show()

    def mail_me():
       fromaddr = "praneethvaasarla@gmail.com"
       name = dialog.askstring('Mail Id', 'Please enter your mail ID')
       toaddr = name
       msg = MIMEMultipart()
       msg['From'] = fromaddr
       msg['To'] = toaddr
       msg['Subject'] = "Expected price of bitcoin"
       body = msgmain
       msg.attach(MIMEText(body, 'plain'))
       filename = "Bitcoin_Prediction.png"
       attachment = open("E:\\Programming\\Data_Analytics\\BTC_GUI\\Bitcoin_Prediction.png", "rb")
       p = MIMEBase('application', 'octet-stream')
       p.set_payload((attachment).read())
       encoders.encode_base64(p)
       p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
       msg.attach(p)
       s = smtplib.SMTP('smtp.gmail.com', 587)
       s.starttls()
       s.login(fromaddr, "pransun1825")
       text = msg.as_string()
       s.sendmail(fromaddr, toaddr, text)
       s.quit()


    MailMe = Button(prediction, text='Mail Me!', command=mail_me)
    MailMe.pack(fill='none', expand= 'true')
    MailMe.place(relx=.5, rely=.5, anchor="center")

root = Tk()
root.configure(bg= '#dedede')
root.geometry('600x500')
root.title("Bitcoin Value Predictor and sentiment estimator")
menubar = Menu(root)


#INTRO PAGE
label=Label(root, text= 'Welcome to Bitcoin Paradise', fg= 'red', font=('Lucida Calligraphy', 18),bg='#dedede')
label1=Label(root, text= "Everything trending about bitcoin,now at your finger tips!!", fg='black',font=('Lucida Calligraphy',13), bg= '#dedede')
label1.place(x=19,y=95)
#3399ff
label.place(x=93, y= 35)


gif = Gif(root, gif="bitcoin_rotate.gif")
gif.pack(fill='none', expand='true')
gif.place(relx=.5, rely= .5, anchor="center")
gif.animate(threaded=False, interval=10, n_repeats=-1)


helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=help)
helpmenu.add_command(label="About...", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)


newmenu=Menu(menubar,tearoff=0)
newmenu.add_command(label='Google stock',command=donothing())


btcmenu= Menu(menubar, tearoff=0)
menubar.add_cascade(label='Explore',menu=btcmenu)
btcmenu.add_command(label='Predict',command=BTC_predict)
btcmenu.add_command(label='Data',command=show_data)
btcmenu.add_command(label='Source',command=source)
btcmenu.add_command(label='Trend Cloud', command=cloud)
btcmenu.add_command(label='Sentiment',command=senti)
btcmenu.add_command(label='Interest over region', command=showTrend)
btcmenu.add_command(label='Interest over time', command=showTrend2)


root.iconbitmap(r'E:\Programming\Data_Analytics\GUI_test\Papirus-Team-Papirus-Apps-Bitcoin.ico')
root.config(menu=menubar)
root.mainloop()