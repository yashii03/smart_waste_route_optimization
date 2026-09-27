from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def create_route(distance_matrix, demands, vehicle_capacities):
    """
    Create optimized routes for multiple waste collection vehicles.

    distance_matrix:
        Distance between every location in km.

    demands:
        Waste amount at each location in kg.

    vehicle_capacities:
        List containing the capacity of each vehicle.
    """

    num_locations = len(distance_matrix)
    num_vehicles = len(vehicle_capacities)

    # Location 0 is the depot
    depot = 0

    manager = pywrapcp.RoutingIndexManager(
        num_locations,
        num_vehicles,
        depot
    )

    routing = pywrapcp.RoutingModel(manager)

    # -------------------------
    # Distance callback
    # -------------------------

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        return int(
            distance_matrix[from_node][to_node] * 1000
        )

    distance_callback_index = routing.RegisterTransitCallback(
        distance_callback
    )

    routing.SetArcCostEvaluatorOfAllVehicles(
        distance_callback_index
    )

    # -------------------------
    # Waste demand callback
    # -------------------------

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)

        return int(demands[from_node])

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback
    )

    # Vehicle capacity constraint
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        vehicle_capacities,
        True,
        "Capacity"
    )

    # -------------------------
    # Search settings
    # -------------------------

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()

    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # -------------------------
    # Solve
    # -------------------------

    solution = routing.SolveWithParameters(
        search_parameters
    )

    if solution is None:
        return None

    # -------------------------
    # Extract routes
    # -------------------------

    routes = []

    for vehicle_id in range(num_vehicles):

        index = routing.Start(vehicle_id)

        vehicle_route = []

        while not routing.IsEnd(index):

            node = manager.IndexToNode(index)

            vehicle_route.append(node)

            index = solution.Value(
                routing.NextVar(index)
            )

        # Add depot at the end
        vehicle_route.append(
            manager.IndexToNode(index)
        )

        routes.append(vehicle_route)

    return routes