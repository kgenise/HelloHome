from sqlalchemy import *
from config import host, port, database, user, password

conn_str = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_engine(conn_str)
connection = engine.connect()

metadata = MetaData()
# first_tb = Table('first_table', metadata,
#    Column('id', Integer, primary_key=True),
#    Column('name', String(255), nullable=False),
#    Column('isHappy', Boolean, nullable=False)
# )

user_tb = Table('users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('account_type', String(5)),
    Column('fname', String(20)),
    Column('lname', String(20)),
    Column('email', String(100), unique=True),
    Column('pw', String(100), nullable=False),
    Column('phone', String(22)),
    Column('company', String(100))
)

metadata.create_all(engine)
query = insert(user_tb).values(fname='JohnMcMillion', account_type='agent', lname='Marge', email='m.marge@test.com', pw='testing')
ResultProxy = connection.execute(query)