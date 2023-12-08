from flask import Flask, request, jsonify
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

class LotrePlanet:
    def __init__(self):
        self.alien = ['Jupiter', 'Saturn', 'Uranus', 'Neptune']
        self.astronaut = ['Mercury', 'Venus', 'Earth', 'Mars']
        self.max_planets = 6
        self.bonus_multiplier = 5
        self.astronaut_chance = 0.09
        self.alien_chance = 0.05
        self.alien_bonus = {'Jupiter': 45, 'Saturn': 25, 'Uranus': 15, 'Neptune': 10}
        self.astronaut_bonus = 5

    def lotre(self, chosen_planets):
        total_bonus = 0
        hasil = 0
        
        if len(chosen_planets) == 0:
            return "Anda belum memilih planet untuk melakukan lotre."
        
        # Membuat daftar nilai yang tidak valid
        invalid_values = [planet for planet, value in chosen_planets.items() if not str(value).isdigit() or int(value) <= -1]
        chosen_planets = {planet: value for planet, value in chosen_planets.items() if int(value) != 0}

        # Validasi jumlah planet yang dipilih
        if len(chosen_planets) > 6 or invalid_values:
            if len(chosen_planets) > 6:
                return "Jumlah planet tidak boleh lebih dari 6."
            if invalid_values:
                return f"Nilai tidak valid pada planet: {', '.join(invalid_values)}"
        else:
            pass

        result = random.choice(self.astronaut + self.alien)

        if (result in self.astronaut and random.random() < self.astronaut_chance) and result in chosen_planets:
            astronaut_bonus = sum(int(value) for key, value in chosen_planets.items() if key in self.astronaut)
            return jsonify({
                "out": "Astronaut",
                "bonus": astronaut_bonus * self.astronaut_bonus
            }), 200

        if (result in self.alien and random.random() < self.alien_chance) and result in chosen_planets:
            total_bonus = 0
            for planet, taruhan in chosen_planets.items():
                if planet in self.astronaut:
                    total_bonus += int(taruhan) * self.astronaut_bonus
                elif planet in self.alien:
                    total_bonus += int(taruhan) * self.alien_bonus[planet]
            return jsonify({
                "out": "Alien",
                "bonus": total_bonus
            }), 200

        if result in chosen_planets:
            if result in self.astronaut:
                hasil = int(chosen_planets[result]) * self.astronaut_bonus
                return jsonify({
                    "out": result,
                    "bonus": hasil
                }), 200
            else:
                hasil = int(chosen_planets[result]) * self.alien_bonus[result]
                return jsonify({
                    "out": result,
                    "bonus": hasil
                }), 200

        if total_bonus == 0:
            return jsonify({
                "out": result,
                "bonus": 0
            }), 200
        else:
            return jsonify({
                "out": result,
                "bonus": total_bonus
            }), 200

lotre = LotrePlanet()

@app.route('/galaxy', methods=['POST'])
def lotre_handler():
    data = request.get_json()
    result = lotre.lotre(data)
    return result

if __name__ == '__main__':
    app.run(debug=True)
