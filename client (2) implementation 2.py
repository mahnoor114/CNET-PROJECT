# client.py - Quantum Key Distribution Client
import socket
import random
import json

HOST = '127.0.0.1'
PORT = 65432

class BB84Client:
    def __init__(self, key_length=100):
        self.key_length = key_length
    
    def connect_to_server(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                print("[CLIENT] Connected to quantum key server")
                
                # Step 1: Receive qubit information from Alice (Server)
                data = s.recv(4096).decode()
                qubit_data = json.loads(data)
                alice_bits = qubit_data['alice_bits']
                alice_bases = qubit_data['alice_bases']
                print(f"[CLIENT] Received {len(alice_bits)} qubits from server")
                
                # Step 2: Bob (Client) chooses random measurement bases
                bob_bases = [random.randint(0, 1) for _ in range(self.key_length)]
                print(f"[CLIENT] Bob's bases sample: {bob_bases[:10]}...")
                
                # Step 3: Send Bob's bases back to Alice
                bases_data = {'bob_bases': bob_bases}
                s.sendall(json.dumps(bases_data).encode())
                print("[CLIENT] Sent measurement bases to server")
                
                # Step 4: Simulate Bob's measurement results
                bob_bits = []
                for i in range(self.key_length):
                    if alice_bases[i] == bob_bases[i]:
                        bob_bits.append(alice_bits[i])
                    else:
                        bob_bits.append(random.randint(0, 1))
                
                print(f"[CLIENT] Bob's measured bits sample: {bob_bits[:10]}...")
                
                # Step 5: Receive final key from server
                response_data = s.recv(4096).decode()
                response = json.loads(response_data)
                
                if response['status'] == 'SUCCESS':
                    final_key = response['final_key']
                    qber = response['qber']
                    key_length = response['key_length']
                    print(f"🎉 [SUCCESS] Quantum key exchange completed!")
                    print(f"   Key length: {key_length} bits")
                    print(f"   QBER: {qber:.3f}")
                    print(f"   Final key sample: {final_key[:16]}...")
                    
                    # Demonstrate usage for encryption
                    self.demo_encryption_usage(final_key)
                    
                elif response['status'] == 'REJECTED':
                    print(f"🚨 [REJECTED] {response['reason']}")
                    print("   Eavesdropper detected or channel too noisy!")
                    
                else:
                    print(f"❌ [ERROR] {response.get('message', 'Unknown error')}")
                    
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
    
    def demo_encryption_usage(self, quantum_key):
        """Demonstrate how the quantum key would be used for encryption"""
        print("\n🔐 ENCRYPTION DEMONSTRATION:")
        
        # Convert quantum key to bytes for AES encryption
        key_bits = ''.join(map(str, quantum_key))
        
        # Pad to multiple of 8 bits
        while len(key_bits) % 8 != 0:
            key_bits += '0'
        
        # Convert to bytes (for AES key)
        key_bytes = bytearray()
        for i in range(0, len(key_bits), 8):
            byte_str = key_bits[i:i+8]
            key_bytes.append(int(byte_str, 2))
        
        print(f"   Quantum-derived key (hex): {key_bytes.hex()[:32]}...")
        print(f"   Can be used with AES-{len(key_bytes)*8} encryption")
        print("   Secure socket communication ready! ✅")

def start_client():
    client = BB84Client(key_length=50)
    client.connect_to_server()

if __name__ == "__main__":
    start_client()