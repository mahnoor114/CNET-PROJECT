Secure Quantum–Classical Hybrid Communication System

This repository contains the step-by-step implementation of a Quantum–Classical Hybrid Communication System, starting from basic classical and quantum protocols and extending to improved, integrated versions as presented in the research paper:

“Secure Quantum–Classical Hybrid Communication:
A Practical Implementation of Superdense Coding, Teleportation, and AES–BB84 Security Layer Using TCP and Qiskit”

The project demonstrates how classical TCP/IP communication can be enhanced with quantum security and efficiency mechanisms using Qiskit simulations.

Project Objectives

Implement basic classical TCP communication

Implement basic quantum protocols (BB84, Superdense Coding, Teleportation)

Gradually improve and integrate these modules into a hybrid secure system

Compare classical vs quantum vs hybrid performance

Provide a practical software-based proof of hybrid quantum communication

 

Implementation Phases
Phase 1: Basic Classical Implementation

TCP/IP client–server communication

Message and file transfer

Latency and reliability measurement

Serves as a baseline for comparison

Folder: 01_classical_basic/

Phase 2: Basic Quantum Protocols

BB84 key generation (basic version)

Superdense Coding (2 classical bits transmitted using 1 qubit)

Quantum Teleportation (quantum state transfer)

Implemented independently using Qiskit

Folder: 02_quantum_basic/

Phase 3: Improved Classical Layer

Latency benchmarking

Throughput analysis

Stability testing

Used to analyze the impact of quantum overhead

Folder: 03_classical_improved/

Phase 4: Improved Quantum Layer

Enhancements based on the research paper include:

BB84 with Quantum Bit Error Rate (QBER) monitoring

Fidelity analysis for:

Superdense coding

Quantum teleportation (approximately 98–99 percent)

Error analysis and robustness testing

Folder: 04_quantum_improved/

Phase 5: Hybrid Quantum–Classical Model

Integration of:

BB84-generated keys

AES encryption for classical data

TCP/IP for message transmission

Quantum layer responsibilities:

Key distribution

Superdense coding

Teleportation

Classical layer responsibilities:

Message routing

Encryption and decryption

Packet delivery

Folder: 05_hybrid_model/

Security Design

BB84 ensures secure quantum key exchange

AES encrypts classical messages using quantum-generated keys

Any eavesdropping attempt increases QBER and becomes detectable

Provides end-to-end confidentiality in the hybrid architecture

Results Summary

Hybrid model introduces a slight latency increase due to quantum operations

Bandwidth efficiency improves through superdense coding

Transmission accuracy reaches approximately 99.8 percent

Teleportation fidelity remains between 98 and 99 percent

Security improves from medium (classical TCP) to very high (hybrid model)

Technologies Used

Python 3.x

Qiskit

TCP/IP Sockets

AES Cryptography

NumPy

Matplotlib

How to Run (Basic)

Install required dependencies:

pip install qiskit cryptography numpy matplotlib


Basic execution flow:

Run the TCP server

Execute BB84 key exchange

Encrypt data using AES

Send encrypted messages via TCP

Decode and verify data using the hybrid model

Reference Paper

The complete methodology, experiments, and evaluation are documented in the included research paper:

paper/research_paper.pdf

Authors

Afza Anjum
Nabeelah Maryam
Mahnoor Haider
Nabeeha Fazail
Mohsin Khan

Department of Data Science
FAST National University, Islamabad

Future Enhancements

Deployment on IBM Quantum hardware

Multi-party quantum communication

Integration of quantum repeaters

Reduced latency hybrid system designs
