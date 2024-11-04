from sqlmodel import SQLModel, Field, Relationship

# I added the relationship to use the power of SQLModel

#No need to define the Class Base
# class Base(SQLModel):
#     pass

# Not necessary to have a class just for creation, we can use the Organisation's class
# class CreateOrganisation(SQLModel):
#     name: str


class Organisation(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str
    locations: list["Location"] = Relationship(back_populates="organisation")
    #Now, locations will refer to my Location table 

class Location(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    organisation_id: int = Field(foreign_key="organisation.id")
    #Now, organisation will refer to my Organisation table 
    organisation: Organisation =  Relationship(back_populates="locations")
    location_name: str
    longitude: float
    latitude: float
