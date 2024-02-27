from sqlalchemy import Column, Integer, ForeignKey, LargeBinary, String, Boolean, DateTime, BigInteger

from web.src.db.db import dfkBase, dfk_session_creator, dfk_engine
from web.src.static.loggers import logger


class LocalHero(dfkBase):
    __tablename__ = 'hero'

    hero_id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    dfk_hero_id = Column(Integer, nullable=False)
    account_id = Column(Integer, ForeignKey('account.account_id'))

    is_full_stamina = Column(Boolean, nullable=False)
    maximum_stamina = Column(Integer, nullable=False)
    current_xp = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)

    current_quest = Column(String, nullable=False)
    quest_start_time = Column(Integer, nullable=True)  # Epoch timestamp of quest end
    quest_end_time = Column(Integer, nullable=True)  # Epoch timestamp of quest end


# class Quest(dfkBase):
#     __tablename__ = 'quest'
#
#     quest_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
#     current_quest = Column(String, nullable=False)

# class QuestInstance
#  quest_id
#  Start time
#  End time

# class Quest(dfkBase):
#     __tablename__ = 'quest'
#
#     # quest_id
#     # Profession
#     # Level
#
#     pass
#

# class Profession
# short_name
# name
#


class Account(dfkBase):
    __tablename__ = 'account'
    account_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    private_key = Column(LargeBinary(), nullable=False)
    public_address = Column(String, nullable=False)


def create_dfk_tables():
    logger.info('Creating DFK database')

    session = dfk_session_creator()
    dfkBase.metadata.create_all(dfk_engine)
    session.commit()