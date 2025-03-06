# Hackerrank 
## Date - 4/2/2025
## By Brian Mwangi, Antony Wambugu and Anne Muriuki
### Project Overview
The backend for the Hackerrank  serves as the core API and database layer that powers the assessment platform. It manages user authentication, assessments, submissions, and performance tracking while integrating with third-party services for code execution.

## Features
### For Technical Mentors (T.M.):
* Create & manage assessments (MCQs, subjective, and coding challenges)
* Publish assessments and send invitations to students
* View sorted student performance based on scores
* Review student answers and provide feedback
* Set a time limit for test auto-submission
* Release grades

### For Students:
* Log in and access assigned assessments
* Accept invitations and receive real-time notifications
* Monitor countdown timer for active tests
* Take trial assessments before the actual test
* Submit coding solutions with BDD, pseudocode, and code
* Receive feedback from mentors

## Technologies Used
* Backend: Python with Flask
* Database: PostgreSQL
* Authentication: Firebase Authentication, JWT & Google OAuth
* API Integration: Piston API 
* ORM: SQLAlchemy

## Installation & Setup
To set up the backend locally, follow these steps:

* Clone the repository*
   git clone https://github.com/mwangi-student/HackerRank-Backend
   
* Create and activate a virtual environment using Pipenv
   pipenv install 
   pipenv shell
   
* Run database migrations
   flask db upgrade

* Start the backend server
   flask run --debug

   The API will be available at `http://localhost:5000`.

## Challenges faced
* Challenge : Implementing Codewars API

* Solution : Created a structured dataset that mimics API responses. This allowed us to test functionality without external servers by using a function to simulate API requests.

## Future Plans
* Scalability Improvements: Optimize API response times and prepare for higher traffic.
* Expand Assessment Types: Add more interactive and diverse assessment types.





