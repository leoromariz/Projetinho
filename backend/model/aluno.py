from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

# colunas = Student_ID,Age,Gender,Academic_Level,Country,Avg_Daily_Usage_Hours,Most_Used_Platform,Affects_Academic_Performance,
# Sleep_Hours_Per_Night,Mental_Health_Score,Relationship_Status,Conflicts_Over_Social_Media,

class Aluno(Base):
    __tablename__ = 'alunos'
    
    id = Column(Integer, primary_key=True)
    age= Column("Age", Integer)
    gender = Column("Gender", String(50))
    academic_Level = Column("Academic_Level", String(50))
    country = Column("BloodPressure", String(50))
    avg_Daily_Usage_Hours = Column("Avg_Daily_Usage_Hours", Float)
    most_Used_Platform = Column("Most_Used_Platform", String(50))
    affects_Academic_Performance = Column("Affects_Academic_Performance", String(50))
    sleep_Hours_Per_Night = Column("Sleep_Hours_Per_Night", Float)
    mental_Health_Score = Column("Mental_Health_Score", Integer)
    relationship_Status = Column("Relationship_Status", String(50))
    conflicts_Over_Social_Media = Column("Conflicts_Over_Social_Media", Integer)
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(self, conflicts_Over_Social_Media:int, age:int, gender:str, academic_Level:str,
                 country:str, avg_Daily_Usage_Hours:int, most_Used_Platform:str, 
                 affects_Academic_Performance:str, sleep_Hours_Per_Night:Float, mental_Health_Score:int, 
                 relationship_Status:str, data_insercao: Union[DateTime, None] = None):
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
        self.academic_Level = academic_Level
        self.country = country
        self.avg_Daily_Usage_Hours = avg_Daily_Usage_Hours
        self.most_Used_Platform = most_Used_Platform
        self.affects_Academic_Performance = affects_Academic_Performance
        self.sleep_Hours_Per_Night = sleep_Hours_Per_Night
        self.mental_Health_Score = mental_Health_Score
        self.relationship_Status = relationship_Status
        self.conflicts_Over_Social_Media = conflicts_Over_Social_Media

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao