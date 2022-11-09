
import re
from flask import Flask, render_template
from flask import request

app = Flask(__name__)

list=['CandideFr.txt','CandideEn.txt']


file_dic={}


for i in list:
       
        tuple_list=[]

        
        file_open = open(i,'r',encoding="utf-8")
        
        plain_text=file_open.read().lower()

       
        word_result=re.findall("[\W]*([\w\'-]+)[\W]*",plain_text)
        final_list=[]

       
        stop_open=open("stopwords.txt","r",encoding="utf-8")
        stop_text=stop_open.read()
        stop_words=re.findall("\w+",stop_text)
        stop_words=[s.lower() for s in stop_words]

       
        for i in word_result:
                if i not in stop_words:
                    final_list.append(i)

        
        for t in range(len(final_list)):
            count=final_list.count(final_list[t])
            curnt=final_list[t]
            if t==0:
                pre=''
                nxt=final_list[t+1]
            elif t==len(final_list)-1:
                pre=final_list[t-1]
                nxt=''
            else:
                pre=final_list[t-1]
                nxt=final_list[t+1]
            tuple_list.append([pre,curnt,nxt,count])

        
        file_dic.update({i:tuple_list})
        

@app.route('/',methods=["POST","GET"])
def to_index():

    return render_template("index.html",p=final_list)


@app.route('/page1.html',methods=["POST","GET"])
def page1():
    n=request.form['n']
    if request.method=="POST":
        value=[]
        for key in file_dic:
            for i in range(len(file_dic[key])):
                if file_dic[key][i][1]==n:
                    value.append(key)
                    break
    return render_template("page1.html",value=value)


@app.route('/page2.html',methods=["POST","GET"])
def page2():
    if request.method=="POST":
        x= request.form['x']
        word= request.form['word']
        val=0
        for elmnt in file_dic[x]:
            if elmnt[1]==word:
                val=elmnt[3]
                break
        return render_template('page2.html',val=val)


@app.route('/page3.html',methods=["POST","GET"])
def page():
    if request.method=="POST":
        words=request.form['words']
        word_bulk=words
        word_bulk=word_bulk.split()
        wbulk_details=[]
        for word in word_bulk:
            count_both=0
            word_at=[]
            for key in file_dic:
                for i in range(len(file_dic[key])):
                    if file_dic[key][i][1]==word:
                        count_both+=file_dic[key][i][3]
                        word_at.append(key)
                        break
            wbulk_details.append((word,word_at,count_both))
    return render_template("/page3.html",wbulk_details=wbulk_details)


@app.route('/page4.html',methods=["POST","GET"])
def to_page4():
    if request.method=="POST":
        word=request.form['word']
        lines_list=[]
        for i in list:
            file_open = open(i,'r',encoding="utf-8")
            plain_lines=file_open.readlines()
            for line in plain_lines:
                if len(line)>1:
                    words_in=re.findall("[\W]*([\w]+)[\W]*",line)
                    if word in words_in:
                        lines_list.append(line)
    return render_template("/page4.html",lines_list=lines_list)

if __name__ == '__main__':
    app.run(debug =True)