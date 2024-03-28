# Django Cargo and Vehicle Management System
Welcome to the Django Cargo and Vehicle Management System! This application helps you manage cargo shipments and vehicles for efficient logistics operations.

### Features
- Cargo Management: Create, update, and delete cargo shipments.
- Vehicle Management: Track vehicles and their current locations.
- Geographical Information: Store location details including city, state, zip code, latitude, and longitude.
- Validation: Ensure data integrity with validators for cargo weight, vehicle carrying capacity, and unique vehicle numbers.

### Prerequisites

- Python 3.11
- Django and Django REST framework
- Postgresql
- Celery
- Redis

### Installation

#### Start project using docker-compose
1. The first thing to do is to clone the repository:
    ```bash
    git clone https://github.com/marik177/django-cargo-vehicle.git
   ```
2. Using the Dockerfile and docker-compose.yaml run the project:
   ```bash
   docker-compose up --build
   ```
3. In new terminal window run command:
   ````bash
   docker-compose exec cargo sh
   ````
4. Imports uszips.csv data into the PostgreSQL database:
   ````bash
   python manage.py import_uszips cargo/data/uszips.csv
   ````
5. Populates the database with initial vehicle entries:
   ```bash
   python manage.py add_vehicles
   ```
   


### Usage
You could acceess project documentation http://localhost:8000/docs/.

### API Endpoints

#### Get All Cargos
- **URL:** `/api/cargo/`
- **Method:** GET
- **Description:** Retrieves a list of all cargos in the system.
- **Parameters:** None
- **Responses:**
  - 200 OK: List of cargos retrieved successfully.
##### Filter Cargos by Weight:

- **URL:** `/api/cargo/`
- **Method:** GET
- **Query Parameter:** `weight_min or weight_max`
- **Description:** Filters cargos by weight, returning only those with a weight greater than or equal to the specified value.
- **Examples:**
  - `/api/cargo/?weight_min=200`
  - `/api/cargo/?weight_max=500`
  - `/api/cargo/?weight_min=200&weight_max=500`

##### Get Miles of Nearest Vehicles to Cargo:

- **URL:** `/api/cargo/`
- **Method:** GET
- **Query Parameter:** `max_distance_miles`
- **Description:** Retrieves the miles of nearest vehicles to each cargo in the system within the specified distance.
- **Example:** `/api/cargo/?max_distance_miles=100`

#### Create Cargo
- **URL:** `/api/cargo/`
- **Method:** POST
- **Description:** Creates a new cargo shipment.
- **Parameters:** JSON object with cargo details (pick_up, delivery, weight, description).
- **Responses:**
  - 201 Created: Cargo created successfully.

#### Retrieve Cargo
- **URL:** `/api/cargo/{id}/`
- **Method:** GET
- **Description:** Retrieves details of a specific cargo.
- **Parameters:** Cargo ID (integer) in the URL path.
- **Responses:**
  - 200 OK: Cargo details retrieved successfully.

#### Update Cargo
- **URL:** `/api/cargo/{id}/`
- **Method:** PUT or PATCH
- **Description:** Updates details of a specific cargo.
- **Parameters:** Cargo ID (integer) in the URL path, JSON object with updated cargo details.
- **Responses:**
  - 200 OK: Cargo updated successfully.

#### Delete Cargo
- **URL:** `/api/cargo/{id}/`
- **Method:** DELETE
- **Description:** Deletes a specific cargo.
- **Parameters:** Cargo ID (integer) in the URL path.
- **Responses:**
  - 204 No Content: Cargo deleted successfully.

#### Background Tasks

##### Automatic Update of Vehicle Locations

- **Task:** This task automatically updates the locations of all vehicles every 3 minutes.
- **Implementation:** Implemented using Celery Beat scheduler.
- **Description:** The location of each vehicle changes to another random one every 3 minutes.





