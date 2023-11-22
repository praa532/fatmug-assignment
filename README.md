# fatmug-assignment

# Vendor Management System

This project is a Vendor Management System implemented using Django and Django REST Framework. The system handles vendor profiles, tracks purchase orders, and calculates vendor performance metrics.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Backend Logic](#backend-logic)
- [Data Models](#data-models)
- [HTML Pages](#html-pages)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/vendor-management-system.git
    cd vendor-management-system
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser account for administrative access:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

The application should now be accessible at http://localhost:8000/.

## Usage

1. Access the Django admin interface to manage vendors and purchase orders:

    - http://localhost:8000/admin/

## API Endpoints

- **Vendor Management:**
  - `POST /api/vendors/`: Create a new vendor.
  - `GET /api/vendors/`: List all vendors.
  - `GET /api/vendors/{vendor_id}/`: Retrieve a specific vendor's details.
  - `PUT /api/vendors/{vendor_id}/`: Update a vendor's details.
  - `DELETE /api/vendors/{vendor_id}/`: Delete a vendor.

- **Purchase Order Tracking:**
  - `POST /api/purchase_orders/`: Create a purchase order.
  - `GET /api/purchase_orders/`: List all purchase orders with an option to filter by vendor.
  - `GET /api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order.
  - `PUT /api/purchase_orders/{po_id}/`: Update a purchase order.
  - `DELETE /api/purchase_orders/{po_id}/`: Delete a purchase order.

- **Vendor Performance Evaluation:**
  - `GET /api/vendors/{vendor_id}/performance`: Retrieve a vendor's performance metrics.

- **Vendor Acknowledgment:**
  - `POST /api/purchase_orders/{po_id}/acknowledge`: Acknowledge a purchase order and update response time.

## Backend Logic

- **On-Time Delivery Rate:**
  - Calculated each time a PO status changes to 'completed'.
  - Logic: Count the number of completed POs delivered on or before delivery_date and divide by the total number of completed POs for that vendor.

- **Quality Rating Average:**
  - Updated upon the completion of each PO where a quality_rating is provided.
  - Logic: Calculate the average of all quality_rating values for completed POs of the vendor.

- **Average Response Time:**
  - Calculated each time a PO is acknowledged by the vendor.
  - Logic: Compute the time difference between issue_date and acknowledgment_date for each PO, and then find the average of these times for all POs of the vendor.

- **Fulfillment Rate:**
  - Calculated upon any change in PO status.
  - Logic: Divide the number of successfully fulfilled POs (status 'completed' without issues) by the total number of POs issued to the vendor.

## Data Models

1. **Vendor Model:**
   - Fields:
     - name: CharField
     - contact_details: TextField
     - address: TextField
     - vendor_code: CharField
     - on_time_delivery_rate: FloatField
     - quality_rating_avg: FloatField
     - average_response_time: FloatField
     - fulfillment_rate: FloatField

![Alt text](<Screenshot 2023-11-22 174136.png>)

![Alt text](<Screenshot 2023-11-22 174201.png>)

2. **Purchase Order (PO) Model:**
   - Fields:
     - po_number: CharField
     - vendor: ForeignKey to Vendor model
     - order_date: DateTimeField
     - delivery_date: DateTimeField
     - items: JSONField
     - quantity: IntegerField
     - status: CharField
     - quality_rating: FloatField (nullable)
     - issue_date: DateTimeField
     - acknowledgment_date: DateTimeField (nullable)

3. **Historical Performance Model:**
   - Fields:
     - vendor: ForeignKey to Vendor model
     - date: DateTimeField
     - on_time_delivery_rate: FloatField
     - quality_rating_avg: FloatField
     - average_response_time: FloatField
     - fulfillment_rate: FloatField

## Contributing

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add a new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
