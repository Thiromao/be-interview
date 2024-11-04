from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select, Session
from typing import Optional

from app.db import get_db
from app.models import Location, Organisation

router = APIRouter()

# I just use my Organisation model to create an organisation
@router.post("/create", response_model=Organisation, tags=["Organisation"])
def create_organisation(organisation: Organisation, 
                        session: Session = Depends(get_db)) -> Organisation:
    """
    Create an organisation.
    """
    session.add(organisation)
    session.commit()
    session.refresh(organisation)
    return organisation


@router.get("/", response_model=list[Organisation], tags=["Organisation"])
def get_organisations(session: Session = Depends(get_db)) -> list[Organisation]:
    """
    Get all organisations.
    """
    organisations = session.exec(select(Organisation)).all()
    return organisations


@router.get("/{organisation_id}", response_model=list[Organisation], tags=["Organisation"])
def get_organisation(organisation_id: int,
                    session: Session = Depends(get_db)) -> list[Organisation]:
    """
    Get organisation by id.
    """
    organisation = session.get(Organisation, organisation_id)
    if organisation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")
    return organisation

# I'm sure we could mex those two functions : If and ID is given, retrieve the data from this ID,
#Otherwise, retrieve all the data available
# I've written this, it doesn't work, but I'm close to the two hours needed to do the test.

# @router.get("/{organisation_id}", response_model=list[Organisation], tags=["Organisation"])
# def get_organisation(organisation_id: Optional[int] = None,
#                     session: Session = Depends(get_db)) -> list[Organisation]:
#     """
#     Get organisation by id.
#     """
#     #Check if and id is given
#     if organisation_id : 
#         organisation = session.get(Organisation, organisation_id)
#         #Check if the ID is in the Database
#         if organisation is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")
#         return organisation
#     #If no id is given 
#     organisations = session.exec(select(Organisation)).all()
#     return organisations


@router.post("/create/locations", response_model= Location, tags=["Location"]) # The response_model defeind if my models.py
#I specify that my location wil lhave the same model as Location,
# My sessions is defined in model.py and it should sent the result as the Location model
def create_location(location : Location,
                    session: Session = Depends(get_db)) -> Location : 
    """
    Create a location for an organisation
    """
    #Check if the organisation already exist in the database 
    organisation = session.get(Organisation, location.organisation_id)
    if organisation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")
    #Create the data and add it to the database
    session.add(location)
    session.commit()
    session.refresh(location)
    return location



@router.get("/{organisation_id}/locations", response_model=list[Location],  tags=["Location"]) #I want the location to be stored in a list of multiple Location's model
def get_organisation_locations(organisation_id: int, 
                               bounding_box: Optional[tuple[float, float, float, float]], #Define the optionnal parameter  
                               session: Session = Depends(get_db)) -> list[Location] : 
    """
    Retrieve the locations for an organisation as a list
    """
    organisation = session.get(Organisation, organisation_id) #Check if the Id exist
    if organisation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")
    if bounding_box: #If the bounding box is specified
        # Stored the bounding box inside different variables for readability
        min_latitude, min_longitude, max_latitude, max_longitude = bounding_box
    
        # Store all my location into a variable, to check if they are completly inside my bounding box 
        all_locations = organisation.locations 
        # Check for each location's latitude and logntiude if they are in the bounding box,
        # if so, I store it in a list
        final_locations = [individual_location for individual_location in all_locations 
                           if (min_latitude < individual_location.latitude < max_latitude and
                               min_longitude < individual_location.longitude < max_longitude)]
        return final_locations
    
    return organisation.locations