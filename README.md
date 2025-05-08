# 🍽️ Restaurant Management System

This project is a restaurant management system based on a microservices architecture, developed as part of the Distributed Systems course. It simulates the full workflow of a restaurant — from order creation to kitchen processing and table payments — in a modular and efficient way.

## 📦 Project Structure

- `/site` — Web interface for user interaction.
- `/api_gateway` — Entry point for the frontend to access backend services.
- `/orders` — Microservice responsible for creating and managing orders.
- `/kitchen` — Microservice that simulates order preparation in the kitchen.
- `/payments` — Microservice that manages table payments.

## ⚙️ Technologies Used

- **Python + Flask** — For backend microservices.
- **HTML/CSS/JavaScript** — For a responsive frontend interface.
- **JSON** — For local data persistence.
- **CORS + Fetch API** — For asynchronous communication between frontend and backend.

## 💡 Features

- Create orders per table with a list of items.
- Kitchen simulation with automatic order status updates.
- Payment system per table with confirmation and automatic cleanup.
- Communication between services through HTTP.
- Lightweight, reactive, and user-friendly interface.

## 📁 Data Persistence

All data is stored locally in `.json` files, ensuring durability between restarts without the need for an external database.

## 🧪 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/TubiasComU/1706619_ei_sd_2024_25
   cd 1706619_ei_sd_2024_25
   
2. Start start.py
   ```bash
   python start.py

3. Open Website
   ```bash
   cd site
   start index.html

