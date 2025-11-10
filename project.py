import heapq

# ---------------------------
# Campus Graph Dataset
# ---------------------------
CAMPUS_GRAPH = {
    'A': {'B': 4, 'C': 2, 'J': 7},
    'B': {'A': 4, 'C': 1, 'D': 5, 'E': 6},
    'C': {'A': 2, 'B': 1, 'D': 8, 'F': 3},
    'D': {'B': 5, 'C': 8, 'E': 2, 'G': 4},
    'E': {'B': 6, 'D': 2, 'F': 5, 'H': 3},
    'F': {'C': 3, 'E': 5, 'G': 2, 'I': 6},
    'G': {'D': 4, 'F': 2, 'H': 5, 'I': 3},
    'H': {'E': 3, 'G': 5, 'I': 4, 'J': 6},
    'I': {'F': 6, 'G': 3, 'H': 4, 'J': 2},
    'J': {'A': 7, 'H': 6, 'I': 2}
}

BASE_FARE = 20  # fare per unit distance

# ---------------------------------------------------
# Algorithm 1: Dijkstra’s Algorithm (Shortest Path)
# ---------------------------------------------------
def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, node = heapq.heappop(pq)
        if d > dist[node]:
            continue
        for neigh, w in graph[node].items():
            new_d = d + w
            if new_d < dist[neigh]:
                dist[neigh] = new_d
                prev[neigh] = node
                heapq.heappush(pq, (new_d, neigh))

    return dist, prev

def shortest_path(graph, start, end):
    dist, prev = dijkstra(graph, start)
    path, current = [], end
    while current:
        path.append(current)
        current = prev[current]
    path.reverse()
    return dist[end], path

# ---------------------------------------------------
# Algorithm 2: Prim’s Algorithm (Minimum Spanning Tree)
# ---------------------------------------------------
def prim_mst(graph, start='A'):
    visited, edges, total = set(), [], 0
    pq = [(0, start, None)]
    while pq:
        w, node, parent = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if parent:
            edges.append((parent, node, w))
            total += w
        for neigh, wt in graph[node].items():
            if neigh not in visited:
                heapq.heappush(pq, (wt, neigh, node))
    return total, edges

# ---------------------------------------------------
# Algorithm 3: Binary Search (case-insensitive)
# ---------------------------------------------------
def binary_search(arr, target):
    """arr is a list of tuples (route_name, distance) sorted by route_name (case-insensitive)."""
    target_upper = target.upper()
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_name = arr[mid][0].upper()
        if mid_name == target_upper:
            return arr[mid]
        elif mid_name < target_upper:
            lo = mid + 1
        else:
            hi = mid - 1
    return None

# ---------------------------------------------------
# Backend Functionalities
# ---------------------------------------------------
def show_optimal_route(pickup, drop):
    if pickup not in CAMPUS_GRAPH or drop not in CAMPUS_GRAPH:
        print("Invalid locations! Try again.")
        return
    dist, path = shortest_path(CAMPUS_GRAPH, pickup, drop)
    fare = dist * BASE_FARE
    print(f"\nOptimal Route: {' → '.join(path)}")
    print(f"Total Distance: {dist} Kilometers")
    print(f"Estimated Fare: ₹{fare}")

def show_campus_map():
    total, edges = prim_mst(CAMPUS_GRAPH)
    print("\nCampus Connectivity (Minimum Spanning Tree):")
    for u, v, w in edges:
        print(f"{u} - {v} (Cost: {w})")
    print(f"Total Connection Cost: {total}")

def search_route():
    # routes must be sorted by route name (case-insensitive) for binary search to work
    routes = [
        ('A-J', 15),
        ('A-C', 2),
        ('B-F', 10),
        ('C-I', 12),
        ('D-H', 8)
    ]
    # Sort by route name case-insensitively
    routes.sort(key=lambda x: x[0].upper())

    target = input("Enter route name to search (e.g., A-J): ").strip()
    if not target:
        print("No route entered.")
        return

    result = binary_search(routes, target)
    if result:
        print(f"Found Route: {result[0]} - Distance: {result[1]}")
    else:
        print("Route not found. Available routes:")
        for r in routes:
            print(f"  {r[0]} - Distance: {r[1]}")

# ---------------------------------------------------
# Main Menu
# ---------------------------------------------------
def main():
    pickup = None
    drop = None
    while True:
        print("\n=== CAMPUS SHUTTLE ROUTE OPTIMIZATION SYSTEM ===")
        print("1. Choose Pickup Location")
        print("2. Choose Drop Location")
        print("3. View Optimal Route & Fare")
        print("4. Show Full Campus Connectivity Map (MST)")
        print("5. Search Route Information")
        print("0. Exit")

        choice = input("Enter choice: ").strip()
        if choice == '1':
            pickup = input("Enter Pickup Location (A-J): ").strip().upper()
        elif choice == '2':
            drop = input("Enter Drop Location (A-J): ").strip().upper()
        elif choice == '3':
            if not pickup or not drop:
                print("Please select both pickup and drop first!")
            else:
                show_optimal_route(pickup, drop)
        elif choice == '4':
            show_campus_map()
        elif choice == '5':
            search_route()
        elif choice == '0':
            print("Exiting system. Thank you for using Campus Shuttle Optimizer!")
            break
        else:
            print("Invalid choice, please try again.")

# ---------------------------------------------------
# Run the System
# ---------------------------------------------------
if __name__ == "__main__":
    main()
