import socket
import threading
import random
from string import ascii_lowercase, ascii_uppercase

HOST = "0.0.0.0"
PORT = 31337
FLAG = "flag{w0W_1T_is_r3Lly_G00d_WPM}"

texts = [
    "Breakthrough graphene battery achieves record energy density",
    "Global cybersecurity pact signed by leading nations",
    "Scientists map deep-sea volcano ecosystems for the first time",
    "New AI-driven platform predicts crop yields with 95% accuracy",
    "Electric vehicle maker unveils solid-state battery prototype",
    "International treaty bans single-use plastics in oceans",
    "Researchers develop portable detector for waterborne pathogens",
    "Tech consortium demonstrates quantum-secure communication link",
    "Urban vertical farm yields 10x more produce per square meter",
    "AI regulator proposes universal ethics framework for robotics",
    "Solar power plant with built-in storage goes online in Spain",
    "Biotech startup engineers bacteria to recycle electronic waste",
    "Space telescope captures first image of exoplanet’s atmosphere",
    "Breakthrough in carbon capture cuts emissions cost by half",
    "Global health summit endorses mRNA vaccine for malaria",
    "Smartphone app uses AI to diagnose skin conditions instantly",
    "Autonomous cargo ship completes transatlantic voyage",
    "Novel biodegradable polymer wins green chemistry award",
    "Researchers create lab-grown meat at commercial scale",
    "Aviation industry adopts biofuels for short-haul flights",
    "Solar sail mission to Jupiter’s moon launches successfully",
    "AI-powered tutor boosts student performance by 40%",
    "New fusion reactor design reaches net energy gain",
    "Global fintech alliance sets standards for digital currencies",
    "Archaeologists decode ancient inscriptions using machine learning",
    "Groundwater replenishment project restores depleted aquifers",
    "Virtual reality therapy approved for PTSD treatment",
    "Drone swarm plants 10,000 trees in deforested region",
    "Scientists detect rare Earth–like planet in habitable zone",
    "Electric trucking startup secures $200 M in Series B funding",
    "AI model translates sign language in real time",
    "Waste-to-energy plant converts landfill gas into electricity",
    "Next-gen 6G network trials begin in South Korea",
    "Researchers develop self-healing concrete for infrastructure",
    "Global data privacy accord takes effect in 2026",
    "Ocean cleanup initiative removes 90% of surface plastics",
    "Biodegradable electronics prototype debuts at tech fair",
    "AI-driven drug discovery yields new antibiotic candidate",
    "Asteroid sample return mission touches down on Earth",
    "Mobile health clinic uses satellite link for remote diagnostics",
    "Renewable hydrogen project powers industrial complex",
    "Global summit agrees on AI-powered climate modeling standards",
    "Innovative desalination plant uses solar thermal energy",
    "Startup launches wearable sensor for early Parkinson’s detection",
    "Researchers unveil transparent solar windows for buildings",
    "Electric ferry begins zero-emission service in Norway",
    "New algorithm reduces data center energy use by 30%",
    "UN declares moratorium on deep-sea mining activities",
    "AI chatbot passes advanced coding proficiency test",
    "Next-generation prosthetic arm controlled by thought",
    "Microgrid project brings power to remote island community",
    "Scientists create synthetic spider silk stronger than steel",
    "Biotech firm develops universal flu vaccine candidate",
    "Autonomous drone ambulance completes first trial flight",
    "Blockchain consortium launches cross-border payment network",
    "Global conference endorses net-zero aviation roadmap",
    "Researchers design recyclable composite for automotive use",
    "AI detects deforestation hotspots from satellite imagery",
    "New study finds microplastics in rooftop rainwater tanks",
    "Modular nuclear reactor achieves full safety certification",
    "Telemedicine platform expands to underserved rural areas",
    "Solar highway project generates power from road surface",
    "Startup debuts consumer brain-computer interface headset",
    "Scientists restore coral reefs using 3D-printed substrates",
    "Autonomous farming robot plants seeds with millimeter precision",
    "Global agreement sets emissions cap for shipping industry",
    "Innovative magnetic refrigeration promises greener cooling",
    "AI optimizes wind farm layouts for maximum output",
    "Researchers trace COVID-19 origins through wastewater analysis",
    "Space station tests 3D-printed habitats for Moon missions",
    "Electric motorcycle breaks 300 km range barrier",
    "Citywide smart-lighting network cuts energy use by 50%",
    "Biodegradable battery developed from plant waste",
    "AR glasses translate foreign languages on the fly",
    "Global pollinator protection treaty signed by 75 countries",
    "Scientists unveil chip-scale atomic clock with unprecedented accuracy",
    "Electric cargo bike network rolls out in major European cities",
    "AI-powered early-warning system predicts earthquakes",
    "Researchers engineer crops to thrive in saline soils",
    "Startup launches subscription service for home fuel cells",
    "WHO endorses AI triage tool for emergency departments",
    "Breakthrough in neural implant restores sight in trial patients",
    "Tech giant unveils holographic telepresence prototype",
    "Ocean observatory records deep-sea temperature rise for first time",
    "Autonomous waste sorting system boosts recycling rates by 70%",
    "New plastic-eating enzyme patent licensed to major chemical firm",
    "NASA greenlights mission to sample Saturn’s rings",
    "Solar-powered desalination buoy provides freshwater to ships",
    "AI creates original music track indistinguishable from human-made",
    "Researchers demonstrate wireless power transfer over 5 meters",
    "Electric supersonic jet completes first test flight",
    "Global initiative funds clean cooking stoves for 1 million homes",
    "Biotech breakthrough enables on-demand insulin production",
    "AI-driven platform predicts financial market anomalies",
    "Scientists develop edible packaging film from seaweed",
    "Mars rover discovers evidence of ancient microbial life",
    "Startup pilots urban air mobility service with electric VTOL",
    "Quantum computer solves optimization problem in record time",
    "Global treaty bans deep-sea noise pollution from shipping",
    "Researchers employ CRISPR to restore endangered species",
]


def encrypt(text):
    shift = random.randint(1, 25)
    encrypted_text = ""
    for char in text:
        if char in ascii_lowercase:
            encrypted_text += ascii_lowercase[
                (ascii_lowercase.index(char) + shift) % 26
            ]
        elif char in ascii_uppercase:
            encrypted_text += ascii_uppercase[
                (ascii_uppercase.index(char) + shift) % 26
            ]
        else:
            encrypted_text += char
    return encrypted_text


def handle_client(conn, addr):
    with conn:
        count = 0
        random.shuffle(texts)
        conn.sendall(b"Welcome to the broken library!")
        while True:
            text = encrypt(texts[count])
            conn.sendall(f"\n----------------\nRestore the text:\n{text}\n> ".encode())
            input = conn.recv(1024).decode("utf-8").strip()

            if not input:
                break

            if input == texts[count]:
                count += 1
                conn.sendall(f"Correct![{count}/{len(texts)}]\n".encode())

                if count >= len(texts):
                    conn.sendall(f"Congratulations!\nYour flag is: {FLAG}\n".encode())
                    break
            else:
                conn.sendall(b"Wrong!\n")
                break


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = srv.accept()
            print(f"Connection from {addr}")
            threading.Thread(
                target=handle_client, args=(conn, addr), daemon=True
            ).start()


if __name__ == "__main__":
    main()
