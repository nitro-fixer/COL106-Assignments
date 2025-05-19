from flight import Flight

class AdjListNode:
    def __init__(self):
        self.flights = []  # Store flights sorted by departure time
        
    def add_flight(self, flight):
        # Insert maintaining sort by departure time
        i = 0
        while i < len(self.flights) and self.flights[i].departure_time < flight.departure_time:
            i += 1
        self.flights.insert(i, flight)

class Planner:
    def __init__(self, flights):
        # Find max city number for array size
        max_city = 1
        for flight in flights:
            max_city = max(max_city, flight.start_city, flight.end_city)
            
        # Initialize adjacency lists
        self.adj_list = [AdjListNode() for _ in range(max_city + 1)]
        
        # Add flights to adjacency lists O(m)
        for flight in flights:
            self.adj_list[flight.start_city].add_flight(flight)
    
    def _find_next_valid_flight(self, city_flights, current_time):
        # Binary search to find first flight departing after current_time
        left, right = 0, len(city_flights) - 1
        result = len(city_flights)
        
        while left <= right:
            mid = (left + right) // 2
            if city_flights[mid].departure_time >= current_time:
                result = mid
                right = mid - 1
            else:
                left = mid + 1
                
        return result
    
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        # Dynamic programming approach tracking minimum flights needed
        if t1 >= t2:
            return []
        INF = float('inf')
        min_flights = [INF] * len(self.adj_list)
        earliest_arrival = [INF] * len(self.adj_list)
        prev_flight = [None] * len(self.adj_list)
        
        min_flights[start_city] = 0
        earliest_arrival[start_city] = t1
        
        # Process cities in order of minimum flights needed
        cities_to_process = [(0, start_city)]  # (num_flights, city)
        processed = [False] * len(self.adj_list)
        
        while cities_to_process:
            num_flights, curr_city = cities_to_process.pop(0)
            
            if processed[curr_city]:
                continue
            processed[curr_city] = True
            
            curr_time = earliest_arrival[curr_city]
            if curr_time > t2:
                continue
                
            city_flights = self.adj_list[curr_city].flights
            start_idx = self._find_next_valid_flight(city_flights, curr_time)
            
            for i in range(start_idx, len(city_flights)):
                flight = city_flights[i]
                if flight.departure_time > t2:
                    break
                    
                next_city = flight.end_city
                next_time = flight.arrival_time + 20  # Connection time
                
                if (num_flights + 1 < min_flights[next_city] or 
                    (num_flights + 1 == min_flights[next_city] and next_time < earliest_arrival[next_city])):
                    min_flights[next_city] = num_flights + 1
                    earliest_arrival[next_city] = next_time
                    prev_flight[next_city] = flight
                    cities_to_process.append((num_flights + 1, next_city))
                    
        # Reconstruct path
        if min_flights[end_city] == INF:
            return []
            
        path = []
        curr_city = end_city
        while curr_city != start_city:
            flight = prev_flight[curr_city]
            path.append(flight)
            curr_city = flight.start_city
            
        return path[::-1]
    
    def cheapest_route(self, start_city, end_city, t1, t2):
        if t1 >= t2:
            return []
        INF = float('inf')
        min_cost = [INF] * len(self.adj_list)
        prev_flight = [None] * len(self.adj_list)
        min_cost[start_city] = 0
        
        # Min heap for Dijkstra's: (cost, time, city)
        heap = [(0, t1, start_city)]
        
        while heap:
            curr_cost, curr_time, curr_city = heap[0]
            heap.pop(0)
            downheap(heap, 0)
            
            if curr_time > t2:
                continue
                
            if curr_city == end_city:
                # Reconstruct path
                path = []
                while curr_city != start_city:
                    flight = prev_flight[curr_city]
                    path.append(flight)
                    curr_city = flight.start_city
                return path[::-1]
            
            city_flights = self.adj_list[curr_city].flights
            start_idx = self._find_next_valid_flight(city_flights, curr_time)
            
            for i in range(start_idx, len(city_flights)):
                flight = city_flights[i]
                if flight.departure_time > t2:
                    break
                    
                next_city = flight.end_city
                next_time = flight.arrival_time + 20
                next_cost = curr_cost + flight.fare
                
                if next_cost < min_cost[next_city]:
                    min_cost[next_city] = next_cost
                    prev_flight[next_city] = flight
                    heap.append((next_cost, next_time, next_city))
                    upheap(heap, len(heap) - 1)
        
        return []
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        if t1 >= t2:
            return []
        INF = float('inf')
        min_flights = [INF] * len(self.adj_list)
        min_cost = [INF] * len(self.adj_list)
        prev_flight = [None] * len(self.adj_list)
        
        min_flights[start_city] = 0
        min_cost[start_city] = 0
        
        # Priority queue: (num_flights, cost, time, city)
        heap = [(0, 0, t1, start_city)]
        
        while heap:
            num_flights, curr_cost, curr_time, curr_city = heap[0]
            heap.pop(0)
            downheap(heap, 0)
            
            if curr_time > t2:
                continue
                
            city_flights = self.adj_list[curr_city].flights
            start_idx = self._find_next_valid_flight(city_flights, curr_time)
            
            for i in range(start_idx, len(city_flights)):
                flight = city_flights[i]
                if flight.departure_time > t2:
                    break
                    
                next_city = flight.end_city
                next_time = flight.arrival_time + 20
                next_cost = curr_cost + flight.fare
                
                if (num_flights + 1 < min_flights[next_city] or
                    (num_flights + 1 == min_flights[next_city] and next_cost < min_cost[next_city])):
                    min_flights[next_city] = num_flights + 1
                    min_cost[next_city] = next_cost
                    prev_flight[next_city] = flight
                    heap.append((num_flights + 1, next_cost, next_time, next_city))
                    upheap(heap, len(heap) - 1)
        
        # Reconstruct path
        if min_flights[end_city] == INF:
            return []
            
        path = []
        curr_city = end_city
        while curr_city != start_city:
            flight = prev_flight[curr_city]
            path.append(flight)
            curr_city = flight.start_city
            
        return path[::-1]

# Helper functions for heap operations
def upheap(heap, idx):
    while idx > 0:
        parent = (idx - 1) // 2
        if heap[parent] <= heap[idx]:
            break
        heap[parent], heap[idx] = heap[idx], heap[parent]
        idx = parent

def downheap(heap, idx):
    while True:
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        
        if left < len(heap) and heap[left] < heap[smallest]:
            smallest = left
        if right < len(heap) and heap[right] < heap[smallest]:
            smallest = right
            
        if smallest == idx:
            break
            
        heap[idx], heap[smallest] = heap[smallest], heap[idx]
        idx = smallest
