
from pydantic import BaseModel, Field
from typing import Literal, Annotated
class UserDetail(BaseModel):
    CreditScore:Annotated[int,Field(...,description='CreditScore of Customer',example=300)]
    Geography:Annotated[Literal['Germany','Spain','France'],Field(...,description='Country of Customer',example='France')]
    Gender:Annotated[Literal['Male','Female'],Field(...,description='Gender of Customer',example='Male')]
    Age:Annotated[int,Field(...,lt=120,gt=18,description="Age of Customer",example=50)]
    Tenure:Annotated[int,Field(...,le=10,ge=0,description='Tenure of Customer',example=5)]
    Balance:Annotated[int,Field(...,ge=0,description='Balance of Customer in a Bank',example=5000)]
    NumOfProducts:Annotated[Literal[1,2,3,4],Field(...,descripiton='Features of Bank',example=2)]
    HasCrCard:Annotated[Literal[0,1],Field(...,description='Does Customer have credit card or not',example=0)]
    IsActiveMember:Annotated[Literal[0,1],Field(...,description='Is Customer is an active Member of Bank',example=0)]
    EstimatedSalary:Annotated[int,Field(...,ge=0,description='Estimated Salary of Customer',example=5000)]
