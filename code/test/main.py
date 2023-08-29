import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

# Define the database connection and session
engine = create_engine('sqlite:///./test.db')
Session = sessionmaker(bind=engine)
session = Session()

# Define the base class for declarative models
Base = declarative_base()

# Define the association table between Entry and Language
entry_spoken_language_association = Table('entry_spoken_language_association', Base.metadata,
    Column('entry_id', Integer, ForeignKey('entries.id')),
    Column('language_id', Integer, ForeignKey('languages.id'))
)

entry_learn_language_association = Table('entry_learn_language_association', Base.metadata,
    Column('entry_id', Integer, ForeignKey('entries.id')),
    Column('language_id', Integer, ForeignKey('languages.id'))
)

# Define the Language model
class Language(Base):
    __tablename__ = 'languages'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # Adding unique constraint
    
# Define the Entry model
class Entry(Base):
    __tablename__ = 'entries'
    
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    name = Column(String)
    
    spoken_languages = relationship("Language", secondary=entry_spoken_language_association, backref="spoken_by")
    learn_languages = relationship("Language", secondary=entry_learn_language_association, backref="learners")

# Create the tables in the database
Base.metadata.create_all(engine)

# Read the CSV file using pandas
csv_file = 'entries.csv'
data = pd.read_csv(csv_file)

# Process the CSV data and populate the database
for index, row in data.iterrows():
    spoken_languages = row['languages'].split(';') if pd.notnull(row['languages']) else []
    learn_languages = row['languages to learn'].split(';') if pd.notnull(row['languages to learn']) else []

    spoken_language_objects = []
    for lang in spoken_languages:
        language = session.query(Language).filter_by(name=lang).first()
        if lang and not language:
            language = Language(name=lang)
            session.add(language)
        if language:
            spoken_language_objects.append(language)

    learn_language_objects = []
    for lang in learn_languages:
        language = session.query(Language).filter_by(name=lang).first()
        if lang and not language:
            language = Language(name=lang)
            session.add(language)
        if language:
            learn_language_objects.append(language)

    entry = Entry(year=row['year'], name=row['name'], spoken_languages=spoken_language_objects, learn_languages=learn_language_objects)
    session.add(entry)

session.commit()
print("Database populated successfully!")

# Query and display elements from the Entry table
entries = session.query(Entry).all()
print("Entries:")
for entry in entries:
    spoken_language_names = ', '.join([language.name for language in entry.spoken_languages])
    learn_language_names = ', '.join([language.name for language in entry.learn_languages])
    print(f"ID: {entry.id}, Year: {entry.year}, Name: {entry.name}, Spoken Languages: {spoken_language_names}, Languages to Learn: {learn_language_names}")

# Query and display elements from the Language table
languages = session.query(Language).all()
print("\nLanguages:")
for language in languages:
    print(f"ID: {language.id}, Name: {language.name}")

