# 🚛 Smart Waste Collection Route Optimization

A web-based smart waste collection system that uses **Python, Streamlit, MySQL, SQLAlchemy, and OR-Tools** to monitor waste bins and generate optimized collection routes.

The system helps improve waste collection efficiency by considering bin fill levels, collection priority, vehicle capacity, distance, estimated travel time, and fuel consumption.

---

## 🎯 Project Objectives

- Monitor waste bin information and fill levels
- Calculate priority for waste collection
- Manage waste collection vehicles
- Generate optimized collection routes
- Reduce unnecessary travel distance
- Estimate travel time and fuel consumption
- Maintain collection history
- Provide analytics and visual insights

---

## ✨ Features

### 🗑️ Bin Management
- Add and manage waste bins
- Store bin location, capacity, waste type, and fill level
- Search and filter bins
- Track bin status

### 🚛 Vehicle Management
- Add and manage collection vehicles
- Store vehicle capacity and fuel efficiency
- Track vehicle availability
- Assign vehicles for route planning

### 🧠 Route Optimization
- Calculates bin collection priority
- Uses **Google OR-Tools** for Vehicle Routing Problem (VRP) optimization
- Considers vehicle capacity
- Generates optimized routes
- Calculates:
  - Total distance
  - Estimated travel time
  - Estimated fuel consumption
  - Total waste collected

### 🗺️ Interactive Route Map
- Displays the optimized route on an interactive map
- Shows the depot and collection bins
- Uses **OpenStreetMap**

### 📊 Analytics
- Total number of bins
- Estimated waste
- Average fill level
- High-priority bins
- Waste type distribution
- Bin status distribution
- Detailed bin data

### 📜 Collection History
- Record completed waste collections
- Store waste collected
- Record fill level before collection
- Store collection notes
- Maintain collection history

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| MySQL | Database |
| SQLAlchemy | ORM and database connectivity |
| PyMySQL | MySQL database driver |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Plotly | Data visualization |
| Folium | Interactive maps |
| Streamlit-Folium | Folium integration with Streamlit |
| Google OR-Tools | Route optimization |
| Python-dotenv | Environment variable management |

---

## 🧠 Route Optimization

The system models waste collection as a **Vehicle Routing Problem (VRP)**.

The optimization considers:

- Depot location
- Waste bin locations
- Estimated waste quantity
- Vehicle capacities
- Distance between locations

The system uses **Google OR-Tools** to determine an efficient route for the available collection vehicles.

### Priority Calculation

Bin priority is calculated using:

```text
Priority Score =
(Fill Level × 0.7) + (Collection Delay Score × 0.3)