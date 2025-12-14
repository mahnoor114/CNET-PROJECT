# bb84_protocol.py - Complete BB84 Protocol Implementation
import numpy as np
import matplotlib.pyplot as plt
import random
import hashlib

print("Setting up quantum simulator...")

# QISKIT 2.2.3 COMPATIBLE IMPORTS
QISKIT_AVAILABLE = False
Aer = None
QuantumCircuit = None

try:
    from qiskit import QuantumCircuit
    from qiskit_aer import Aer
    from qiskit_aer import AerSimulator
    
    # Test if it works
    backend = Aer.get_backend('qasm_simulator')
    
    print("✅ Qiskit 2.2.3 successfully loaded!")
    QISKIT_AVAILABLE = True
    
except Exception as e:
    print(f"❌ Qiskit not available: {e}")
    print("Using pure Python simulation mode")
    QISKIT_AVAILABLE = False

class BB84Protocol:
    def __init__(self, key_length=100):
        self.key_length = key_length
        self.QISKIT_AVAILABLE = QISKIT_AVAILABLE
        
        if self.QISKIT_AVAILABLE:
            try:
                from qiskit_aer import Aer
                self.backend = Aer.get_backend('qasm_simulator')
                print("✅ Qiskit backend ready")
            except:
                self.QISKIT_AVAILABLE = False
                print("❌ Qiskit backend failed, using Python simulation")
        else:
            self.backend = None
        
        print(f"Initialized BB84 with {key_length} qubits")
        
    def alice_prepare_qubits(self):
        """Step 1: Alice prepares qubits in random bases"""
        self.alice_bits = [random.randint(0, 1) for _ in range(self.key_length)]
        self.alice_bases = [random.randint(0, 1) for _ in range(self.key_length)]
        
        print(f"🔐 Alice's original bits: {self.alice_bits[:10]}...")
        print(f"🔐 Alice's bases: {self.alice_bases[:10]}... (0=Z, 1=X)")
        return self.alice_bits, self.alice_bases
    
    def simulate_quantum_measurement(self, alice_bit, alice_basis, bob_basis):
        """Pure Python quantum measurement simulation"""
        if alice_basis == bob_basis:
            return alice_bit
        else:
            return random.randint(0, 1)
    
    def bob_measure_qubits_qiskit(self, eavesdropper_present=False, eavesdrop_prob=0.3):
        """Qiskit implementation for version 2.2.3"""
        self.bob_bases = [random.randint(0, 1) for _ in range(self.key_length)]
        self.bob_bits = []
        
        eve_interceptions = 0
        
        print("⚛️  Using Qiskit 2.2.3 quantum simulation")
        for i in range(self.key_length):
            # Create quantum circuit
            qc = QuantumCircuit(1, 1)
            
            # Alice prepares the qubit
            if self.alice_bits[i] == 1:
                qc.x(0)
            
            if self.alice_bases[i] == 1:  # X-basis
                qc.h(0)
            
            # Eve's interception
            if eavesdropper_present and random.random() < eavesdrop_prob:
                eve_interceptions += 1
                # Eve measures
                eve_basis = random.randint(0, 1)
                if eve_basis == 1:
                    qc.h(0)
                qc.measure(0, 0)
                
                # Execute Eve's measurement (Qiskit 2.x style)
                from qiskit_aer import Aer
                backend = Aer.get_backend('qasm_simulator')
                job = backend.run(qc, shots=1)
                result = job.result()
                counts = result.get_counts()
                eve_bit = int(list(counts.keys())[0])
                
                # Eve re-prepares
                qc = QuantumCircuit(1, 1)
                if eve_bit == 1:
                    qc.x(0)
                if eve_basis == 1:
                    qc.h(0)
            
            # Bob measures
            if self.bob_bases[i] == 1:
                qc.h(0)
            qc.measure(0, 0)
            
            # Execute Bob's measurement (Qiskit 2.x style)
            from qiskit_aer import Aer
            backend = Aer.get_backend('qasm_simulator')
            job = backend.run(qc, shots=1)
            result = job.result()
            counts = result.get_counts()
            bob_bit = int(list(counts.keys())[0])
            self.bob_bits.append(bob_bit)
        
        if eavesdropper_present:
            print(f"👂 Eavesdropper intercepted {eve_interceptions} qubits")
        
        return self.bob_bits, self.bob_bases
    
    def bob_measure_qubits_pure_python(self, eavesdropper_present=False, eavesdrop_prob=0.3):
        """Pure Python implementation"""
        self.bob_bases = [random.randint(0, 1) for _ in range(self.key_length)]
        self.bob_bits = []
        
        eve_interceptions = 0
        
        print("🧪 Using pure Python quantum simulation")
        for i in range(self.key_length):
            current_bit = self.alice_bits[i]
            current_basis = self.alice_bases[i]
            
            # Eve's interception
            if eavesdropper_present and random.random() < eavesdrop_prob:
                eve_interceptions += 1
                eve_basis = random.randint(0, 1)
                current_bit = self.simulate_quantum_measurement(
                    current_bit, current_basis, eve_basis
                )
                current_basis = eve_basis
            
            # Bob measures
            bob_bit = self.simulate_quantum_measurement(
                current_bit, current_basis, self.bob_bases[i]
            )
            self.bob_bits.append(bob_bit)
        
        if eavesdropper_present:
            print(f"👂 Eavesdropper intercepted {eve_interceptions} qubits")
        
        return self.bob_bits, self.bob_bases
    
    def bob_measure_qubits(self, eavesdropper_present=False, eavesdrop_prob=0.3):
        """Main measurement function"""
        if self.QISKIT_AVAILABLE:
            return self.bob_measure_qubits_qiskit(eavesdropper_present, eavesdrop_prob)
        else:
            return self.bob_measure_qubits_pure_python(eavesdropper_present, eavesdrop_prob)
    
    def sift_keys(self):
        """Step 3: Alice and Bob sift their keys by comparing bases"""
        self.sifted_alice_key = []
        self.sifted_bob_key = []
        
        matching_bases = 0
        for i in range(self.key_length):
            if self.alice_bases[i] == self.bob_bases[i]:
                matching_bases += 1
                self.sifted_alice_key.append(self.alice_bits[i])
                self.sifted_bob_key.append(self.bob_bits[i])
        
        print(f"🔄 Sifted key length: {len(self.sifted_alice_key)} (from {matching_bases} matching bases)")
        return self.sifted_alice_key, self.sifted_bob_key
    
    def estimate_error_rate(self, sample_size=0.3):
        """Step 4: Estimate Quantum Bit Error Rate (QBER)"""
        if len(self.sifted_alice_key) == 0:
            return 1.0  # 100% error if no key
        
        sample_count = max(5, int(len(self.sifted_alice_key) * sample_size))
        sample_count = min(sample_count, len(self.sifted_alice_key))
        
        sample_indices = random.sample(range(len(self.sifted_alice_key)), sample_count)
        
        error_count = 0
        for idx in sample_indices:
            if self.sifted_alice_key[idx] != self.sifted_bob_key[idx]:
                error_count += 1
        
        self.sample_indices = sample_indices
        qber = error_count / sample_count if sample_count > 0 else 0
        
        print(f"📊 Tested {sample_count} bits, found {error_count} errors")
        print(f"📊 Quantum Bit Error Rate (QBER): {qber:.3f}")
        
        return qber
    
    def generate_final_key(self, qber_threshold=0.1):
        """Step 5: Generate final key if QBER is below threshold"""
        qber = self.estimate_error_rate()
        
        if qber > qber_threshold:
            print(f"🚨 QBER {qber:.3f} exceeds threshold {qber_threshold}. Key rejected!")
            return None, None, qber
        
        # Remove test bits from final key
        final_alice_key = []
        final_bob_key = []
        for i in range(len(self.sifted_alice_key)):
            if i not in self.sample_indices:
                final_alice_key.append(self.sifted_alice_key[i])
                final_bob_key.append(self.sifted_bob_key[i])
        
        print(f"✅ Final secure key length: {len(final_alice_key)} bits")
        return final_alice_key, final_bob_key, qber

# Standalone testing
if __name__ == "__main__":
    print("Testing BB84 Protocol...")
    bb84 = BB84Protocol(key_length=50)
    bb84.alice_prepare_qubits()
    bb84.bob_measure_qubits(eavesdropper_present=False)
    bb84.sift_keys()
    key, _, qber = bb84.generate_final_key()
    if key:
        print(f"Test successful! Generated {len(key)}-bit key with QBER: {qber:.3f}")