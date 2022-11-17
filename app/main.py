#import packages
from fastapi import FastAPI
from elasticsearch import Elasticsearch
from pydantic import BaseModel

#create model for post method to update the city details
class Item(BaseModel):
    id: int
    city: str
    population: str

#create instances
es = Elasticsearch('http://es:9200')
app = FastAPI()

#return values for home page
@app.get("/")
def root():
    return "City population api is running..."

#health check
@app.get("/health")
def healthcheck():
    if not es.ping():
        return "Elasticsearch server is down"
    else:
        return "OK"

#list the population
@app.get("/city/population")
def city_population():
    if not es.ping():
        return "Elasticsearch server is down"
    else:
        if es.indices.exists(index="city_details"):
            resp = es.search(index="city_details", query={"match_all": {}})
            print("Got %d Hits:" % resp['hits']['total']['value'])
            my_list = []
            for hit in resp['hits']['hits']:
                my_list.append(hit["_id"] + " %(city)s %(population)s" % hit["_source"])
            return my_list
        else:
            return "City details are not updated."

#create or update city population details
@app.post("/city/add")
async def create_item(item: Item):
    if not es.ping():
        return "Elasticsearch server is down"
    else:
        item_dict = item.dict()
        doc = {
            'city': item_dict['city'],
            'population': item_dict['population']
        }
        resp = es.index(index="city_details", id=item_dict['id'], document=doc)
        return ("City population details are %s" % resp['result'])
