# Introduction

# Getting Started

# Resource Endpoint Library

## GET /categories
- fetches a dictionary of questions' categories, where the key is the category id  and the value is the category name
- Request body : None
- Response sample

```json
{
    "categories" : 
    {
        "1" : "Sport",
        "2" : "Geography",
        "3" : "Science"

    },
    "success" : true
}
```