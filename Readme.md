To Navigate Refer to Readme file at [Master Branch](https://github.com/amrit-fuse/python/tree/master)

This branch contains ORM assignments and its solutions for Hotel management system.

To run the application:

`>> python app_ORM_assignment.py`

To check use `ORM_assignment.ipynb` file.

|**Function Name**|**Description**|
|:---|:---|
|`create_tables()`|Creates tables in the database|
|`delete_all()`|Deletes all rows of all tables from the database|
|`add_room_types`| Adds all available room types to the database|
|`add_rooms()`|Adds all room to the database|
|`check_room_availability()`|Checks if a room is available for a given date range|
|`convert_date()`|Converts a string date to a datetime object|



|**Methods**|**URL**|**Description**|
|:---|:---|:---|
|POST|/add_customer?first_name=`string`& last_name=`string`&phone=`int`&email=`string` |Adds a customer to the database|
|GET|/get_unbooked_rooms?check_in=`DateTime`& check_out=`DateTime`|Returns a list of unbooked rooms for a given date range|    
|GET|check_room_availability?check_in=`DateTime`& check_out=`DateTime`&room_id=`int`| Check if a room is available for a given date range|
|GET|/get_total_price?check_in=`DateTime`& check_out=`DateTime`&rooms=`String`|Returns the total price for a given date range and list of rooms|
|POST|/add_booking??check_in=`DateTime`& check_out=`DateTime`&rooms=`String`& customer_id=`int`&payment_done=`bool`|Adds a booking to the database|


## Questions:
1. The desk officer should be able to add new customers and their personal as well as booking information. One customer can book many rooms and there can be many types of rooms (Single, Double, Deluxe, etc). The booking details should include the check-in and check-out date as well as cost and payment information.
2. Each room must have its specific price and payment should be calculated accordingly. There can be many rooms in a hotel and the room status should be tracked. For example, whether a room is available or not.
3. Users should be able to calculate the price of the stay. For example, if a customer wants to stay for 5 days in a single room that costs Rs 2000 per day. The total cost of Rs 10000 should be returned.









