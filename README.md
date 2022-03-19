## Installation instructions
```
pip3 install -r requirements.txt
```

## To run the app
```
flask run
```

## Update the light settings
### Request
```
POST /light HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Content-Length: 39

{
    "id": "staris",
    "value": 50
}
```
### Response
```
{
    "staris": 50
}
```

Upon every update request the server will compile a string in the format Node understands and will forward the command.

## Update the temperature settings
### Request
```
POST /temperature HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Content-Length: 363

{
   "day": "2022-03-18",
   "floor": 1,
   "mode": "manual",
   "value": 22,
   "periods": [
      {
         "from": "07:00",
         "to": "08:00",
         "value": 22
      },
      {
         "from": "08:00",
         "to": "09:00",
         "value": 23
      },
      {
         "from": "10:00",
         "to": "19:00",
         "value": 23
      }
   ]
}
```
### Response
```
{
    "1": {
        "auto_value": 22,
        "mode": "manual",
        "periods": [
            {
                "from": "07:00",
                "to": "08:00",
                "value": 22
            },
            {
                "from": "08:00",
                "to": "09:00",
                "value": 23
            },
            {
                "from": "10:00",
                "to": "19:00",
                "value": 23
            }
        ]
    }
}
```
Upon every update request the server will compile a string in the format Node understands containing the current temperature and floor, and will forward the command. This also happens every 5 minutes. 
