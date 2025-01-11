import random
from flask import Flask, request, jsonify, render_template
from collections import defaultdict
import heapq

class SocialNetwork:
    def __init__(self):
        self.network = {}

    def add_user(self, user):
        if user not in self.network:
            self.network[user] = set()
            return f"User '{user}' added to the network."
        else:
            return f"User '{user}' already exists in the network."

    def connect_users(self, user1, user2):
        if user1 in self.network and user2 in self.network:
            self.network[user1].add(user2)
            self.network[user2].add(user1)
            return f"'{user1}' and '{user2}' are now connected."
        else:
            return "One or both users do not exist in the network."

    def remove_user(self, user):
        if user in self.network:
            for friend in self.network[user]:
                self.network[friend].remove(user)
            del self.network[user]
            return f"User '{user}' removed from the network."
        else:
            return f"User '{user}' does not exist in the network."

    def suggest_friends(self, user):
        if user not in self.network:
            return f"User '{user}' does not exist in the network."

        direct_friends = self.network[user]
        suggestions = set()

        # For each direct friend
        for friend in direct_friends:
            # Get their friends (friends of friends)
            friends_of_friends = self.network[friend]
            # Add them to suggestions
            suggestions.update(friends_of_friends)

        # Remove the user themselves and their direct friends from suggestions
        suggestions.discard(user)
        suggestions -= direct_friends

        # Return the list of suggestions with additional information
        if suggestions:
            result = {
                "user": user,
                "direct_friends": list(direct_friends),
                "suggested_friends": list(suggestions)
            }
            return result
        else:
            return {
                "user": user,
                "direct_friends": list(direct_friends),
                "suggested_friends": []
            }

    def view_network(self):
        return self.network

    def remove_connection(self, user1, user2):
        if user1 in self.network and user2 in self.network:
            if user2 in self.network[user1]:
                self.network[user1].remove(user2)
                self.network[user2].remove(user1)
                return f"Connection between '{user1}' and '{user2}' removed."
            else:
                return f"'{user1}' and '{user2}' are not connected."
        else:
            return "One or both users do not exist in the network."

    def find_shortest_path(self, start_user, end_user):
        if start_user not in self.network or end_user not in self.network:
            return {
                "error": "One or both users do not exist in the network",
                "path": [],
                "distance": -1
            }

        # Initialize distances and predecessors
        distances = {user: float('infinity') for user in self.network}
        distances[start_user] = 0
        predecessors = {user: None for user in self.network}
        
        # Priority queue to store (distance, node)
        pq = [(0, start_user)]
        visited = set()

        while pq:
            current_distance, current_user = heapq.heappop(pq)

            if current_user in visited:
                continue

            visited.add(current_user)

            if current_user == end_user:
                break

            # Check all neighbors (friends) of current user
            for neighbor in self.network[current_user]:
                distance = current_distance + 1  # Each edge has weight 1

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_user
                    heapq.heappush(pq, (distance, neighbor))

        # Reconstruct path
        if distances[end_user] == float('infinity'):
            return {
                "error": "No path exists between these users",
                "path": [],
                "distance": -1
            }

        path = []
        current = end_user
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()

        return {
            "path": path,
            "distance": distances[end_user],
            "error": None
        }

# Generate a large graph with Indian names as nodes
nodes = [
    "Ayaan", "Ishaan", "Maya", "Riya", "Dev", "Sanya", "Tanya", "Yash", "Kiran", "Mehul"
]


# Initialize the social network
large_social_network = SocialNetwork()

# Add all names as nodes
for name in nodes:
    large_social_network.add_user(name)

# Manually connect nodes to create the graph
connections =[
    ("Ayaan", "Ishaan"), ("Ayaan", "Dev"), ("Ishaan", "Maya"),
    ("Ishaan", "Riya"), ("Maya", "Tanya"), ("Riya", "Dev"),
    ("Dev", "Yash"), ("Sanya", "Kiran"), ("Tanya", "Mehul"),
    ("Yash", "Maya")
]

for user1, user2 in connections:
    large_social_network.connect_users(user1, user2)

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/add_user', methods=['POST'])
def add_user():
    user = request.form['user']
    return jsonify(large_social_network.add_user(user))

@app.route('/connect_users', methods=['POST'])
def connect_users():
    user1 = request.form['user1']
    user2 = request.form['user2']
    return jsonify(large_social_network.connect_users(user1, user2))

@app.route('/remove_user', methods=['POST'])
def remove_user():
    user = request.form['user']
    return jsonify(large_social_network.remove_user(user))

@app.route('/suggest_friends', methods=['POST'])
def suggest_friends():
    user = request.form['user']
    suggestions = large_social_network.suggest_friends(user)
    return jsonify(suggestions)

@app.route('/remove_connection', methods=['POST'])
def remove_connection():
    user1 = request.form['user1']
    user2 = request.form['user2']
    return jsonify(large_social_network.remove_connection(user1, user2))

@app.route('/view_network', methods=['GET'])
def view_network():
    # Convert all sets to lists for JSON serialization
    return jsonify({user: list(friends) for user, friends in large_social_network.network.items()})

@app.route('/find_path', methods=['POST'])
def find_path():
    user1 = request.form['user1']
    user2 = request.form['user2']
    result = large_social_network.find_shortest_path(user1, user2)
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)






















