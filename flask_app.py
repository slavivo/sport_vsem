from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import re


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'VERY_SECRET_KEY'
db = SQLAlchemy(app)

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    activities = db.Column(db.String(200))
    webpage = db.Column(db.String(200))
    contact = db.Column(db.String(100))
    tel = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    district = db.Column(db.String(50))

class SampleForm(FlaskForm):
    name = StringField('Name', render_kw={"placeholder": "Name"}, validators=[DataRequired()])
    activities = StringField('Activities', render_kw={"placeholder": "Activities"})
    webpage = StringField('Webpage', render_kw={"placeholder": "Webpage"})
    contact = StringField('Contact', render_kw={"placeholder": "Contact"})
    tel = StringField('Tel', render_kw={"placeholder": "Tel"})
    email = StringField('Email', render_kw={"placeholder": "Email"})
    address = StringField('Address', render_kw={"placeholder": "Address"})
    district = StringField('District', render_kw={"placeholder": "District"})

class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

def add_entry(entry):
    sample = Sample(
        name=entry['name'],
        activities=entry.get('activities'),
        webpage=entry.get('webpage'),
        contact=entry.get('contact'),
        tel=entry.get('tel'),
        email=entry.get('email'),
        address=entry.get('address'),
        district=entry['district']
    )
    db.session.add(sample)
    db.session.commit()

def add_entries_from_file(file_path, district):
    with open(file_path, 'r') as file:
        entry = {'district': district}
        for line in file:
            line = line.strip()
            if line.startswith('Pohybové aktivity'):
                entry['activities'] = line.split(': ')[1]
            elif line.startswith('Webová stránka'):
                entry['webpage'] = line.split(': ')[1]
            elif line.startswith('Kontaktní osob'):
                entry['contact'] = line.split(': ')[1]
            elif line.startswith('Telefon'):
                entry['tel'] = line.split(': ')[1]
            elif line.startswith('Email') or line.startswith('E-mail'):
                entry['email'] = line.split(': ')[1]
            elif line.startswith('Adresa'):
                entry['address'] = line.split(': ')[1]
                add_entry(entry)
                entry = {'district': district}
            elif re.match(r'^\s*$', line):  # Empty line
                continue
            else:
                entry['name'] = line
        # Add the last entry if it wasn't added
        if entry and 'address' in entry:
            add_entry(entry)

@app.route('/')
def index():
    # Retrieve all samples from the database
    samples = Sample.query.all()
    return render_template('index.html', samples=samples)

@app.route('/add_sample', methods=['GET', 'POST'])
def add_sample(entry):
    form = SampleForm()
    if form.validate_on_submit():
        # Create a new Sample instance and add it to the database
        form.district.data = form.district.data.lower()
        sample = Sample(
            name=form.name.data,
            activities=form.activities.data,
            webpage=form.webpage.data,
            contact=form.contact.data,
            tel=form.tel.data,
            email=form.email.data,
            address=form.address.data,
            district=form.district.data
        )
        db.session.add(sample)
        db.session.commit()
        flash('Sample added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_sample.html', form=form)

@app.route('/delete_sample/<int:sample_id>', methods=['GET', 'POST'])
def delete_sample(sample_id):
    # Retrieve the sample from the database
    sample = Sample.query.get(sample_id)
    # Delete the sample from the database
    db.session.delete(sample)
    db.session.commit()
    flash('Sample deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/show_samples', methods=['GET', 'POST'])
def show_all_samples():
    # Retrieve all samples from the database
    samples = Sample.query.all()
    return render_template('show_samples.html', samples=samples)

district_dict = {
    'praha': 'Praha',
    'stredocesky': 'Středočeský kraj',
    'jihocesky': 'Jihočeský kraj',
    'plzen': 'Plzeňský kraj',
    'karlovarsky': 'Karlovarský kraj',
    'ustecky': 'Ústecký kraj',
    'liberec': 'Liberecký kraj',
    'kralovehradecky': 'Královéhradecký kraj',
    'pardubicky': 'Pardubický kraj',
    'vysocina': 'Kraj Vysočina',
    'jihomoravsky': 'Jihomoravský kraj',
    'olomouc': 'Olomoucký kraj',
    'moravskoslezsky': 'Moravskoslezský kraj',
    'zlin': 'Zlínský kraj'
}

@app.route('/kraj/<district>', methods=['GET', 'POST'])
def show_samples(district):
    # Retrieve all samples from the database
    samples = Sample.query.filter_by(district=district).all()
    district = district_dict.get(district, district)
    return render_template('show_samples.html', district=district, samples=samples)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # db.session.query(Sample).delete()
        # db.session.commit()
        # districts = ['praha', 'stredocesky', 'jihocesky', 'plzen', 'karlovarsky',
        #              'ustecky', 'liberec', 'kralovehradecky', 'pardubicky',
        #              'vysocina', 'jihomoravsky', 'olomouc', 'moravskoslezsky', 'zlin']
        # for district in districts:
        #     add_entries_from_file(f'data/samples_{district}.txt', district)
    app.run(debug=True)
