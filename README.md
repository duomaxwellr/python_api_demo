# Flask demo

## Build docker image

make build

## Run app

make run

## HTTP Port for test

 * http://localhost:5000 flask app port
 * http://localhost:8080 nginx reverse proxy

## API Usage

### API URI

 * http://localhost:8080/userinfo

### Full Json format

```json
{
    "name": "Marcus",
    "job_title": "DevOps",
    "communicate_information": {
        "email": "test@test.com",
        "mobile": "0900000000"
    }
}
```

### GET request body

```json
{
    "name": "Marcus"
}
```

### POST request body

```json
{
    "name": "Marcus",
    "job_title": "DevOps",
    "communicate_information": {
        "email": "test@test.com",
        "mobile": "0900000000"
    }
}
```

### PUT request body

```json
{
    "name": "Marcus",
    "job_title": "DevOps",
    "communicate_information": {
        "email": "test@test.com",
        "mobile": "0900000000"
    }
}
```

### DELETE request body

```json
{
    "name": "Marcus"
}
```