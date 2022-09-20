
import orm_dbsecrets
from flask import Flask, jsonify, request
import json
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, Boolean, Table, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func
from datetime import datetime


# create Database  SChemea manually in MySQL Workbench
dbuser, dbpass, dbhost, dbport, dbname = orm_dbsecrets.dbuser, orm_dbsecrets.dbpass, orm_dbsecrets.dbhost, orm_dbsecrets.dbport, orm_dbsecrets.dbname

# engine = create_engine('DB_TYPE+DB_CONNECTOR://user:pass@host:port/DB_name')
# echo=True will show the SQL commands in the terminal
engine = create_engine(
    f'mysql+mysqldb://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}', echo=True)

app = Flask(__name__)  # create an instance of the Flask class for our web app

Base = declarative_base()  # create a base class for our class definitions

# create a session object to connect to the DB
session = sessionmaker(bind=engine)()

# Model Classes for the tables in the DB


class Booking(Base):
    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True)
    check_in = Column(Date)
    check_out = Column(Date)
    total_cost = Column(Float)
    payment_done = Column(Boolean)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    room_id = Column(Integer, ForeignKey('room.room_id'))

    # back_populates='booking' is used to create a relationship between the two tables (Booking and Customer)
    customer = relationship('Customer', back_populates='booking')
    # syntax: relationship('class_name', back_populates='attribute_name')
    room = relationship('Room', back_populates='booking')

    def __repr__(self):
        return f'Booking ID: {self.booking_id}, Check-in: {self.check_in}, Check-out: {self.check_out}, Customer ID: {self.customer_id}, Room ID: {self.room_id}, Total Cost: {self.total_cost}, Payment Done: {self.payment_done}'


class Customer(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    phone = Column(String(20))
    email = Column(String(20))
    booking = relationship('Booking', back_populates='customer')

    def __repr__(self):
        return f'Customer ID: {self.customer_id}, First Name: {self.first_name}, Last Name: {self.last_name}, Phone: {self.phone}, Email: {self.email}'


class Room(Base):
    __tablename__ = 'room'
    room_id = Column(Integer, primary_key=True)
    room_type_id = Column(Integer, ForeignKey('room_type.room_type_id'))
    booking = relationship('Booking', back_populates='room')
    room_type = relationship('Room_type', back_populates='room')

    def __repr__(self):
        return f'Room ID: {self.room_id},  Room Type ID: {self.room_type_id}'


class Room_type(Base):
    __tablename__ = 'room_type'
    room_type_id = Column(Integer, primary_key=True)
    name = Column(String(20))
    price = Column(Float)
    room = relationship('Room', back_populates='room_type')

    def __repr__(self):
        return f'Room Type ID: {self.room_type_id}, Room Type: {self.name}, Price: {self.price}'


# create all tables in the DB with the above model classes
def create_tables():
    Base.metadata.create_all(engine)


# delete all contents of all tables
def delete_all():
    session.query(Booking).delete()
    session.query(Customer).delete()
    session.query(Room).delete()
    session.query(Room_type).delete()
    session.commit()

# add all room types to the DB


def add_room_types():
    # add room types
    room_types = [
        # create a new room type object and add it to the session
        Room_type(name='Single', price=1000),
        Room_type(name='Double', price=2000),
        Room_type(name='Deluxe', price=3000),
        Room_type(name='Suite', price=4000),
    ]

    # only insert if the room type does not exist
    # filter_by()  is used to filter the query by a certain condition and accepts keyword arguments **kwargs
    # first() returns the first row of the query result
    for room_type in room_types:
        if not session.query(Room_type).filter_by(name=room_type.name).first():
            session.add(room_type)


def add_rooms():
    # add rooms
    # collect available room types
    # done to prevent error due to foreign key constraint
    room_types = session.query(Room_type).all()

    # create a new room object and add it to the session
    rooms = [
        Room(room_type=room_types[0]),
        Room(room_type=room_types[0]),
        Room(room_type=room_types[1]),
        Room(room_type=room_types[1]),
        Room(room_type=room_types[2]),
        Room(room_type=room_types[2]),
        Room(room_type=room_types[3]),
        Room(room_type=room_types[3])
    ]

    # add all rooms to the session
    session.add_all(rooms)
    session.commit()


# check if the room is available for the given dates

def check_room_availability(check_in, check_out, room_id):
    # get all bookings for the given room
    # all() returns all rows of the query result

    bookings = session.query(Booking).filter_by(room_id=room_id).all()

    for booking in bookings:
        # compare existing checkin and checkout dates with the new checkin and checkout dates
        if (check_in >= booking.check_in and check_in <= booking.check_out) or (check_out >= booking.check_in and check_out <= booking.check_out):
            return False
    return True


# Covert string to datetime.date   (YYYY-MM-DD)
def convert_date(date):
    return datetime.strptime(date, '%Y-%m-%d').date()


# calculate total price of stay for the given dates
def calculate_total_price(check_in, check_out, room_type_id):
    # get the room type
    room_type = session.query(Room_type).filter_by(
        room_type_id=room_type_id).first()
    # calculate the total price of stay for the given dates
    total_price = (check_out - check_in).days * room_type.price
    return total_price


##################################  API Endpoints ##############################
@app.route('/add_customer', methods=['POST'])
def add_customer():
    # print url
    print(request.url)

    # get the data from the request
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    phone = request.args.get('phone')
    email = request.args.get('email')

    # only insert if the customer does not exist
    # filter_by()  is used to filter the query by a certain condition and accepts keyword arguments **kwargs
    # identify customer by phone number
    if not session.query(Customer).filter_by(phone=phone).first():
        # create a new customer object and add it to the session
        customer = Customer(first_name=first_name, last_name=last_name,
                            phone=phone, email=email)
        session.add(customer)
        session.commit()

        return jsonify({'message': 'Customer added successfully', 'customer_id': customer.customer_id, 'first_name': customer.first_name, 'last_name': customer.last_name, 'phone': customer.phone, 'email': customer.email})

    # if the customer already exists
    else:
        return jsonify({'message': 'Customer already exists ', 'first_name': first_name, 'phone': phone})


@app.route('/add_booking', methods=['POST'])
def add_booking():
    print(request.url)

    # single customer can book many rooms  and check each room if available or not for the given dates
    # get the data from the request
    check_in = convert_date(request.args.get('check_in'))
    check_out = convert_date(request.args.get('check_out'))
    payment_done_int = int(request.args.get('payment_done'))
    customer_id = request.args.get('customer_id')
    room_id = request.args.get('room_id')
    rooms = request.args.get('rooms')
    # convert the string to list
    rooms = rooms.split(',')

    # convert string to boolean
    if payment_done_int == 1:
        payment_done = True
    else:
        payment_done = False

    total_sum = 0

    for room_no in rooms:
        # check if the room is available for the given dates
        if check_room_availability(check_in, check_out, room_no):
            # get the room type
            room_type = session.query(Room).filter_by(room_id=room_no).first()

            total_price = calculate_total_price(
                check_in, check_out, room_type.room_type_id)

            total_sum += total_price

            # create a new booking object
            booking = Booking(check_in=check_in, check_out=check_out, payment_done=payment_done,
                              total_cost=total_price, customer_id=customer_id, room_id=room_no)
            # add the booking to the session
            session.add(booking)
            # commit the changes to the DB
            session.commit()

        else:
            # return a message saying the room is not available for the given dates
            return jsonify({'message': 'Room is not available for the given dates', 'room_id': room_no})

    return jsonify({'message': 'Booked successfully', 'check_in': booking.check_in, 'check_out': booking.check_out, 'payment_done': booking.payment_done, 'total_cost for all booking': total_sum, 'customer_id': booking.customer_id, 'Room numbers': rooms})

# API to get  all  unbooked rooms with their room type and price


@app.route('/get_unbooked_rooms', methods=['GET'])
def get_unbooked_rooms():
    print(request.url)

    # get checkin and checkout dates from the request
    check_in = convert_date(request.args.get('check_in'))
    check_out = convert_date(request.args.get('check_out'))

    rooms = session.query(Room).all()
    room_types = session.query(Room_type).all()
    bookings = session.query(Booking).all()
    # get all unbooked rooms
    unbooked_rooms = []

    # check if the room is available for the given dates
    for room in rooms:
        if check_room_availability(check_in, check_out, room.room_id):

            room_type = session.query(Room_type).filter_by(
                room_type_id=room.room_type_id).first()
            # create a dictionary for the room
            room_dict = {'room_id': room.room_id, 'room_type': room_type.name,
                         'price': room_type.price}
            # append the dictionary to the list
            unbooked_rooms.append(room_dict)

    return jsonify({'unbooked_rooms': unbooked_rooms})

# get whether room is available or not for the given dates


@app.route('/check_room_availability', methods=['GET'])
def check_room_availability_api():
    print(request.url)

    check_in = convert_date(request.args.get('check_in'))
    check_out = convert_date(request.args.get('check_out'))
    room_id = request.args.get('room_id')

    if check_room_availability(check_in, check_out, room_id):
        return jsonify({'message': 'Room is available', 'room_id': room_id, 'check_in': check_in, 'check_out': check_out})
    else:
        return jsonify({'message': 'Room is not available', 'room_id': room_id, 'check_in': check_in, 'check_out': check_out})


# grt total price for supplied  rooms for the given dates
@app.route('/get_total_price', methods=['GET'])
def get_total_price():
    print(request.url)

    check_in = convert_date(request.args.get('check_in'))
    check_out = convert_date(request.args.get('check_out'))
    rooms = request.args.get('rooms')
    # convert the string to list
    rooms = rooms.split(',')
    print(rooms)
    print(type(rooms))

    total_price_of_stay = 0   # total price of stay for multiple room id supplied

    track_price = []

    for room_id in rooms:

        # Check if the room is available for the given dates
        if not check_room_availability(check_in, check_out, room_id):
            return jsonify({'message': 'Room not available for the given dates, Try different date', 'Room id': room_id})

        room = session.query(Room).filter_by(room_id=room_id).first()
        # calculate the total price of stay for the given dates
        price_of_stay = calculate_total_price(
            check_in, check_out, room.room_type_id)

        total_price_of_stay += price_of_stay
        tract_dict = {'room_id': room_id,
                      'price_of_stay': price_of_stay, 'Room_type': room.room_type_id}
        track_price.append(tract_dict)

    return jsonify({'total_price_of_stay': total_price_of_stay,  'rooms': track_price, 'check_in': check_in, 'check_out': check_out})


if __name__ == '__main__':
    create_tables()
    add_room_types()  # add room types to the DB only if they do not exist
    add_rooms()

    # delete_all()  # delete all records from all tables

    # run the Flask app in debug mode (for development only)
    app.run(debug=True)
