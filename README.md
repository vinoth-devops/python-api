# Demo App

This is a demo app that will be used to manage the city population. We have python fast API in the app server and elasticsearch as a Database.
We will have below three endpoints from the app-server.

- `http://localhost:8000/health`
    This will check both elastic search and app health status and return `OK` if everything is fine.
- `http://localhost:8000/city/population`
    This will list all cities and its population which is in DB.
- `http://localhost:8000/city/add`
    This will help us to add or update the city details.

## prerequisites

- Install minikube software to run kubernetes cluster locally.
- Install docker, kubectl and helm to execute this demo.

## Installation

- start minikube and check it is running fine.

  `minikube start`

- Build a docker image

  `docker build -t app:1.0 .`

- Import the app image and elasticsearch image to minikube

  `docker pull elasticsearch:8.5.0`
  `minikube image load elasticsearch:8.5.0`

  `minikube image load app:1.0`

- Run the helm install to install both the es and app.

  `helm install app ./deploy/helm/app`

  `helm install es ./deploy/helm/es`

## Demo

- Run the below command to expose the app command to machine.
  `kubectl port-forward svc/app 8000:8000`

- Check the status

  `http://localhost:8000/health`
   output: `"OK"`

- Upload the city details

  `curl -X POST "http://localhost:8000/city/add" -H 'Content-Type: application/json' -d'
 {
 "id":1,
 "city" : "trichy",
 "population":"11232"
 }'`

 output: `"City population details are created"` or
         `"City population details are updated"`

- List the city population

  `http://localhost:8000/city/population`

   output: `["id city population "]["2 Dubai 100"]`
