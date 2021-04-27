from asyncpg import Connection
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import (Column, Integer, BigInteger, String,Sequence)
from sqlalchemy import sql

from config import pg_uri

db = Gino()


class Profile(db.Model):
    __tablename__ = 'profile'

    id = Column(Integer, Sequence('profile_id_seq'), primary_key=True)
    uniq_user_id = Column(BigInteger)
    first_name = Column(String(20))
    last_name = Column(String(20))
    username = Column(String(40))
    phone_number = Column(String(20))
    street_name = Column(String(40))
    build_number = Column(Integer)
    apartment_number = Column(Integer)
    user_role = Column(String(20))
    query: sql.Select

    def __repr__(self):
        return "Profile ({} {}: {})".format(self.first_name, self.last_name, self.phone_number)


class DBCommands:
    pool: Connection = db

    async def get_profile(self, uniq_user_id):
        profile = await Profile.query.where(Profile.uniq_user_id == uniq_user_id).gino.first()
        return profile

    async def create_profile(self, user_data):
        profile = await self.get_profile(user_data.get('uniq_user_id'))
        if not profile:
            profile = Profile()
            profile.uniq_user_id = user_data.get('uniq_user_id')
            profile.first_name = user_data.get('first_name')
            profile.last_name = user_data.get('last_name')
            profile.username = user_data.get('username')
            await profile.create()
        return profile


async def create_db():
    await db.set_bind(pg_uri)

    db.gino: GinoSchemaVisitor
    await db.gino.drop_all()
    await db.gino.create_all()
