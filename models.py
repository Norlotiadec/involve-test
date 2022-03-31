from sqlalchemy import MetaData, create_engine, Table, Column, Integer, Float, String
from datetime import datetime

meta = MetaData()

payments = Table('Payment', meta,
                 Column('id_payment', Integer, primary_key=True),
                 Column('currency', String(length=4)),
                 Column('amount', Float),
                 Column('description', String),
                 Column('time_of_departure', String))

engine = create_engine('sqlite:///data_d.db')
meta.create_all(engine)


def add_value(currency: str, amount: float, description: str):
    if currency == '978':
        currency = 'EUR'
    elif currency == '840':
        currency = 'USD'
    else:
        currency = 'RUB'
    conn = engine.connect()
    add_info = payments.insert().values(currency=currency, amount=amount, description=description,
                                        time_of_departure=str(datetime.now()))
    conn.execute(add_info)
