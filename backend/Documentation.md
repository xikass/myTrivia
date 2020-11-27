# Introduction

# Getting Started

# Resource Endpoint Library

## GET /categories
- fetches a dictionary of categories, where the key is the category id  and the value is the category name
- Request Arguments : None
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
## GET /questions
- fetches all questions from the data base
- Request Arguments (optional) : URL query argument is page example: /questions?page=2. if not supplied it is defalted to page=1
- Response: The response is a json object containing the following key valye pairs
    1. questions : [Array] the retrieved questions in the specified page. if page is not provided in the URL query argument it is defaulted to 1
    2. total_questions: [integer] the count of ALL questions fitched.