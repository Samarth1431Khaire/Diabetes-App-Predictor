from flask import Flask, render_template, request, url_for, redirect, session
from sqlite3 import*

import pickle
app=Flask(__name__)
app.secret_key="ml engineer"



@app.route("/", methods=["GET","POST"])
def home():
  if "un" in session:
        
      if request.method=="POST":
         if request.form['action']=="Check Diabetes":
                 f=None
                 model=None
                 try:
                      f=open("diabetes.model", "rb")
                      model=pickle.load(f)
                 except Exception as e:
                       msg="f issue" + str(e)
                       return render_template("home.html", msg=msg)
                 finally:
                       if f is not None:
                               f.close()
                 if model is not None:
                       fs=float(request.form["fs"])
                       fu=request.form["fu"]
                       if fu==1:
                                    data=[[fs,1,0]]
                       else:
                                  data=[[fs,0,1]]
                       ans=model.predict(data)
                       msg="Your Diabetes Status is" +" "+ str(ans[0])
                       return render_template("home.html", msg=msg)
                 else:
                       return render_template("home.html", msg="model issue")
         elif request.form['action']=="Logout":
                  session.pop('un', None)
                  return redirect(url_for('login'))
                  
         else:
                  return render_template("home.html")
                  
                  
      else:
               return render_template("home.html")
  else:
          return redirect(url_for('login'))
 

 
              

@app.route("/signup",methods=["GET","POST"])
def signup():
      if "un" in session:
             return redirect(url_for('home'))
      
      if request.method=="POST":
               un=request.form["un"]
               pw1=request.form["pw1"] 
               pw2=request.form["pw2"]
               if pw1==pw2:
                      con=None
                      try:
                           con=connect("bmw.db")
                           cursor=con.cursor()
                           sql="insert into users values('%s','%s')"
                           cursor.execute(sql%(un,pw1))
                           con.commit()
                           return redirect(url_for('login'))

                      except Exception as e:
                             con.rollback()
                             return render_template("signup.html", msg="user already exits" + str(e))
                      finally:
                              if con is not None:
                                      con.close()
               else:
                    return render_template("signup.html", msg="passwords did not match")

      else:
             return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
       if "un" in session:
             return redirect(url_for('home'))
      
       if request.method=="POST":
               un=request.form["un"]
               pw=request.form["pw"] 
               con=None
               try:
                        con=connect("bmw.db")
                        cursor=con.cursor()
                        sql="select * from users where username='%s' and password='%s'"

                        cursor.execute(sql % (un,pw))
                        data=cursor.fetchall()
                        if len(data)==0:
                              return render_template("login.html", msg="invalid login")
                        else:
                             session["un"]=un
                             return redirect(url_for('home'))
               except Exception as e:
                           return render_template("login.html", msg=str(e))
               finally:
                          if con is not None:
                              con.close()
       else:
               return render_template("login.html")

@app.route("/readme", methods=["GET","POST"])
def readme():
        if "un" in session:
             return redirect(url_for('home'))

        return render_template("readme.html")
     
  
     

@app.errorhandler(404)
def not_found(e):
        return redirect(url_for('login'))



if __name__=="__main__":
        app.run(debug=True, use_reloader=True)