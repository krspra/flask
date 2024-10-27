from datetime import datetime,timezone
from flask import Flask , render_template,request ,redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db=SQLAlchemy(app)

class Todo(db.Model):
    Sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

@app.route("/",methods=['GET','POST'])
def Home_Page():
    if request.method=='GET':
     allTodo=Todo.query.all()
     return render_template('index.html',allTodo=allTodo)
    if request.method=='POST':
       newtitle=request.form['title']
       newdesc=request.form['desc']
       todo=Todo(title=newtitle,desc=newdesc)
       db.session.add(todo)
       db.session.commit()
       return redirect('/')

@app.route('/delete/<int:deleteSno>')
def handle_delete(deleteSno):
    todo=Todo.query.filter_by(Sno=deleteSno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:updateSno>',methods=['POST','GET'])
def handle_update(updateSno):
    if request.method=='POST':
        newtitle = request.form['title']
        newdesc = request.form['desc']
        todo = Todo.query.filter_by(Sno=updateSno).first()
        todo.title = newtitle
        todo.desc = newdesc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(Sno=updateSno).first()
    return render_template('update.html', todo=todo)
      
# if __name__ =="__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)