from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from faker import Faker

fake = Faker()

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)


engine = create_engine('postgresql://postgres:vfrc3224@localhost/fastapi_db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def create_contact():
    return Contact(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        birthday=fake.date_of_birth(),
        additional_info=fake.text() if fake.boolean(chance_of_getting_true=50) else None
    )


for _ in range(10):
    contact = create_contact()
    session.add(contact)

session.commit()

session.close()
