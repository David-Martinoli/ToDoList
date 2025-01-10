from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.task import Base, Task

class DataBase:
    def __init__(self):
        self.engine = create_engine('sqlite:///tasks.db')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def add_task(self, task):
        session = self.Session()
        session.add(task)
        session.commit()
        session.close()
    
    def get_tasks(self):
        session = self.Session()
        tasks = session.query(Task).all()
        session.close()
        return tasks
    
    def delete_task(self, task):
        session = self.Session()
        session.delete(task)
        session.commit()
        session.close()
    
    def update_task(self, task):
        session = self.Session()
        session.merge(task)
        session.commit()
        session.close()
