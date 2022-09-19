
import orm_dbsecrets
from flask import Flask, jsonify, request
import json
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, Boolean, Table, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func
from datetime import datetime


# create Database manually in MySQL Workbench

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
        Room(room_type=room_types[0]),
        Room(room_type=room_types[0]),
        Room(room_type=room_types[1]),
        Room(room_type=room_types[1]),
        Room(room_type=room_types[1]),
        Room(room_type=room_types[1]),
        Room(room_type=room_types[2]),
        Room(room_type=room_types[2]),
        Room(room_type=room_types[2]),
        Room(room_type=room_types[2]),
        Room(room_type=room_types[3]),
        Room(room_type=room_types[3]),
        Room(room_type=room_types[3]),
        Room(room_type=room_types[3]),
    ]

    # add all rooms to the session
    session.add_all(rooms)
    session.commit()


# check if the room is available for the given dates
# if available, add the booking to the DB
# if not available, return a message saying the room is not available for the given dates


def check_room_availability(check_in, check_out, room_id):
    # check if the room is available for the given dates
    # get all bookings for the given room
    # all() returns all rows of the query result
    bookings = session.query(Booking).filter_by(room_id=room_id).all()
    # check if the room is available for the given dates
    for booking in bookings:
        # if the room is not available for the given dates
        # compare existing checkin and checkout dates with the new checkin and checkout dates
        if (check_in >= booking.check_in and check_in <= booking.check_out) or (check_out >= booking.check_in and check_out <= booking.check_out):
            return False
    # if the room is available for the given dates
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


########## API Endpoints ############
# API to add a new customer, personal info and booking info
# The desk officer should be able to add new customers and their personal as well as booking information. One customer can book many rooms and there can be many types of rooms (Single, Double, Deluxe, etc). The booking details should include the check-in and check-out date as well as cost and payment information.


@app.route('/add_customer', methods=['POST'])
def add_customer():
    # print url
    print(request.url)

    # get the data from the request
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    phone = request.args.get('phone')
    email = request.args.get('email')

    # create a new customer object
    customer = Customer(first_name=first_name,
                        last_name=last_name, phone=phone, email=email)
    # add the customer to the session
    session.add(customer)
    # commit the changes to the DB
    session.commit()
    # return the customer id  with message and other personal details in JSON format
    return jsonify({'message': 'Customer added successfully', 'customer_id': customer.customer_id, 'first_name': customer.first_name, 'last_name': customer.last_name, 'phone': customer.phone, 'email': customer.email})


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

    # check if the room is available for the given dates
    # if available, add the booking to the DB
    # if not available, return a message saying the room is not available for the given dates

    total_sum = 0

    for room_no in rooms:
        # check if the room is available for the given dates
        if check_room_availability(check_in, check_out, room_no):
            # calculate the total price of stay for the given dates

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

    # return the booking id  with message in JSON format
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
    for room in rooms:
        # check if the room is available for the given dates
        # if available, add the room to the unbooked_rooms list

        if check_room_availability(check_in, check_out, room.room_id):
            unbooked_rooms.append(room)

    print('unbooked_rooms')

    # create a list of dictionaries to store the room details
    room_details = []
    for room in unbooked_rooms:
        # get the room type of the room
        room_type = session.query(Room_type).filter_by(
            room_type_id=room.room_type_id).first()
        # create a dictionary to store the room details
        room_detail = {
            'room_id': room.room_id,
            'type': room_type.name,
            'price/day': room_type.price
        }
        # append the room details to the room_details list
        room_details.append(room_detail)
    print('roomdetails')
    # return the room details in JSON format
    return jsonify(room_details)


# grt total price for supplied  rooms for the given dates
@app.route('/get_total_price', methods=['GET'])
def get_total_price():
    print(request.url)

    # get checkin and checkout dates from the request
    check_in = convert_date(request.args.get('check_in'))
    check_out = convert_date(request.args.get('check_out'))
    rooms = request.args.get('rooms')
    # convert the string to list
    rooms = rooms.split(',')
    print(rooms)
    print(type(rooms))

    # calculate the total price of stay for the given dates
    total_price = 0
    for room_id in rooms:

        # Check if the room is available for the given dates
        if not check_room_availability(check_in, check_out, room_id):
            return jsonify({'message': 'Room not available for the given dates'})

            # get the room type of the room
        room = session.query(Room).filter_by(room_id=room_id).first()
        # calculate the total price of stay for the given dates
        total_price += calculate_total_price(
            check_in, check_out, room.room_type_id)

    # return the total price , room selected , checkin and checkout dates
    return jsonify({'total_price': total_price, 'rooms': rooms, 'check_in': check_in, 'check_out': check_out})


# def add_customer():
#     # add a new customer
#     new_customer = Customer(first_name='John', last_name='Doe',
#                             phone='1234567890', email='hello@gmail.com')
#     session.add(new_customer)  # add new customer to the session
#     session.commit()  # commit the changes to the DB
if __name__ == '__main__':
    create_tables()
    # add_customer() to test the add_customer() function
    add_room_types()  # add room types to the DB only if they do not exist
    # add_rooms()

    # delete_all()  # delete all records from all tables
    # run the Flask app in debug mode (for development only)
    app.run(debug=True)
