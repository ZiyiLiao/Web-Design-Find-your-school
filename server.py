#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import psycopg2

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://nz2297:0875@34.74.165.156/proj1part2"

# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)


# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id integer,
#   name varchar
# );""")
# engine.execute("""INSERT INTO test(id, name) VALUES (1,'grace hopper'), (2,'alan turing'), (3,'ada lovelace');""")
# engine.execute("DROP TABLE test")



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  # print(request.args)



  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  # context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  # return render_template("index.html", **context)

  return render_template("index.html")

@app.route('/borough', methods = ['GET'])
def borough():
  cursor = g.conn.execute("SELECT b.bname, b.area, b.population, c.type, COUNT(*) AS counts FROM borough b JOIN crime c ON c.bid = b.bid GROUP BY c.type, b.bname, b.area, b.population")
  borough = {}
  for result in cursor:
    key = (result['bname'], result['area'], result['population'])
    info = (result['type'], result['counts'])
    if key not in borough:
      borough[key] = [info]
    else:
      borough[key].append(info)
  cursor.close()
  return render_template('borough.html', data = borough)

@app.route('/search', methods = ['GET', 'POST'])
def search():
  bid = request.args.get("bid")
  level = request.args.get("fund")
  score = request.args.get("score")
  cursor = g.conn.execute("SELECT bname,bid FROM borough")
  names = []
  for result in cursor:
    temp = (result['bname'], result['bid'])
    names.append(temp)
  cursor.close()

  step1 = g.conn.execute("SELECT DISTINCT level FROM fund")
  fund_result = []
  for result in step1:
    fund_result.append(result['level'])
  step1.close()

  step2 = g.conn.execute("SELECT DISTINCT level FROM sat")
  score_result = []
  for result in step2:
    score_result.append(result['level'])
  step2.close()

  if (bid == None and level == None and score == None):
    return render_template("search.html", names = names, fund = fund_result, score = score_result)
  elif (bid != None and level == None and score == None):
    c = g.conn.execute("SELECT distinct initcap(sname), s.sid FROM school s, fund f, sat where s.bid = %s and f.sid = s.sid and sat.sid = s.sid", bid)
  elif (level != None and score == None and bid == None):
    c = g.conn.execute("SELECT distinct initcap(sname), s.sid FROM school s, fund f, sat where f.level = %s and f.sid = s.sid and sat.sid = s.sid",level)
  elif(level == None and bid == None and score != None): 
    c = g.conn.execute("SELECT distinct initcap(sname), s.sid FROM school s, fund f, sat where f.sid = s.sid and sat.sid = s.sid and sat.level = %s",score)
  elif (score == None):
    c = g.conn.execute("SELECT distinct initcap(sname), s.sid FROM school s, fund f, sat where s.bid = %s and f.level = %s and f.sid = s.sid and sat.sid = s.sid", bid, level)
  elif (level == None):
    c = g.conn.execute("SELECT distinct initcap(sname), s.sid FROM school s, fund f, sat where s.bid = %s and f.sid = s.sid and sat.sid = s.sid and sat.level = %s", bid, score)
  elif (bid == None):
    c = g.conn.execute("SELECT distinct initcap(sname), s.sid FROM school s, fund f, sat where f.level = %s and f.sid = s.sid and sat.sid = s.sid and sat.level = %s",level,score)
  elif (bid != None and level != None and score != None):
    c = g.conn.execute("SELECT distinct initcap(sname), s.sid FROM school s, fund f, sat where s.bid = %s and f.level = %s and f.sid = s.sid and sat.sid = s.sid and sat.level = %s", bid, level,score)
  schools = c.fetchall()
  c.close()
  return render_template("search.html", names = names, result = schools, fund = fund_result, score = score_result)
  


@app.route('/school_search')
def school_search():
  cursor = g.conn.execute("SELECT sname,sid FROM school")
  names = []
  for result in cursor:
    temp = (result['sname'], result['sid'])
    names.append(temp)
  cursor.close()
  return render_template("school_search.html", names = names)


@app.route('/school_info', methods=['GET'])
def school_info():
  fsid = request.args.get("sid") # extract selected sid
  cursor = g.conn.execute("SELECT * FROM school s, borough b WHERE s.sid = %s and s.bid = b.bid", fsid)
  rows = cursor.fetchall()
  cursor.close() 

  c = g.conn.execute("SELECT * FROM survey s WHERE s.sid = %s", fsid)
  survey = c.fetchall()
  c.close() 

  s = g.conn.execute("SELECT * FROM sat WHERE sat.sid = %s", fsid)
  sat = s.fetchall()
  s.close()

  f = g.conn.execute("SELECT * FROM fund WHERE fund.sid = %s", fsid)
  fund = f.fetchall()
  f.close()
  return render_template('school_info.html', school_id = rows, survey = survey, sat = sat, fund = fund)


@app.route('/login', methods = ['GET','POST'])
def login():
  return render_template("login.html")


@app.route('/manage', methods = ['GET','POST'])
def manage():  
  userid = request.args.get("userid")
  pwd = request.args.get("password")
  try:
    digit = int(userid[0])
    sid = userid
    cursor = g.conn.execute("SELECT * FROM school where sid = %s and password = %s", sid, pwd)
    s = cursor.fetchall()
    cursor.close()
    if len(s) == 0:
      return render_template("login.html", err = sid)
    else:
      c1 = g.conn.execute("SELECT distinct course_id, course_name, tname FROM teach t, teacher t1 where t.sid = %s and t.tid = t1.tid order by course_id", sid)
      teach = c1.fetchall()
      c1.close()

      c2 = g.conn.execute("SELECT * from student where left(stuid,6) like %s order by stuid;", sid)
      students = c2.fetchall()
      c2.close()

      c3 = g.conn.execute("SELECT * from teacher where left(tid,6) like %s order by tid;", sid)
      teacher = c3.fetchall()
      c3.close()
      
      c4 = g.conn.execute("SELECT * FROM survey s WHERE s.sid = %s", sid)
      survey = c4.fetchall()
      c4.close()   

      sat = g.conn.execute("SELECT * FROM sat WHERE sat.sid = %s order by year", sid)
      score = sat.fetchall()
      sat.close()

      f = g.conn.execute("SELECT * FROM fund WHERE fund.sid = %s", sid)
      fund = f.fetchall()
      f.close()

      return render_template("manage.html", data = s, sid = sid, teach = teach, survey = survey, fund = fund, sat = score, student = students, teacher = teacher)
  except:
    bname = userid
    print("bname :" + bname)
    cursor = g.conn.execute("SELECT * FROM borough where bname = %s and password = %s", bname, pwd)
    s = cursor.fetchall()
    cursor.close()
    if len(s) == 0:
      return render_template("login.html", err = bname)
    else:
      c1 = g.conn.execute("SELECT fid, sname, f.year, amount FROM borough b, fund f, school s where b.bname = %s and b.bid = f.bid and f.sid = s.sid", bname)
      fund = c1.fetchall()
      c1.close()

      c2 = g.conn.execute("SELECT sname, sid FROM school s, borough b where b.bname = %s and b.bid = s.bid", bname)
      names = c2.fetchall()
      c2.close()
      return render_template("manage.html", data = s, bname = bname , names = names, fund = fund)

  

@app.route('/insert_borough', methods=['GET',"POST"])
def insert_borough():
  bname = request.args.get("bname")
  cursor = g.conn.execute("SELECT bid, password FROM borough where bname = %s", bname)
  s = cursor.fetchone()
  bid = s[0]
  pwd = s[1]
  cursor.close() 
  item = request.args.get("item")

  if request.method == "POST":
    if item == 'fund':
      fid = request.form['fid']
      sid = request.form['sid']
      year = request.form['year']
      amount = request.form['amount']
      c1 = g.conn.execute("INSERT INTO fund(fid, sid, bid, year, amount) VALUES (%s, %s, %s, %s, %s)", (fid, sid, bid, year,amount))
      c2 = g.conn.execute("UPDATE fund set level = case when amount >82000 then 'High' when amount >75000 and amount < 82000 then 'Medium' else 'low' end")
      c1.close()
      c2.close()
    elif item == 'school':
      sid = request.form['sid']
      sname = request.form['sname']
      enrollment = request.form['enrollment']
      principal = request.form['principal']
      password = request.form['password']
      c1 = g.conn.execute("INSERT INTO school(sid, sname,enrollment, bid, principal, password) VALUES (%s,%s,%s,%s,%s,%s)", (sid,sname,enrollment,bid,principal,password))
      c1.close()
    return render_template("insert_borough.html", bname = bname, pwd = pwd, item = item, message = "*  Finished!")
  return render_template("insert_borough.html", bname = bname, pwd = pwd,item = item)


@app.route('/insert_school', methods=['GET',"POST"])
def insert_school():
  sid = request.args.get("sid")
  cursor = g.conn.execute("SELECT password FROM school where sid = %s", sid)
  s = cursor.fetchone()
  pwd = s[0]
  cursor.close()
  item = request.args.get("item")

  if request.method == "POST":
    if item == 'sat':
      year= request.form['year']
      reading = request.form['reading']
      mathematics = request.form['mathematics']
      writing = request.form['writing']
      total = int(reading) + int(mathematics) + int(writing)
      c1 = g.conn.execute("INSERT INTO sat(sid, year, reading, mathematics, writing) VALUES (%s, %s, %s, %s, %s)", (sid, year, reading, mathematics,writing))
      c2 = g.conn.execute("UPDATE sat set total = %s where sid = %s and year = %s", (total, sid, year))
      c3 = g.conn.execute("UPDATE sat set level = case when total >1200 then 'High' when total >1125 and total < 1200 then 'Medium' else 'low' end")
      c1.close()
      c2.close()
      c3.close()
    elif item == 'student':
      temp= request.form['stuid']
      name = request.form['name']
      stuid = sid +temp
      c1 = g.conn.execute("INSERT INTO student(stuid, name) VALUES (%s, %s)", (stuid, name))
      c1.close()
    elif item == 'teacher':
      course_id= request.form['cid']
      course_name = request.form['cname']
      tid = request.form['tid']
      stuid= request.form['stuid']
      c1 = g.conn.execute("INSERT INTO teach(course_id, course_name, tid, stuid) VALUES (%s, %s, %s, %s)", (course_id, course_name, tid, stuid))
      c1.close()
    elif item == 'course':
      tid = sid + request.form['tid']
      name = request.form['cname']
      stuid = sid + request.form['stuid']
      course_id = request.form['cid']
      c1 = g.conn.execute("INSERT INTO teach(course_id, course_name, tid, stuid, sid) VALUES (%s, %s, %s, %s, %s)", (course_id, name, tid, stuid, sid))
      c1.close()

    return render_template("insert_school.html", sid = sid , item = item, message = "* Finished!", pwd = pwd)
  else:
    return render_template("insert_school.html",sid = sid,item = item, pwd = pwd)




# @app.route('/check', methods = ['GET', 'POST'])
# def check():
#   c2 = g.conn.execute("SELECT * FROM sat where sid = '01M292'")
#   teach = c2.fetchall()
#   c2.close()
  
#   return render_template("check.html", names = teach)


# Example of adding new data to the database
# @app.route('/add', methods=['GET','POST'])
# def add():
#   if request.method == "POST":
#     name = request.form['name']
#     g.conn.execute("INSERT INTO test(name) VALUES (%s)", (name))
#     return render_template("add.html",res = "y")
#   return render_template("add.html")




  


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  #@click.argument('HOST', default='0.0.0.0')
  @click.argument('HOST', default='35.237.146.64')
  @click.argument('PORT', default=8111, type=int)
  #@click.argument('PORT', default=8080, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
