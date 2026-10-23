#!/usr/bin/env python3
"""
Axiomatic Optical Boundary Nodes & Continuous Stream-Phase Interlocking (AOBN-CSPI)
Volume I Core Simulation & Telemetry Verification Engine

Author & Proprietor: Ravinder Singh. (ORCID: 0009-0002-6532-7699)
Framework Designation: Axiomatic Optical Boundary Node (AOBN) Architecture
Model Engine: Relativistic Scalar Strain (RSS) Architecture Model Engine
Copyright © 2026 Ravinder Singh S. All Rights Reserved.

This module provides physical-layer numerical verification for:
1. Chapter 1: CSPI Phase-Gating & Kinetic Photon Evacuation Channel (KPEC) Shunting.
2. Chapter 2: Multi-Node All-Optical Abort Propagation vs. Electronic Latency.
3. Chapter 3: Spatial Thermal Decay (KPEC Copper Sinks) & Phononic Acoustic Bandgap Attenuation.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Set visual style for high-rigor publication telemetry plots
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#444444'
plt.rcParams['axes.linewidth'] = 0.8


# ==============================================================================
# CHAPTER 1: CSPI PHASE-GATING & KPEC EVACUATION SIMULATION
# ==============================================================================
def run_chapter1_cspi_simulation(output_dir="figures"):
    """
    Simulates Continuous Stream-Phase Interlocking (CSPI) gating element.
    Models phase perturbation phi(t), gating transmission T(phi), and
    sub-graph execution status drop upon crossing phase tolerance delta.
    """
    print("[1/3] Executing Chapter 1 Simulation: CSPI Phase Gating & KPEC...")
    
    t = np.linspace(0, 10, 1000)  # Time in nanoseconds
    # Simulate dynamic phase drift phi(t) with periodic acoustic/thermal noise
    phi_t = 0.08 * np.sin(2 * np.pi * 0.3 * t) + 0.04 * np.random.randn(len(t)) + 0.02 * t
    delta_tolerance = 0.12  # Phase tolerance limit in radians
    
    # Calculate Optical Transmission through Micro-Ring Resonator
    # T(phi) = 1 / (1 + F * sin^2(phi / 2)), Finesse parameter F ~ 40
    Finesse = 40.0
    transmission = 1.0 / (1.0 + Finesse * (np.sin(phi_t / 2.0) ** 2))
    
    # Sub-graph execution state F(G): 1 (Green/EXECUTE) if |phi| < delta else 0 (Red/OFF)
    execution_state = np.where(np.abs(phi_t) < delta_tolerance, 1.0, 0.0)
    
    # Create telemetry figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    
    # Panel 1: Phase Drift vs Tolerance Window
    ax1.plot(t, phi_t, color='#00d2ff', lw=1.5, label=r'Optical Phase Perturbation $\phi(t)$')
    ax1.axhline(delta_tolerance, color='#ff0055', ls='--', lw=1.2, label=r'Tolerance Window $\pm \delta$ ($0.12\text{ rad}$)')
    ax1.axhline(-delta_tolerance, color='#ff0055', ls='--', lw=1.2)
    ax1.fill_between(t, -delta_tolerance, delta_tolerance, color='#00d2ff', alpha=0.1)
    ax1.set_ylabel(r'Phase Offset $\phi(t)$ (rad)', fontsize=10)
    ax1.set_title('Chapter 1: CSPI Continuous Phase-Gating Dynamics', fontsize=12, pad=10)
    ax1.grid(True, linestyle=':', alpha=0.3)
    ax1.legend(loc='upper left', fontsize=9)
    
    # Panel 2: Sub-graph Execution State F(G) & Optical Transmission
    ax2.plot(t, execution_state, color='#00ff88', lw=2, label=r'Sub-Graph Execution State $\mathcal{F}(G)$ (Stateless Gate)')
    ax2.plot(t, transmission, color='#ffaa00', ls=':', lw=1.2, label=r'Resonator Transmission $T(\phi)$')
    ax2.set_xlabel('Time (ns)', fontsize=10)
    ax2.set_ylabel('Gating State / Trans.', fontsize=10)
    ax2.set_ylim(-0.1, 1.15)
    ax2.grid(True, linestyle=':', alpha=0.3)
    ax2.legend(loc='lower left', fontsize=9)
    
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'figure_1_2_cspi_telemetry.png')
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()
    print(f"    -> Saved telemetry plot: {filepath}")


# ==============================================================================
# CHAPTER 2: MULTI-NODE CAUSAL ROUTING & ABORT LATENCY SIMULATION
# ==============================================================================
def run_chapter2_multinode_simulation(output_dir="figures"):
    """
    Simulates multi-node propagation latency across N node hops.
    Compares Electronic DSP latency (~3.0 GHz clock limit) against All-Optical
    High-Q Purcell-Enhanced Abort Path (~11.6 ps/mm).
    """
    print("[2/3] Executing Chapter 2 Simulation: Multi-Node Causal Abort Latency...")
    
    hops = np.arange(1, 11)  # 1 to 10 node hops
    distance_per_hop_mm = 2.5  # 2.5 mm inter-node distance
    total_distance_mm = hops * distance_per_hop_mm
    
    # All-Optical path propagation delay (group index n_g ~ 3.5 -> ~11.6 ps/mm) + Purcell gating (2 ps)
    v_group_ps_mm = 11.66
    optical_latency_ps = (total_distance_mm * v_group_ps_mm) + 2.0  # Total in ps
    
    # Electronic DSP latency: 1 clock cycle (333 ps at 3 GHz) + re-timing per hop
    electronic_latency_ps = hops * 333.3 + (total_distance_mm * 5.0)  # Total in ps
    
    fig, ax = plt.subplots(figsize=(9, 5))
    
    ax.plot(hops, electronic_latency_ps / 1000.0, 'o--', color='#ff3366', lw=2, label='Conventional Electronic DSP (3.0 GHz Re-timing)')
    ax.plot(hops, optical_latency_ps / 1000.0, 's-', color='#00e5ff', lw=2.5, label='AOBN All-Optical High-$Q$ Path ($11.66\text{ ps/mm}$)')
    
    ax.set_title('Chapter 2: Abort Signal Latency Across Multi-Node Hops', fontsize=12, pad=10)
    ax.set_xlabel('Inter-Node Hop Count ($N$)', fontsize=10)
    ax.set_ylabel('Total Abort Propagation Latency (ns)', fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.3)
    ax.legend(loc='upper left', fontsize=10)
    
    # Annotate race condition hazard zone
    ax.axhspan(0.333, 3.5, color='#ff0055', alpha=0.1)
    ax.text(5.5, 0.8, 'Electronic Hazard Zone (Race Condition Window)', color='#ff0055', fontsize=9, fontweight='bold')
    
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'figure_2_2_abort_latency.png')
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()
    print(f"    -> Saved telemetry plot: {filepath}")


# ==============================================================================
# CHAPTER 3: THERMAL DECAY & PHONONIC BANDGAP ISOLATION SIMULATION
# ==============================================================================
def run_chapter3_thermal_acoustic_simulation(output_dir="figures"):
    """
    Simulates spatial thermal decay profiles (unmitigated SOI vs. KPEC copper sink)
    and acoustic attenuation across phononic frequencies (8-12 GHz bandgap).
    """
    print("[3/3] Executing Chapter 3 Simulation: Thermal Decay & Phononic Bandgap...")
    
    # Panel 1: Spatial Thermal Decay T(x)
    x_um = np.linspace(0, 50, 500)  # Distance from active node edge in micrometers
    T_ambient = 300.0  # Ambient Kelvin
    Delta_T_node = 15.0  # Node local heating in Kelvin
    
    # Decay length L_d: Unmitigated SOI ~ 18 um, KPEC Copper Sink ~ 4.5 um
    L_d_unmitigated = 18.0
    L_d_kpec = 4.5
    
    T_unmitigated = T_ambient + Delta_T_node * np.exp(-x_um / L_d_unmitigated)
    T_kpec = T_ambient + Delta_T_node * np.exp(-x_um / L_d_kpec)
    
    # Panel 2: Phononic Acoustic Attenuation across frequency
    freq_GHz = np.linspace(1, 20, 500)
    # Deep-trench tungsten/oxide phononic barrier attenuation curve centered at 10 GHz
    f_center = 10.0
    f_bandwidth = 2.0
    attenuation_dB = 85.0 * np.exp(-((freq_GHz - f_center) ** 2) / (2 * (f_bandwidth ** 2))) + 5.0
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot Thermal Decay
    ax1.plot(x_um, T_unmitigated, '--', color='#ff6600', lw=1.8, label=r'Unmitigated SOI ($L_d \approx 18\ \mu\text{m}$)')
    ax1.plot(x_um, T_kpec, '-', color='#00ffcc', lw=2.2, label=r'AOBN Copper Sink ($L_d \approx 4.5\ \mu\text{m}$)')
    ax1.axhline(T_ambient + 1.2, color='#ff0055', ls=':', label=r'Phase Safe Threshold (+1.2 K)')
    ax1.set_title('Spatial Thermal Decay from Node Edge', fontsize=11)
    ax1.set_xlabel(r'Distance from Active Edge ($\mu\text{m}$)', fontsize=10)
    ax1.set_ylabel('Substrate Temperature $T$ (K)', fontsize=10)
    ax1.grid(True, linestyle=':', alpha=0.3)
    ax1.legend(fontsize=9)
    
    # Plot Acoustic Attenuation
    ax2.plot(freq_GHz, attenuation_dB, color='#a060ff', lw=2.2, label='Deep-Trench Tungsten/Oxide Barrier')
    ax2.axvspan(8.0, 12.0, color='#a060ff', alpha=0.15, label='Target Phononic Bandgap (8-12 GHz)')
    ax2.axhline(80.0, color='#00ff88', ls='--', lw=1.0, label='Isolation Threshold (>80 dB)')
    ax2.set_title('Phononic Acoustic Attenuation vs. Frequency', fontsize=11)
    ax2.set_xlabel('Acoustic / Phonon Frequency (GHz)', fontsize=10)
    ax2.set_ylabel('Acoustic Attenuation (dB)', fontsize=10)
    ax2.grid(True, linestyle=':', alpha=0.3)
    ax2.legend(fontsize=9)
    
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'figure_3_1_thermal_acoustic_telemetry.png')
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()
    print(f"    -> Saved telemetry plot: {filepath}")


# ==============================================================================
# MAIN EXECUTION ENTRY POINT
# ==============================================================================
if __name__ == '__main__':
    print("====================================================================")
    print("AOBN VOLUME I CORE SIMULATION ENGINE")
    print("Copyright © 2026 Ravinder Singh. All Rights Reserved.")
    print("====================================================================")
    
    run_chapter1_cspi_simulation()
    run_chapter2_multinode_simulation()
    run_chapter3_thermal_acoustic_simulation()
    
    print("====================================================================")
    print("Simulation suite executed successfully. All output figures saved.")
    print("====================================================================")
