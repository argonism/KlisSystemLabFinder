from bottle import route, run, template, redirect, request,HTTPResponse
import sqlite3
import json
# / にアクセスしたら、index関数が呼ばれる

#選択肢のカテゴリーと質問をinput,オススメの研究室をoutput----
@route("/search", method=["GET","POST"])
def rec_1():
    #jsonデータを受け取る.
    rec_data_1 = request.json["tags"]
    teachers=rec_data_1
    print(rec_data_1)
    print(request.method)
    #ques=rec_data_1[1]
    #-------------------計算part1
    conn = sqlite3.connect("finder.db")
    c = conn.cursor()
    teachers_list = []
    for tea in teachers:
        sel = "select distinct name from teacher where id=?"
        data=tea

        c.execute(sel,str(data))
        for row in c.fetchall():
            teachers_list.append(row)

    conn.close()
    #-----part2
    for tea in teachers_list:

        print(tea[0])


    output_1 = {"message": "OK"}
    #------out(dict)----------------
    header = {"Content-Type": "application/json"}
    res_1 = HTTPResponse(status=200, body=teachers_list, headers=header)
    return res_1
#------------
@route("/get/questions",method="GET")
def get_2():
    conn = sqlite3.connect("finder.db")
    c = conn.cursor()
    select = "select id,question , op_text , op_num from questions"
    question_list=[]
    for row in c.execute(select):
        question_list.append({
            "id":row[0],
            "text":row[1],
            "options":[{
            "title":row[2],
            "value":row[3]
            }
            ]
        })
    conn.close()
    header = {"Content-Type": "application/json"}
    res_3 = HTTPResponse(status=200, body=question_list, headers=header)
    question_json=json.dumps(question_list,ensure_ascii=False)
    return {question_json}
#----------------





@route("/get/tags",method="GET")
def get_1():
    #jsonデータを受け取る.
    conn = sqlite3.connect("finder.db")
    c = conn.cursor()
    select = "select id,category from bigcategory "
    category_list=[]
    for row in c.execute(select):
        category_list.append({
            "id":row[0],
            "category":row[1]
        })
    conn.close()
    header = {"Content-Type": "application/json"}
    res_2 = HTTPResponse(status=200, body=category_list, headers=header)
    category_json=json.dumps(category_list,ensure_ascii=False)
    return {category_json}
# テスト用のサーバをlocalhost:8080で起動する
run(host="localhost", port=8080, debug=True, reloader=True)



request.json
