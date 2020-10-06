from flask import Flask,flash
from flask import request,redirect,render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# connection with mysql ..
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/Employees_SqlAlchemy'

app.config['SECRET_KEY'] = 'I\xf1k\xffDiouH\x04\xf0\xe1\xf3\x17W\x08\xfc"m\xc0\x96\xfb\x93\x7f'

""" for secret key ..
import os 
os.urandom(24)
"""

db = SQLAlchemy(app)

# creating models ..
class Employees(db.Model):
    id = db.Column('employee_id',db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    salary = db.Column(db.Float(50))
    age = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    # def __init__(self,name,salary,age,pin):
    #     self.name = name
    #     self.salary =salary
    #     self.age = age
    #     self.pin = pin

    def __repr__(self):
        return  "<Employees(name='%s', salary='%f', age='%s', pin='%s')>" % (self.name, self.salary, self.age, self.pin)
        # return self.name

db.create_all() # to create all tables in database
# we can write this statement here or at exactly before run statement ..

@app.route('/')
def list_employees():

    employees = Employees.query.all() # returns list ..
    print(employees)

    return render_template('list_employees.html',Employees = employees)

@app.route('/add_employee',methods=['GET','POST'])
def addEmployee():
    if request.method =="POST":
        if not request.form['name'] or not request.form['salary'] or not request.form['age']:
            flash("Please enter all the fields ..")
            return render_template('add.html')
        else:
            name = request.form['name']
            age = request.form['age']
            salary = request.form['salary']
            pin = request.form['pin']
            employee = Employees(name=name,salary=salary,age=age,pin=pin) # insert query ..
            db.session.add(employee)
            db.session.commit()

            flash("Record was Successfully added.")
            return redirect('/') # or return redirect(url_for('list_employees'))
    else : 
        return render_template('add.html')

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    emp = Employees.query.filter_by(id=id).first()
    print(request.method)
    if request.method =='POST':
        name = request.form['name']
        age = request.form['age']
        salary = request.form['salary']
        pin = request.form['pin']

        emp.name = name
        emp.age = age
        emp.salary = salary
        emp.pin = pin
        db.session.commit()
        flash("Data Successfully Updated..")
        return redirect('/')
    else:
        return render_template('edit.html',employee = emp)

@app.route('/delete')
def delete():
    e_id = request.args.get('id')
    # print(pk)
    emp = Employees.query.filter_by(id= e_id).first()
    """ or we can write 
     emp = Employees.query.get(e_id) 
     by providing just e_id
     """

    db.session.delete(emp)
    db.session.commit()
    flash("Data is successfully Deleted..")
    return redirect('/')


if __name__ == "__main__":
    # db.create_all() # to create all tables in database
    app.run(debug=True)