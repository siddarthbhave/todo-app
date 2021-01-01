from flask import Flask, render_template, url_for, request, redirect
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, server_default=func.now())

    def __repr__(self):
        return '<Task id:%r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    tasks = ToDo.query.order_by(ToDo.id).all()
    if request.method == 'POST':
        if request.form['content'].strip() == '':
            flash('Task cannot be empty!')
            return render_template('index.html', tasks=tasks)
        task_content = request.form['content']
        new_task = ToDo(content=task_content)
        print('q', len(request.form['content']), 'q')

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding your task'
    else:
        return render_template('index.html', tasks=tasks)


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    u = ToDo.query.get(id)
    if request.method == 'POST':
        if request.form['content'].strip() == '':
            flash('Task cannot be empty!')
            return render_template('update.html', task=u)
        u.content = request.form['content']
        u.date_created = func.now()
        try:
            db.session.commit()
        except:
            print("Couldn't update!")

        return redirect(url_for('index'))

    return render_template('update.html', task=u)


@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    u = ToDo.query.get(id)
    try:
        db.session.delete(u)
        db.session.commit()
    except:
        print("Couldn't delete")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True, host='0.0.0.0')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, ToDo=ToDo)
