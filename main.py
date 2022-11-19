from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()

class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cpf = Column(String(11), nullable=False)
    address = Column(String(50))

    conta = relationship(
        "Conta", back_populates="client", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Client(ID:{self.id}, Name:{self.name}, CPF:{self.cpf}, Address:{self.address})"


class Conta(Base):
    __tablename__ = 'conta'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    agency = Column(String)
    number = Column(Integer, nullable=False)
    id_client = Column(Integer, ForeignKey("client.id"), nullable=False)
    saldo = Column(Float, nullable=False)

    client = relationship(
        "Client", back_populates="conta"
    )

    def __repr__(self):
        return f"Conta(ID:{self.id}, Type:{self.type}, Agency:{self.agency}, Number:{self.number}, Saldo:{self.saldo}" \
               f", Foreignkey: {self.id_client}) "


print(Client.__tablename__)

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("client"))


with Session(engine) as session:
    william = Client(
        name="William Santos",
        cpf="11122233344",
        address="Av. Industrial Urbana",

    )
    will = Conta(
        type="Corrente",
        agency="001",
        number=1234,
        saldo=1000.0,
        id_client=1
    )

    session.add_all([william, will])

    session.commit()

stmt = select(Client).where(Client.id.in_([1]))

print('\n Recuperando conta a partir de condição de filtragem')
for client in session.scalars(stmt):
    print(client)

stmt_conta = select(Conta).where(Conta.id.in_([1]))
for conta in session.scalars(stmt_conta):
    print(conta)