from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, Integer, String, DateTime,Float

from ..database import db
from ..mixins import CRUDModel

class Sklad(CRUDModel):
    __tablename__ = 'sklad'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True )
    Nazev = Column(String, nullable=False, index=True)
    rozmer = Column(Float, nullable=False, index=False)
    kusu = Column(Integer, default=1)
    datum_insertu= Column(DateTime)



    # Use custom constructor
    # pylint: disable=W0231
    def __init__(self, **kwargs):
        self.datum_insertu = datetime.utcnow()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    @staticmethod
    def find_by_nazev(nazev):
        return db.session.query(Sklad).filter_by(Nazev = nazev ).all()

