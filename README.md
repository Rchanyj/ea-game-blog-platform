# Game Review Platform
A simple blog platform for users to post game reviews and comments on. _*TekSystems/EA interview assignment._

## MVP
- Only the back-end API portion will be available (as per the requirements), with the following MVP features:
    1. Blog post loading
        - single post
        - list of posts
    2. Blog post creation
    3. Comment creation
    
## Assumptions
- Field data sent from the front end will be in JSON format
- Data taken by end points are assumed to be in the form sent by the front end
- For simplicity, all ids for the MVP will be integers of specific digit lengths. Features like encryption and the use of UUIDs will be in the Future Wish List :)

## Instructions on running the API locally:
1. Clone the repo and (if pipenv is not available) run `pip install pipenv`
2. Run `pipenv install`
3. Run `python main.py` to start the service
4. Run `pytest` with the service running to run all tests
5. Since there is no front end currently available, the API's functionalities can be tested in GUI form on SwaggerUI: http://petstore.swagger.io/ (currently using `http` scheme for MVP). Use `http://{localhost}:8000/swagger` to get the UI. 

## Future wish list:
- Deploy service
- Improve existing error handling and implement error handling for more edge cases (e.g. missing/erroneous request params)
- Improve tests (test error handling, set up TestContext suite for requests, etc.)
- Implement a front end UI
- Implement post editing
- Implement text formatting and customization when creating blog posts
- Implement the ability to add images to blog posts
- Implement user registration
- Implement user account features
- Implement security features
- Implement a likes/claps/support button feature
- Implement a sharing feature that allows reader to link or share blogs on social media