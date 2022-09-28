from flask import Flask, render_template, request, redirect, url_for, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.secret_key = "Secret Key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    assign=db.Column(db.String(20))
    status=db.Column(db.String(20))
    date=db.Column(db.String(20))


    def __init__(self, name, email, phone,assign,status,date):

        self.name = name
        self.email = email
        self.phone = phone
        self.assign=assign
        self.status=status
        self.date=date





#This is the index route where we are going to
#query on all our employee data
@app.route('/',methods=['GET','POST'])
def login():
    error = None
    text="invalid user"
    if request.method == 'POST':
        if request.form['username']=='admin' and request.form['password']=='admin':
            return render_template('dashboard.html')
        else:
            return redirect(url_for('login'))
            
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
    
@app.route('/showtask')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", employees = all_data)


#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        assign =request.form['assign']
        status =request.form['status']
        date=request.form['date']



        my_data = Data(name, email, phone,assign,status,date)
        db.session.add(my_data)
        db.session.commit()

        flash("TASK Inserted Successfully")

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
      

        db.session.commit()
        flash("TASK Updated Successfully")

        return redirect(url_for('Index'))




#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("TASK Deleted Successfully")

    return redirect(url_for('Index'))






if __name__ == "__main__":
    app.run(debug=True)