# Metadata Management Service

This project is a backend service built using **Django** and **Django REST Framework**
to manage dataset metadata and their associated data elements.

---

## Data Model

### Dataset
Represents a logical dataset.

Fields:
- name (unique)
- description
- created_at

### DataElement
Represents a field inside a dataset.

Fields:
- dataset (ForeignKey)
- name
- data_type (string, integer, float, boolean, date)
- is_required
- created_at

A composite uniqueness constraint ensures that a field name is unique within a dataset.

---

## Key Design Decisions

- RESTful API design
- Class-based views using APIView
- Nested data elements returned with dataset details
- Database-level constraints for data integrity

---

## API Endpoints

| Method | Endpoint | Description |
|------|---------|-------------|
| GET | /api/datasets/ | List all datasets |
| POST | /api/datasets/ | Create dataset |
| GET | /api/datasets/<id>/ | Get dataset by ID |
| PUT | /api/datasets/<id>/ | Update dataset |
| DELETE | /api/datasets/<id>/ | Delete dataset |

---

## How to Run the Application

```bash
python3 -m venv venv
source venv/bin/activate
pip install django djangorestframework
python manage.py migrate
python manage.py runserver
