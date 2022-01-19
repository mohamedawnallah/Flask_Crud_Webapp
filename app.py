from flask import Flask, render_template, url_for, request, redirect
from itsdangerous import exc
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Task %r>' % self.id
        
db.create_all()

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"{e}"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        
        return render_template('index.html',tasks = tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delte = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delte)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"{e}"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"{e}"
    else:
        return render_template('update.html',task = task)

if __name__ == "__main__":
    app.run(debug=True)