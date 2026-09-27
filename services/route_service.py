from sqlalchemy.orm import Session

from database.connection import engine
from database.models import Bin, Vehicle

from Optimization.priority import calculate_priority
from Optimization.distance import calculate_distance
from Optimization.vrp_solver import create_route


def get_priority_bins():
    """
    Get active bins from the database
    and calculate their priority.
    """

    with Session(engine) as session:

        bins = (
            session.query(Bin)
            .filter(Bin.status == "Active")
            .all()
        )

        bin_data = []

        for bin_item in bins:

            priority = calculate_priority(
                bin_item.fill_level,
                bin_item.last_collected
            )

            bin_data.append({
                "bin_id": bin_item.bin_id,
                "bin_code": bin_item.bin_code,
                "location_name": bin_item.location_name,
                "latitude": float(bin_item.latitude),
                "longitude": float(bin_item.longitude),
                "capacity_kg": float(bin_item.capacity_kg),
                "fill_level": float(bin_item.fill_level),
                "priority": priority
            })

        bin_data.sort(
            key=lambda x: x["priority"],
            reverse=True
        )

        return bin_data


def get_available_vehicles():
    """
    Get vehicles that are not under maintenance.
    """

    with Session(engine) as session:

        vehicles = (
            session.query(Vehicle)
            .filter(Vehicle.status != "Maintenance")
            .all()
        )

        return [
            {
                "vehicle_id": vehicle.vehicle_id,
                "vehicle_number": vehicle.vehicle_number,
                "capacity_kg": float(vehicle.capacity_kg),
                "fuel_efficiency": float(
                    vehicle.fuel_efficiency or 0
                ),
                "driver_name": vehicle.driver_name
            }
            for vehicle in vehicles
        ]


def build_distance_matrix(locations):
    """
    Create a distance matrix for all locations.
    """

    matrix = []

    for location_a in locations:

        row = []

        for location_b in locations:

            distance = calculate_distance(
                location_a["latitude"],
                location_a["longitude"],
                location_b["latitude"],
                location_b["longitude"]
            )

            row.append(distance)

        matrix.append(row)

    return matrix


def calculate_route_distance(route, distance_matrix):
    """
    Calculate total route distance in kilometers.
    """

    total_distance = 0

    for i in range(len(route) - 1):

        from_location = route[i]
        to_location = route[i + 1]

        total_distance += distance_matrix[
            from_location
        ][
            to_location
        ]

    return round(total_distance, 2)


def optimize_routes():
    """
    Create optimized routes using actual database
    bins and vehicles.
    """

    bins = get_priority_bins()
    vehicles = get_available_vehicles()

    if not bins:
        return None

    if not vehicles:
        return None

    # Temporary depot:
    # first bin location
    depot = {
        "bin_id": 0,
        "bin_code": "DEPOT",
        "location_name": "Vadodara Institute of Engineering",
        "latitude": 22.407221,
        "longitude": 73.307012
    }

    locations = [depot] + bins

    # Distance matrix
    distance_matrix = build_distance_matrix(locations)

    # Waste demand
    demands = [0]

    for bin_item in bins:

        waste_amount = (
            bin_item["capacity_kg"]
            * bin_item["fill_level"]
            / 100
        )

        demands.append(
            int(waste_amount)
        )

    # Vehicle capacities
    vehicle_capacities = [
        int(vehicle["capacity_kg"])
        for vehicle in vehicles
    ]

    # Run OR-Tools
    routes = create_route(
        distance_matrix,
        demands,
        vehicle_capacities
    )

    if routes is None:
        return None

    route_results = []

    for vehicle_index, route in enumerate(routes):

        # Ignore unused vehicles
        if len(route) <= 2:
            continue

        vehicle = vehicles[vehicle_index]

        route_bins = []

        total_waste = 0

        for position in route:

            if position == 0:
                route_bins.append(depot)
            else:

                bin_item = bins[position - 1]

                route_bins.append(bin_item)

                waste_amount = (
                    bin_item["capacity_kg"]
                    * bin_item["fill_level"]
                    / 100
                )

                total_waste += waste_amount

        total_distance = calculate_route_distance(
            route,
            distance_matrix
        )

        # Assume average speed of 30 km/h
        estimated_time = (
            total_distance / 30
        ) * 60

        # Fuel consumption
        if vehicle["fuel_efficiency"] > 0:
            estimated_fuel = (
                total_distance
                / vehicle["fuel_efficiency"]
            )
        else:
            estimated_fuel = 0

        route_results.append({
            "vehicle_id": vehicle["vehicle_id"],
            "vehicle_number": vehicle["vehicle_number"],
            "driver_name": vehicle["driver_name"],
            "route": route_bins,
            "total_distance_km": round(
                total_distance, 2
            ),
            "estimated_time_min": round(
                estimated_time, 2
            ),
            "estimated_fuel_l": round(
                estimated_fuel, 2
            ),
            "total_waste_kg": round(
                total_waste, 2
            )
        })

    return route_results