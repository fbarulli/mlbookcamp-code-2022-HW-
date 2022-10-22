import numpy as np
import xgboost 
import bentoml
from bentoml.io import JSON
from pydantic import BaseModel

class UserProfile(BaseModel):
    name: str
    age : int
    country : str
    rating : float









model_ref = bentoml.sklearn.get("mlzoomcamp_homework:qtzdz3slg6mwwdu5")
#dv = model_ref.custom_objects['dictVectorizer']

model_runner = model_ref.to_runner()

svc = bentoml.Service("credit_risk_classifier", runners=[model_runner])


@svc.api(input=JSON(pydantic_model=UserProfile), output=JSON())
async def classify(UserProfile):
    user_profile_data = UserProfile.dict()
    vector = dv.transform(user_profile_data)
    prediction = await model_runner.predict.async_run(vector)
    print(prediction)
    result = prediction[0]

    if result > 0.5:
        return {
            "status": "DECLINED"
        }
    elif result > 0.25:
        return {
            "status": "MAYBE"
        }
    else:
        return {
            "status": "APPROVED"
        }
