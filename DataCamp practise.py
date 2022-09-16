############## Engines and connection strings##########################


################ ALL imports ##########################################
# Import create_engine function
from sqlalchemy import select, func
from sqlalchemy import insert
from sqlalchemy import Table, Column, String, Integer
from sqlalchemy import create_engine, MetaData
from sqlalchemy import delete, select
from sqlalchemy import insert, select
from sqlalchemy import Table, Column, String, Integer, Float, Boolean
from sqlalchemy import case, cast, Float
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import func
from sqlalchemy import desc
from sqlalchemy import and_
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import create_engine

# Create an engine to the census database
engine = create_engine('sqlite:///census.sqlite')

# Print table names
print(engine.table_names())


################ Autoloading  tables from a database ####################
# Import create_engine, MetaData, and Table

# Create engine: engine
engine = create_engine('sqlite:///census.sqlite')

# Create a metadata object: metadata
metadata = MetaData()

# Reflect census table via engine: census
# fromat table('table_name',metadata,autoload=True,autoload_with=engine)
# autoload_with is used to specify the engine to use for loading the table metadata from the database.
census = Table('census', metadata, autoload=True, autoload_with=engine)

# reflection is the process of reading the database and building the metadata based on that information. It's the opposite of creating a Table by hand and is very useful for working with existing databases.

# Print census table metadata
print(repr(census))


################# Viewing table details ###############################
# by APP
engine = create_engine('sqlite:///census.sqlite')
metadata = MetaData()

# Reflect the census table from the engine: census
census = Table('census', metadata, autoload=True, autoload_with=engine)

# Print the column names
print(census.columns.keys())

# Print full table metadata
# repr() returns a printable representation of the object.
print(repr(metadata.tables['census']))


# SQLAlchemy Provide pythonic way to interact with database i.e build python classes that map to tables in database and instances of those classes map to rows in the table.
# SQLAlchemy is a library that facilitates the communication between Python programs and databases. It is an Object Relational Mapper (ORM) that provides a high-level abstraction layer for the database. It is used to perform CRUD operations on the database.
# hides the complexity of SQL behind a simple and consistent API.


################# Selecting data from a Table: raw SQL ###############################
# by APP
# Import create_engine function

# Create an engine to the census database
connection = create_engine('sqlite:///census.sqlite')

# build select statement for census table:stmt
# syntax for select statement: select column_name from table_name
stmt = 'SELECT * FROM census'  # select all columns from census table

# Execute the statement and fetch the results: results
# execute() method on engine returns a ResultProxy and fetchall() method on ResultProxy returns a list of tuples. #fetchall() returns all the rows of a query result.
results = connection.execute(stmt).fetchall()

# Print results
print(results)


################# Selecting data from a Table with SQLAlchemy ###############################
# by APP
# Import create_engine, MetaData, and Table

# Reflect census table from the engine: census
census = Table('census', metadata, autoload=True, autoload_with=engine)

# Biuld select statement for census table: stmt
# syntax for select statement: select([table_name]) # select all columns from census table
# select all columns from census table using select() function
stmt = select([census])

# print the emitted statement to see the SQL emitted
print(stmt)

# Execute the statement and print the results
# fetchmany() returns the first n rows of a query result. size is the number of rows to be returned.
results = connection.execute(stmt).fetchmany(size=10)

# Print results
print(results)


################# Handling a ResultSet ###############################
# by APP
# SQlalchemy allows list style access to the results of a query
# get the first row of the results by using an index on the results object: first_row
first_row = results[0]

# print the first row of the results
print(first_row)

# print the first column of the first row by using an index
print(first_row[0])  #
# print the 'state' column of the first row by using its name
# get the value of the state column in the first row by using its name as an index
print(first_row['state'])


################# Connecting to a PostgreSQL database ###############################

# Import create_engine function

# Create an engine to the census database
engine = create_engine(
    'postgresql+psycopg2://student:datacamp@postgresql.csrrinzqubik.us-east-1.rds.amazonaws.com:5432/census')

# Use the .table_names() method on the engine to print the table names
print(engine.table_names())


################# Filtering data selected from a Table - Simple ###############################

# Import create_engine, MetaData, and Table

# Create a select query: stmt
stmt = select([census])

# Add a where clause to filter the results to only those for New York : stmt_filtered
# where() method on a select() object returns a new select() object with the added where clause.
stmt_filtered = stmt.where(census.columns.state == 'New York')

# Execute the query to retrieve all the data returned: results
results = connection.execute(stmt_filtered).fetchall()

#  loop over the Resultts and print the age, sex, and pop2000
for result in reults:
    print(result.age, result.sex, result.pop2000)


#################### Filter  data selected from a Table -Expression#########################

# Define a list of states for which we want results
states = ['New York', 'California', 'Texas']

# Create a query for the census table: stmt
stmt = select([census])

# Append a where clause to match all the states in the states list
# in_() method on a column returns a Boolean expression that will be True if the value of the column matches any value in the list.
stmt = stmt.where(census.columns.state.in_(states))

# Loop over the ResultProxy and print the state and its population in 2000
for result in connection.execute(stmt):
    print(result.state, result.pop2000)


#################### Filter  data selected from a Table - Advanced#########################
# and_() method on a column returns a Boolean expression that will be True if the value of the column matches all the values in the list.
# '_'  underscore is used  in and, or not to avoid conflict with python keywords.

# Import and_

# # Build a query for the census table: stmt
stmt = select([census])

# Append a where clause to select only non-male records from California using and_
stmt = stmt.where(
    # The state  os california with a non-male sex
    and_(census.columns.state == 'California',
         census.columns.sex != 'M'
         )
)

# Loop over the Result proxy printing the age and SEX
# connection.execute(stmt) gives resultproxy
for result in connection.execute(stmt):
    print(result.age, result.sex)


################################ Ordering by a single column #########################

# Build a query to select the state column: stmt
stmt = select([census.columns.state])

# Order stmt by the state column
# order_by() method on a select() object returns a new select() object with the added order_by clause.
stmt = stmt.order_by(census.columns.state)

# Execute the query and store the results: results
# fetchall() returns all the rows of a query result.
results = connection.execute(stmt).fetchall()

# Print the first 10 results
print(results[:10])  # print first 10 rows of results


################################ Ordering in descending order, by a single column #########################
# smilar to above but use desc() method on a column to order in descending order.

# Import desc

# Build a query to select the state column: stmt
stmt = select([census.columns.state])

# Order stmt by state in descending order: rev_stmt
rev_stmt = stmt.order_by(desc(census.columns.state))

# Execute the query and store the results: rev_results
rev_results = connection.execute(rev_stmt).fetchall()

# Print the first 10 rev_results
print(rev_results[:10])


################################ Ordering by multiple columns #########################
# for multiple columns, pass a list of columns to the order_by() method.
# first column is ordered then matching rows are ordered by second column.

# Build a query to select state and age: stmt
stmt = select([census.columns.state, census.columns.age])

# Append order by to ascend by state and descend by age
# order by state in ascending order and age in descending order.
stmt = stmt.order_by(census.columns.state, desc(census.columns.age))

# Execute the statement and store all the records: results
results = connection.execute(stmt).fetchall()

# Print the first 20 results
print(results[:20])


# count() method on a select() object returns the number of rows in the result set returned by the select() object.
# distinct() method on a column returns a new column that only returns distinct values in the column.
# SQl aggregate functions like count() and sum() are called on a select() object using the .scalar() method.and are insides the func() function.
# scalar() method returns the first column of the first row of the result set returned by the select() object.
# Groupby() method on a select() object returns a new select() object with the added group_by clause.
# label() method on a column returns a new column with the added label. similar to alias AS in SQL.

################################ Counting Distinct Data #########################

# Build a query to count the distinct states values: stmt
stmt = select([func.count(census.columns.state.distinct())])

# Execute the query and store the scalar result: distinct_state_count
distinct_state_count = connection.execute(stmt).scalar()

# Print the distinct_state_count
print(distinct_state_count)


################################ Count of Records by State #########################
# import func

# Build a query to select the state and count of age: stmt
stmt = select([census.columns.state, func.count(census.columns.age)])

# Group stmt by state
stmt = stmt.group_by(census.columns.state)

# Execute the query and store the results: results
results = connection.execute(stmt).fetchall()

# Print the results
print(results)

# Print the keys/column names of the results returned
# keys() method on a ResultProxy returns the column names of the results.
print(results[0].keys())


################################ Determining the Population Sum by State #########################
# import func

# build an expression to calculate the sum of pop2008 labeled as population
pop2008_sum = func.sum(census.columns.pop2008).label('population')

# Build a query to select the state and sum of pop2008: stmt
stmt = select([census.columns.state, pop2008_sum])

# Group stmt by state
stmt = stmt.group_by(census.columns.state)

# Execute the query and store the results: results
results = connection.execute(stmt).fetchall()

# Print the results
print(results)

# Print the keys/column names of the results returned
# now we have population column in the result instead of sum_1
print(results[0].keys())


################################ ResultsSets and pandas DataFrames #########################
# import pandas

# create a DataFrame df from the ResultSet results
df = pd.DataFrame(results)

# Set the DataFrame's column names
df.columns = results[0].keys()  # Tuple unpacking

# Print the Dataframe
print(df)


################################ From SQLAlchemy results to a Graph #########################
# import matplotlib

# create a dataframe df from the results
df = pd.DataFrame(results)

# Set the DataFrame's column names
df.columns = results[0].keys()

# plot a bar chart of the results
df.plot.bar(x='state', y='population', rot=90, title='Population by State', legend=False, figsize=(
    10, 7), fontsize=12, color='red', alpha=0.5, edgecolor='black', linewidth=1, grid=True)
plt.show()


# perform arithematic operations on columns of a DataFrame.
# Case statement is a list of tuples. Each tuple contains a condition, a value, and a value to return if the condition is false.
# syntaxc for case statement is case([(condition, if_true_value)], else=value)
# cast() method on a column returns  a new column converted to a different type. like cast(census.columns.pop2008, Integer) converts pop2008 column to integer.

################################ Connecting to a MySQL database #########################
# Import create_engine function

# Create an engine to the census database
engine = create_engine(
    'mysql+pymysql://student:datacamp@courses.csrrinzqubik.us-east-1.rds.amazonaws.com:3306/census')  # mysql+pymysql://username:password@host:port/database

# Print the table names
print(engine.table_names())


################################ Calculating a Difference between Two Columns #########################
# Build query to return state names by population difference from 2008 to 2000: stmt
stmt = select([census.columns.state, (census.columns.pop2008 -
              census.columns.pop2000).label('pop_change')])

# Append group by for the state: stmt_grouped
stmt_grouped = stmt.group_by(census.columns.state)

# Append order by for pop_change descendingly: stmt_ordered
stmt_ordered = stmt_grouped.order_by(desc('pop_change'))

# Return only 5 results: stmt_top5
# limit() method on a select() object returns a new select() object with the added limit clause.
stmt_top5 = stmt_ordered.limit(5)

# Use connection to execute stmt_top5 and fetch all results
results = connection.execute(stmt_top5).fetchall()

# Print the state and population change for each record
for result in results:
    print('{}:{}'.format(result.state, result.pop_change))


################################ Determining the Overall Percentage of women  ###################################
# import case, cast and Float from sqlalchemy

# Build an expression to calculate female population in 2000
female_pop2000 = func.sum(
    case([
        (census.columns.sex == 'F', census.columns.pop2000)
    ], else_=0))

# Cast an expression to calculate total population in 2000 to Float
total_pop2000 = cast(func.sum(census.columns.pop2000), Float)

# Build a query to calculate the percentage of women in 2000: stmt
stmt = select([female_pop2000 / total_pop2000 * 100])

# Execute the query and store the scalar result: percent_female
percent_female = connection.execute(stmt).scalar()

# Print the percentage
print(percent_female)


# Relationships  helps to avoid duplicate data , easy to update , normalize data
# SQlalchemy automatically adds right join clause if tables has established relationship

########################################### Automatic joins with an established relationship #########################

# Build a statement to join census and state_fact tables: stmt
stmt = select([census.columns.pop2000, state_fact.columns.abbreviation])

# execute the statement and get the first result: result
result = connection.execute(stmt).first()

# loop over the keys in the result object and print the key and value
for key in result.keys():
    print(key, getattr(result, key))


########################################### Joins #########################
# join syntax is table1.join(table2, condition)
# select([table1, table2]) is equivalent to select([table1]).select_from(table2)

# Build a statement to select the census and state_fact tables: stmt
stmt = select([census, state_fact])

# Add a select_from clause that wraps a join for the census and state_fact
# tables where the census state column and state_fact name column match
stmt_join = stmt.select_from(
    census.join(state_fact, census.columns.state == state_fact.columns.name))

# Execute the statement and get the first result: result
result = connection.execute(stmt_join).first()

# Loop over the keys in the result object and print the key and value
for key in result.keys():
    print(key, getattr(result, key))


########################################### More Practice with Joins #########################

# Build a statement to select the state, sum of 2008 population and census division name: stmt
stmt = select([
    census.columns.state,
    func.sum(census.columns.pop2008),
    state_fact.columns.census_division_name
])

# Append select_from to join the census and state_fact tables by the census state and state_fact name columns
stmt_joined = stmt.select_from(
    census.join(state_fact, census.columns.state == state_fact.columns.name)
)

# Append a group by for the state_fact name column
stmt_grouped = stmt_joined.group_by(state_fact.columns.name)

# Execute the statement and get the results: results
results = connection.execute(stmt_grouped).fetchall()

# Loop over the results object and print each record.
for record in results:
    print(record)


# Hierarchical tables are tables that have relationships with themselves. tables that contain hierarchical data, such as employees and managers who are also employees
# alias() method on a table creates an alias of the table. so allow to use same table multiple times in a query.
# syntax is  alias_name = table_object.alias( )
# alias_name.c.column_name is used to refer to a column of an aliased table.

########################################### Using alias to handle same table joined queries #########################
# Make an alias of the employees table: managers
managers = employees.alias()

# Build a query to select names of managers and their employees: stmt
stmt = select(
    [managers.c.name.label('manager'),
     employees.c.name.label('employee')]
)

# Match managers id with employees mgr: stmt_matched
stmt_matched = stmt.where(managers.c.id == employees.c.mgr)

# Order the statement by the managers name: stmt_ordered
stmt_ordered = stmt_matched.order_by(managers.c.name)

# Execute statement: results
results = connection.execute(stmt_ordered).fetchall()

# Print records
for record in results:
    print(record)


#########################Leveraging Functions and Group_bys with Hierarchical Tables #########################

# Make an alias of the employees table: managers
managers = employees.alias()

# Build a query to select names of managers and counts of their employees: stmt
stmt = select([managers.columns.name, func.count(employees.columns.id)])

# Append a where clause that ensures the manager id and employee mgr are equal
stmt_matched = stmt.where(managers.columns.id == employees.columns.mgr)

# Group by Managers Name
stmt_grouped = stmt_matched.group_by(managers.columns.name)

# Execute statement: results
results = connection.execute(stmt_grouped).fetchall()

# print manager
for record in results:
    print(record)

##################  Working on Blocks of Records #########################
# fetchmany() method on a ResultProxy returns a list of tuples corresponding to a specified number of rows.
# .Close the ResultProxy and Connection after fetching all the records.

# Start a while loop checking for more results
while more_results:
    # Fetch the first 50 results from the ResultProxy: partial_results
    partial_results = results_proxy.fetchmany(50)

    # if empty list, set more_results to False
    if partial_results == []:
        more_results = False

    # Loop over the fetched records and increment the count for the state
    for row in partial_results:
        if row.state in state_count:
            state_count[row.state] += 1
        else:
            state_count[row.state] = 1

# Close the ResultProxy, and thus the connection
results_proxy.close()

# Print the count by state
print(state_count)


###################### Creating tables with SQLAlchemy #########################
# Import Table, Column, String, Integer, Float, Boolean from sqlalchemy

# Define a new table with a name, count, amount, and valid column: data
data = Table('data', metadata,
             Column('name', String(255)),
             Column('count', Integer()),
             Column('amount', Float()),
             Column('valid', Boolean())
             )

# Use the metadata to create the table
metadata.create_all(engine)

# Print table details
print(repr(data))

#####################  Constraints and data defaults #########################
# Import Table, Column, String, Integer, Float, Boolean from sqlalchemy


# Define a new table with a name, count, amount, and valid column: data
data = Table('data', metadata,
             Column('name', String(255), unique=True),
             Column('count', Integer(), default=1),
             Column('amount', Float()),
             Column('valid', Boolean(), default=False)
             )

# Use the metadata to create the table
metadata.create_all(engine)

# Print the table details
print(repr(metadata.tables['data']))


##################### Inserting a single row with an insert() statement #########################

# Import insert and select from sqlalchemy

# Build an insert statement to insert a record into the data table: insert_stmt
# insert syantax is insert(table).values(column1=value1, column2=value2)
insert_stmt = insert(data).values(
    name='Anna', count=1, amount=1000.00, valid=True)

# Execute the insert statement via the connection: results
results = connection.execute(insert_stmt)

# Print result rowcount
print(results.rowcount)

# Build a select statement to validate the insert: select_stmt
select_stmt = select([data]).where(data.columns.name == 'Anna')

# Print the result of executing the query.
# first() method returns the first row of the result set.
print(connection.execute(select_stmt).first())


###################### Inserting multiple records at once #########################

# Build a list of dictionaries: values_list
values_list = [
    {'name': 'Anna', 'count': 1, 'amount': 1000.00, 'valid': True},
    {'name': 'Taylor', 'count': 1, 'amount': 750.00, 'valid': False}
]

# Build an insert statement for the data table: stmt
stmt = insert(data)

# Execute stmt with the values_list: results
results = connection.execute(stmt, values_list)

# Print rowcount
print(results.rowcount)


################## Loading a CSV into a table #########################
# import pandas

# read census.csv into a DataFrame : census_df
census_df = pd.read_csv("census.csv", header=None)

# rename the columns of the census DataFrame
census_df.columns = ['state', 'sex', 'age', 'pop2000', 'pop2008']

# append the data from census_df to the "census" table via connection
census_df.to_sql(name="census", con=connection,
                 if_exists="append", index=False)

######################### Updating individual records #########################
# Build a select statement: select_stmt
select_stmt = select([state_fact]).where(state_fact.columns.name == 'New York')

# Execute select_stmt and fetch the results
results = connection.execute(select_stmt).fetchall()

# Print the results of executing the select_stmt
print(results)

# Print the FIPS code for the first row of the result
print(results[0]['fips_state'])


###################### Updating multiple records #########################
# Build a statement to update the notes to 'The Wild West': stmt
stmt = update(state_fact).values(notes='The Wild West')

# Append a where clause to match the West census region records: stmt_west
stmt_west = stmt.where(state_fact.columns.census_region_name == 'West')

# Execute the statement: results
results = connection.execute(stmt_west)

# Print rowcount
print(results.rowcount)


###################### Correlated Updates #########################
# Build a statement to select name from state_fact: fips_stmt
fips_stmt = select([state_fact.columns.name])

# Append a where clause to match the fips_state to  flat_census fips_code: fips_stmt
fips_stmt = fips_stmt.where(
    state_fact.columns.fips_state == flat_census.columns.fips_code)

# Build an update statement to set the state_name to fips_stmt_where: update_stmt
update_stmt = update(flat_census).values(state_name=fips_stmt)

# Execute update_stmt: results
results = connection.execute(update_stmt)

# Print rowcount
print(results.rowcount)


# delete() function to delete all the records from a table.
# drop_all() method on the MetaData to remove the table from the database.
# drop() method on a Table to remove the table from the database.

###################### Deleting all the records from a table #########################
# Import delete, select

# Build a statement to empty the census table: stmt
delete_stmt = delete(census)

# Execute the statement: results
results = connection.execute(delete_stmt)

# Print affected rowcount
print(results.rowcount)

# Build a statement to select all records from the census table : select_stmt
select_stmt = select([census])

# Print the results of executing the statement to verify there are no rows
print(connection.execute(select_stmt).fetchall())


###################### Deleting  Specific records #########################

# Build a statement to count records using the sex column for Men ('M') age 36: count_stmt
count_stmt = select([func.count(census.columns.sex)]).where(
    and_(census.columns.sex == 'M',
         census.columns.age == 36)
)

# Execute the select statement and use the scalar() fetch method to save the record count
# scalar() returns the first column of the first row
to_delete = connection.execute(count_stmt).scalar()

# Build a statement to delete records from the census table: delete_stmt
delete_stmt = delete(census)

# Append a where clause to target Men ('M') age 36: delete_stmt
delete_stmt = delete_stmt.where(
    and_(census.columns.sex == 'M',
         census.columns.age == 36)
)

# Execute the statement: results
results = connection.execute(delete_stmt)

# Print affected rowcount and to_delete record count, make sure they match
print(results.rowcount, to_delete)


###################### Deleting a Table Completely #########################

# drop syntax is table.drop(engine)

# Drop the state_fact table
state_fact.drop(engine)

# Check to see if state_fact exists
print(state_fact.exists(engine))

# Drop all tables
metadata.drop_all(engine)

# Check to see if census exists
print(engine.table_names())


########################  Setup an engine and metadata #########################

# Import create_engine, MetaData

# Define an engine to connect to chapter5.sqlite: engine
engine = create_engine('sqlite:///chapter5.sqlite')

# Initialize MetaData: metadata
metadata = MetaData()


######################### Create a Table to the Database #########################
# Import Table, Column, String, and Integer

# Build a census table: census with columns state,sex,age,pop2000,pop2008
census = Table('census', metadata,
               Column('state', String(30)),
               Column('sex', String(1)),
               Column('age', Integer()),
               Column('pop2000', Integer()),
               Column('pop2008', Integer()))

# Create the table in the database
metadata.create_all(engine)


######################### Reading the data from the CSV #########################

# Create an empty list: values_list
values_list = []

# Iterate over the rows
for row in csv_reader:
    # Create a dictionary with the values
    data = {'state': row[0], 'sex': row[1], 'age': row[2],
            'pop2000': row[3], 'pop2008': row[4]}

    # Append that dictionary to the values list
    values_list.append(data)

#################### Load data from a list into the Table###################
# Import insert

# Build an insert statement : stmt
stmt = insert(census)

# Use values_list to insert data: results
results = connection.execute(stmt, values_list)

# Print rowcount
print(results.rowcount)


#################### Determine the average age by population #########################
# Import select and func

# select the average age weighted by pop2000
# Modify the select statement to alias the new column with weighted average as 'average_age' using .label().
stmt = select([(func.sum(census.columns.pop2000 * census.columns.age) /
              func.sum(census.columns.pop2000)).label('average_age')])

# Modify the select statement to select the sex column of census in addition to the weighted average, with the sex column coming first.
stmt = select([census.columns.sex,
               (func.sum(census.columns.pop2000 * census.columns.age)
                / func.sum(census.columns.pop2000)).label('average_age')
               ])

# Group by sex
stmt = stmt.group_by(census.columns.sex)

# Execute the query and fetch all the results
results = connection.execute(stmt).fetchall()

# print the sex and average age column for each result
for result in results:
    print(result.sex, result.average_age)


######################## Determine the percentage of population by gender and state ##############
# import case, cast and Float from sqlalchemy

# Build a query to calculate the percentage of women in 2000: stmt
stmt = select([census.columns.state,
               (func.sum(
                   case([
                       (census.columns.sex == 'F', census.columns.pop2000)
                   ], else_=0)) /
                   cast(func.sum(census.columns.pop2000), Float) * 100).label('percent_female')
               ])

# Group By state
stmt = stmt.group_by(census.columns.state)

# Execute the query and store the results: results
results = connection.execute(stmt).fetchall()

# Print the percentage
for result in results:
    print(result.state, result.percent_female)


##################### Determine the difference by state from the 2000 and 2008 censuses ###########
# Build query to return state name and population difference from 2008 to 2000
stmt = select([census.columns.state,
               (census.columns.pop2008-census.columns.pop2000).label('pop_change')
               ])

# Group by State
stmt = stmt.group_by(census.columns.state)

# Order by Population Change
stmt = stmt.order_by(desc('pop_change'))

# Limit to top 10
stmt = stmt.limit(10)

# Use connection to execute the statement and fetch all results
results = connection.execute(stmt).fetchall()

# Print the state and population change for each record
for result in results:
    print('{}:{}'.format(result.state, result.pop_change))
