# server.py - Quantum Key Distribution Server
import socket
import threading
import random
import json
from bb84_protocol import BB84Protocol

HOST = '127.0.0.1'
PORT = 65432

class BB84Server:
    def __init__(self, key_length=100):
        self.key_length = key_length
    
    def handle_client(self, conn, addr):
        print(f"[CONNECTED] {addr} connected.")
        
        try:
            # Initialize BB84 protocol
            bb84 = BB84Protocol(key_length=self.key_length)
            
            # Step 1: Alice (Server) prepares qubits
            print("[SERVER] Preparing qubits...")
            alice_bits, alice_bases = bb84.alice_prepare_qubits()
            
            # Step 2: Send qubit information to Bob (Client)
            qubit_data = {
                'alice_bits': alice_bits,
                'alice_bases': alice_bases
            }
            conn.sendall(json.dumps(qubit_data).encode())
            print("[SERVER] Sent qubit data to client")
            
            # Step 3: Receive Bob's measurement bases
            data = conn.recv(4096).decode()
            bob_data = json.loads(data)
            bob_bases = bob_data['bob_bases']
            print(f"[SERVER] Received Bob's bases: {bob_bases[:10]}...")
            
            # Step 4: Simulate Bob's measurements locally
            bb84.bob_bases = bob_bases
            bb84.bob_bits = []
            
            for i in range(self.key_length):
                if alice_bases[i] == bob_bases[i]:
                    bb84.bob_bits.append(alice_bits[i])
                else:
                    bb84.bob_bits.append(random.randint(0, 1))
            
            # Step 5: Sift keys
            sifted_alice_key, sifted_bob_key = bb84.sift_keys()
            
            # Step 6: Error estimation and final key generation
            final_alice_key, final_bob_key, final_qber = bb84.generate_final_key()
            
            # Step 7: Send final key confirmation to Bob
            if final_alice_key:
                response = {
                    'status': 'SUCCESS',
                    'final_key': final_bob_key,
                    'qber': final_qber,
                    'key_length': len(final_bob_key)
                }
                print(f"[SUCCESS] Secure key established! QBER: {final_qber:.3f}, Key length: {len(final_alice_key)}")
            else:
                response = {
                    'status': 'REJECTED',
                    'reason': f'QBER exceeds security threshold',
                    'qber': final_qber
                }
                print(f"[REJECTED] Key exchange failed! QBER: {final_qber:.3f}")
            
            conn.sendall(json.dumps(response).encode())
            
        except Exception as e:
            print(f"[ERROR] Connection with {addr} failed: {e}")
            error_response = {'status': 'ERROR', 'message': str(e)}
            conn.sendall(json.dumps(error_response).encode())
        finally:
            conn.close()
            print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    server = BB84Server(key_length=50)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[LISTENING] BB84 Quantum Key Server running on {HOST}:{PORT}")
        print("[INFO] Waiting for clients to establish secure quantum keys...")
        
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=server.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()