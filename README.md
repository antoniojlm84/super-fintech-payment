# SuperPayment

SuperPayment is a scalable payment processing platform designed to help online merchants increase conversion rates through instant voucher payments. This repository contains the source code for the backend (Django), frontend (Next.js), and widget (Vanilla JS).

## 🚀 Getting Started

### Prerequisites

*   [Git](https://git-scm.com/downloads) - To clone the repository.
*   [Node.js](https://nodejs.org/) (v18+ recommended) - For local frontend development and intellisense.
*   [Make](https://www.gnu.org/software/make/) (Optional) - To run the simplified commands in the Makefile.
*   [Docker](https://www.docker.com/products/docker-desktop) - To run the containerized application.
*   [Docker Compose](https://docs.docker.com/compose/install/) - To orchestrate the services.

### Installation & Running

The project is containerized for easy setup.

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd superpayment
    ```

2.  **Start the application**:
    We use a `Makefile` for convenience.
    ```bash
    make up
    ```
    Alternatively:
    ```bash
    docker-compose up -d
    ```

3.  **Run Migrations**:
    Initialize the database:
    ```bash
    make migrate
    ```

4.  **Create Superuser**:
    ```bash
    make superuser
    ```

### Access Points

| Service | URL | Description |
| :--- | :--- | :--- |
| **Frontend** | [http://localhost:3000](http://localhost:3000) | Next.js Backoffice Dashboard |
| **Backend API** | [http://localhost:8000](http://localhost:8000) | Django API Root |
| **Widget Demo** | [http://localhost:8080](http://localhost:8080) | Static Widget Hosting |
| **Database** | `localhost:5432` | PostgreSQL (User: `postgres`, Pass: `postgres`) |

### Useful Commands

*   `make logs`: View server logs.
*   `make backend-shell`: Access the backend container shell.
*   `make down`: Stop all containers.

---

## 📚 Documentation

Detailed documentation for the project structure, business logic, and architecture can be found in the `documentation/` folder.

*   **[Business Scaling Plan](documentation/business_scaling_plan.md)**
    *   Comprehensive strategy for scaling the business from local development to €10M MRR.
*   **[Presentation](documentation/business_scaling_presentation.md)**
    *   Visual slide deck summarizing the scaling strategy and architecture.
*   **[Database Schema](documentation/database_schema.md)**
    *   Entity Relationship Diagram (ERD) and description of the data model.
*   **[Payment Flow](documentation/payment_flow.md)**
    *   Sequence diagrams explaining the payment processing lifecycle.
