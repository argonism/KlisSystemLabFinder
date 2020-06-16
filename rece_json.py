from bottle import route, run, template, redirect, request,HTTPResponse
import sqlite3
import json
# / にアクセスしたら、index関数が呼ばれる

#選択肢のカテゴリーと質問をinput,オススメの研究室をoutput----
@route("/search", method=["GET","POST"])
def rec_1():
    #jsonデータを受け取る.
    rec_data_1 = request.json["tags"]
    rec_data_2=request.json["questions"]
    teachers=rec_data_1
    #print(rec_data_2)
    #print(request.method)
    #ques=rec_data_1[1]
    #-------------------計算part1
    conn = sqlite3.connect("finder.db")
    c = conn.cursor()
    teachers_list = []
    for tea in rec_data_1:
        sel = "select distinct name from teacher where id=?"
        data=tea

        c.execute(sel,(str(tea),))
        for row in c.fetchall():
            teachers_list.append(row)

    conn.close()
    #-----part2
    output_arr=[]
    teacher_set={}
    def cal(arr1,arr2):
        sum_arr=[]
        sum_arr.append((int(arr1[0])-arr2[0])**2)
        sum_arr.append((int(arr1[1])-arr2[1])**2)
        sum_arr.append((int(arr1[2])-arr2[2])**2)
        q_sum=sum(sum_arr)

        return q_sum

    for tea in teachers_list:
        conn = sqlite3.connect("finder.db")
        c = conn.cursor()
        select = "select zemitime,com,seat from facility where name=?"
        data=tea
        #print(tea)
        c.execute(select,(str(tea[0]),))
        for row in c.fetchall():
            comp=cal(rec_data_2,list(row))
            #print(row)
            teacher_set[tea]=comp
            #output_arr.append(teacher_set)

        conn.close()
    #print(teacher_set)
    cri_lab=sorted(teacher_set.items(),reverse=True)
    output_json=[]
    #print(cri_lab)
    for tea in cri_lab:
        conn = sqlite3.connect("finder.db")
        c = conn.cursor()
        select = "select name,outline,need,osusume from explanation where name=?"
        #print(tea[0][0])
        c.execute(select,(str(tea[0][0]),))
        for row in c.fetchall():
            #print(row)
            output_json.append({
                "name":row[0],
                "options":[{
                    "outline":row[1],
                    "need":row[2]
                }]
            })

        conn.close()
    header = {"Content-Type": "application/json"}
    res_4 = HTTPResponse(status=200, body=output_json, headers=header)
    result_json=json.dumps(output_json,ensure_ascii=False)
    #output_1 = {"message": "OK"}
    #------out(dict)----------------
    #header = {"Content-Type": "application/json"}
    #res_1 = HTTPResponse(status=200, body=output_1, headers=header)
    return {result_json}
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
run(host="0.0.0.0", port=8080, debug=True, reloader=True)



request.json
