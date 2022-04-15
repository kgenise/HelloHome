from flask import Blueprint, render_template, request, redirect, url_for #, Response
from flask_login import login_required, current_user
from . import db
from models import Property
from PIL import Image
import io
import base64

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/check')
def check():
    # current_user.ATTRIBUTE contains information about the logged-in user
    # Uses same attributes as User object
    properties_count = db.session.query(db.func.count()).filter(Property.user_id==current_user.id).scalar()

    properties = db.session.query(Property).order_by(Property.user_id==current_user.id,Property.listing_id.desc()).first()
    image_data = properties.image

    # Read the image and assign to variable.
    image = Image.open(io.BytesIO(image_data))

    # Get the in-memory info using below code line.
    display_image = io.BytesIO()

    #First save image as in-memory.
    image.save(display_image, format="PNG")

    #Then encode the saved image file.
    encoded_img_data = base64.b64encode(display_image.getvalue())

    # reponse = Response(display_image.getvalue(), mimetype='image/png')
    image.show()

    return render_template('success.html', name=current_user.fname, count=properties_count, img_data=encoded_img_data.decode('utf-8'))

@main.route('/properties')
@login_required
def properties():
    account = current_user.account_type

    if 'agent' in account:
        return render_template('properties.html', name=current_user.fname)
    elif 'buyer' in account:
        return render_template('listings.html', name=current_user.fname)
    else:
        return render_template('login.html')

@main.route('/properties', methods=['POST'])
@login_required
def properties_post():
    sale_type = request.form.get('sale_type')
    property_type = request.form.get('property_type')
    price = request.form.get('price')
    num_bed = request.form.get('num_bed')
    num_bath = request.form.get('num_bath')
    building_size = request.form.get('building_size')
    land_size = request.form.get('land_size')
    street = request.form.get('street')
    city = request.form.get('city')
    state = request.form.get('state')
    zip = request.form.get('zip')
    agent_id = current_user.id
    file_image = request.files['file_image']
    upload_image = file_image.read()

    new_property = Property(agent_id, sale_type, property_type, price, num_bed, num_bath, building_size, land_size, street, city, state, zip, upload_image)
    db.session.add(new_property)
    db.session.commit()

    return redirect(url_for('main.check'))