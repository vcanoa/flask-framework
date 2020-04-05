from flask import Flask, render_template, request, redirect

import requests
import json
from pandas import *
import pandas
import matplotlib.pyplot as plt
from datetime import datetime as dt
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter

# male female population
#we read data from an API
response=requests.get('https://www.quandl.com/api/v3/datasets/UGEN/PPRJ_5001.json?api_key=qhTxGYgLa2F4u2aDC47R')
jsn = response.json()
data=jsn[ "dataset"]
list_data=data['data']
# use the panda frame to position the data
df=DataFrame({ 'date':[],
               'female':[],
               'male':[]
})
for row in list_data:
          df=df.append({'date': row[0],'female': row[1],'male': row[2]}, ignore_index=True)

df['date']=to_datetime(df.date)
p = figure(x_axis_type="datetime", title="Women and Men", plot_height=350, plot_width=800)
p.xgrid.grid_line_color=None
p.ygrid.grid_line_alpha=0.5
p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'Number'
p.line(df["date"],df["female"], line_width=2,line_color="blue", legend_label='Females')
p.line(df["date"],df["male"], line_width=2, line_color="green",legend_label='Males')

app = Flask(__name__)

app.vars={}

app.questions={}
app.questions['There are more men or women in the world?']=('men','women')

app.nquestions=len(app.questions)
# should be 1

@app.route('/index_m',methods=['GET','POST'])
def index_m():
#   return 'This is information about health'
    nquestions=app.nquestions
    if request.method == 'GET':
         return render_template('prueba.html',num=nquestions)
    else:
       #request was a POST
        app.vars['name'] = request.form['name_m']
        app.vars['age'] = request.form['age_m']
 
        f = open('%s_%s.txt'%(app.vars['name'],app.vars['age']),'w')
        f.write('Name: %s\n'%(app.vars['name']))
        f.write('Age: %s\n\n'%(app.vars['age']))
        f.close()
 
        return redirect('/main_m')
 
@app.route('/main_m')
def main_m(): 
      if len(app.questions)==0 :
          return show(p)
         #return render_template('end.html')
      else:
         return redirect('/next_m')
   
#####################################
## IMPORTANT: I have separated /next_lulu INTO GET AND POST
## You can also do this in one function, with If and Else
## The attribute that contains GET and POST is: request.met
#####################################

@app.route('/next_m',methods=['GET'])
def next_m():
    # for clarity (temp variables)
      n = app.nquestions - len(app.questions) + 1
      q = list(app.questions.keys())[0] #python indexes at 0
      a1, a2 = list(app.questions.values())[0]

#this will return the answers corresponding to q
 # save the current question key
      app.currentq = q

      return render_template('layout.html',num=n,question=q,ans1=a1,ans2=a2)


@app.route('/next_m',methods=['POST'])
def next_m2():  #can't have two functions with the same name
    # Here, we will collect data from the user.
    # Then, we return to the main function, so it can tell us whether to
    # display another question page, or to show the end page.

     f = open('%s_%s.txt'%(app.vars['name'],app.vars['age']),'a') #a is for append
     f.write('%s\n'%(app.currentq))
     f.write('%s\n\n'%(request.form['answer_from_layout'])) #this was the 'name' on layout.html!
     f.close()
     
     # Remove question from dictionary
     del app.questions[app.currentq]
     
     return redirect('/main_m')


if __name__ == '__main__':
 #app.run(port=33507)
 app.run(debug=True)
