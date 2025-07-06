from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model.base import Base

# colunas = Student_ID,Age,Gender,Academic_Level,Country,Avg_Daily_Usage_Hours,Most_Used_Platform,Affects_Academic_Performance,
# Sleep_Hours_Per_Night,Mental_Health_Score,Relationship_Status,Conflicts_Over_Social_Media,

class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True)
    age= Column("Age", Integer)
    gender = Column("Gender", Integer)
    academic_level = Column("Academic_Level", Integer)
    country = Column("BloodPressure", Integer)
    avg_daily_usage_hours = Column("Avg_Daily_Usage_Hours", Float)
    most_used_platform = Column("Most_Used_Platform", Integer)
    affects_academic_performance = Column("Affects_Academic_Performance", Integer)
    sleep_hours_per_night = Column("Sleep_Hours_Per_Night", Float)
    mental_health_score = Column("Mental_Health_Score", Integer)
    relationship_status = Column("Relationship_Status", Integer)
    conflicts_over_social_media = Column("Conflicts_Over_Social_Media", Integer)
    outcome = Column(Integer)


    def __init__(self, age:int, gender:int, academic_level:int,
                 country:int, avg_daily_usage_hours:float, most_used_platform:int,
                 affects_academic_performance:int, sleep_hours_per_night:float, mental_health_score:int,
                 relationship_status:int, conflicts_over_social_media:int, outcome:int):
        """
        Cria um Aluno

        Arguments:
        age:
        gender:
        academic_Level:
        country:
        avg_Daily_Usage_Hours:
        most_Used_Platform:
        affects_Academic_Performance:
        sleep_Hours_Per_Night:
        mental_Health_Score:
        relationship_Status:
        conflicts_Over_Social_Media:
        """
        # inicializa os atributos do aluno
        self.age= age
        self.gender = gender
        self.academic_level = academic_level
        self.country = country
        self.avg_daily_usage_hours = avg_daily_usage_hours
        self.most_used_platform = most_used_platform
        self.affects_academic_performance = affects_academic_performance
        self.sleep_hours_per_night = sleep_hours_per_night
        self.mental_health_score = mental_health_score
        self.relationship_status = relationship_status
        self.conflicts_over_social_media = conflicts_over_social_media
        # o outcome é a predição do modelo, que deve ser informada
        self.outcome = outcome