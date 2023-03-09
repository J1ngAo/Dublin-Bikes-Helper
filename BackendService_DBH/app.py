import json
from flask import Flask
from sqlalchemy import create_engine, select, MetaData, Table
app = Flask(__name__)


@app.route('/')
def index():
    # get db connection
    # engine = create_engine('postgresql://masterAdmin:4hvJWtw1P4cV7Xm0JQno@database-ddrangers.cftjf3yfdzfx.eu-west-1.rds.amazonaws.com:3306/bike_static_test')
    with open("config.json", "r") as jsonfile:
        configFile = json.load(jsonfile)
        print("successfully loading Json config file...")
    print("reading config file:", configFile)
    username = configFile['username']
    password = configFile['password']
    host = configFile['host']
    port = configFile['port']
    database_name = configFile['database_name']
    # assemble the connection string
    connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'
    # # The Engine is a factory that can create new database connections for us, which also holds onto connections in Connection Pool for fast reuse.
    engine = create_engine(connection_string, echo=True)
    # creat database object
    metadata = MetaData()
    bike_static_test = Table('bike_static_test', metadata, autoload_with=engine)

    # # the column we need
    # columns = ['indexNumber', 'name', 'address', 'location_lat', 'location_lon']
    #
    # # query the data for specified columns
    # stmt = select([getattr(bike_static_test.c, column) for column in columns])

    stmt = select(
        bike_static_test.c.indexNumber,
        bike_static_test.c.name,
        bike_static_test.c.address,
        bike_static_test.c.location_lat,
        bike_static_test.c.location_lon
    )

    # execute the query and get result
    with engine.connect() as conn:
        results = conn.execute(stmt).fetchall()

    # turn the format of result to json
    json_results = json.dumps([dict(row) for row in results])

    return json_results


@app.route('/contact')
def contact():
    # get db connection
    return "app.send_static_file(‘contact.html')"


@app.route('/stations')
def stations():
    # get db connection
    return "list of stations"


@app.route('/stations/<int:station_id>')
def station(station_id):
    # show the station with the given id, the id is an integer
    return 'Retrieving info for Station: {}'.format(station_id)