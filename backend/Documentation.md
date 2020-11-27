# Introduction

# Getting Started

# Resource Endpoint Library

## GET /categories
fetches a dictionary of categories, where the key is the category id  and the value is the category name
### Request Arguments : 
    None
### Response
response is a JSOn object containing two keys
1. categories : a JSON object of all categories
2. success : [boolean] true if the successful

sample response
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
fetches all questions from the database
### Request Arguments _optional_ : 
URL query argument is __page__\
for instance: ```/questions?page=2```. if not supplied it is defaulted to page=1
### Response: 
The response is a json object containing the following key valye pairs.
1. questions : [Array] the retrieved 10 questions in the specified page. if page is not provided in the URL query argument it is defaulted to 1. Each element in the array is a JSON object represents a question
2. total_questions: [integer] the count of ALL questions fitched.
3. categories: [JSON object] a key value paired json object of categories 
4. current_category: [null]
5. success : [boolean] true if the successful
Sample Response
```json
{
    "success" : true,
    "questions" : [
        {
            "id" : 1,
            "question" : "is it a smaple question?",
            "answer" : "this is the answer",
            "category" : 2,
            "difficulty" : 3
        }, 
        {
            "id" : 2,
            "question" : "is another it a smaple question?",
            "answer" : "this another is the answer",
            "category" : 3,
            "difficulty" : 2
        },{...}],
    "total_questions" : 10,
    "categories" : {},
    "current_category": null
}

```
### Errors
__404__:  in case _page_ URL argument is beyound the maximum page number
