# IoT-Based Smart Parking System with FastAPI Integration

This project is a **team-based IoT system** designed to monitor parking occupancy and control vehicle access in real time.

The system not only tracks parking availability but also **actively prevents congestion** by controlling a servo motor barrier when maximum capacity is reached.

---

## Team Contribution

This project was developed as a group project.  
My contributions focused on:

- Processing sensor data  
- Designing and implementing the FastAPI backend  
- Managing data flow between system components  
- Contributing to the real-time monitoring interface  

---

## System Features

- Real-time parking occupancy detection  
- Automatic barrier control using servo motor  
- FastAPI-based backend for data handling  
- Low-latency monitoring interface  
- Cost-effective IoT integration  

---

## Technologies Used

- Python  
- FastAPI  
- Microcontroller (Arduino / similar)  
- IR Sensors  
- HTML/CSS (for dashboard)  

---

## System Architecture

<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/25584296-da5c-4924-a845-52bdfce005ab" />


---

## How to Run

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
