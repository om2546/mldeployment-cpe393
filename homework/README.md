
# mldeployment-cpe393 homework

  

## Go to homework directory in terminal
```
cd homework
```
## Build Docker image
```
docker build -t homework-64070501015 .
```

## Run Docker container
```
docker run -p 9000:9000 homework-64070501015
```
## Test the API in new terminal

  ```
curl -X POST http://localhost:9000/predict \

-H "Content-Type: application/json" \

-d '{"features": ["yes", "no", "no", "no", "yes", "yes", "furnished", 7420, 4, 2, 3,2]}
```
Describe input
- Binary features (Yes/no)
   - mainroad: "yes"
   - guestroom: "no"
  -  basement: "no"
  - hotwaterheating: "no"
  - airconditioning: "yes"
  - prefarea: "yes"
- Categorical feature
  - furnishingstatus ("unfurnished", "semi-furnished", "furnished"): "furnished" 
 - Numerical features
   - area: 7420
   - bedrooms: 4
   - bathrooms: 2
   - stories: 3
   - parking: 2

expected output
 ```
{"prediction": 11389968}
```
---
  ```
curl -X POST http://localhost:9000/predict \

-H "Content-Type: application/json" \

-d '{"features": [["yes", "no", "no", "no", "yes", "yes", "furnished", 7420, 4, 2, 3,2], \
["yes", "no", "no", "no", "yes", "no", "furnished", 8960, 4, 4, 4,3], \
["yes", "no", "yes", "no", "no", "yes", "semi-furnished", 9960, 3, 2, 2,2]]}
```
expected output
 ```
{"prediction": [11389968,10577560,10319785]}
```


