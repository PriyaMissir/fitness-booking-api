# fitness-booking-api


A Simple Booking Api built with FastApi and SQLAlchemy that allows users to view available fitness classes, book a slot, and view bookings using email.


---- Created three Api endpoints to acheive this.
----- http://127.0.0.1:8000/classes is used to get all the available classes and available slots
----- http://127.0.0.1:8000/book is used to book the classes .
---- http://127.0.0.1:8000/bookings?email=priya12@example.com is used to view the bookings done by the user.


#### SET Up Instructions


## 1. Clone the Repository
git clone https://github.com/your-username/fitness-booking-api.git
cd fitness-booking-api

### 2. Create and Activate a Virtual Environment
# For Linux/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate

### 3. Install Dependencies
pip install fastapi uvicorn sqlalchemy pydantic


### 4. Run the FastAPI Server
uvicorn main:app --reload

### 5 Use postman or fastapi Swagger UI
to view the Api docs
