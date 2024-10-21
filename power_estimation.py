def parse_stats_file(filename):
    energy_values = {}
    sim_seconds = 0.0
    with open(filename, 'r') as file:
        for line in file:
            if 'system.mem_ctrl.dram.rank0.totalEnergy' in line:
                energy_values['rank0'] = float(line.split()[1]) * 1e-12  # Convert pJ to J
            elif 'system.mem_ctrl.dram.rank1.totalEnergy' in line:
                energy_values['rank1'] = float(line.split()[1]) * 1e-12  # Convert pJ to J
            elif 'simSeconds' in line:
                # print(line.split())
                # print(line.split()[1])
                sim_seconds = float(line.split()[1])
    return energy_values, sim_seconds

def calculate_power(energy_values, sim_seconds):
    total_energy = sum(energy_values.values())
    power = total_energy / sim_seconds  # Power = Energy / Time
    return power

def main():
    filename = '/home/krishna/Desktop/gem5/m5out/stats.txt'
    energy_values, sim_seconds = parse_stats_file(filename)
    
    if sim_seconds == 0:
        print("Simulation time is zero, cannot calculate power.")
        return

    power = calculate_power(energy_values, sim_seconds)
    print(f"Total Power Consumption: {power * 1000:.3f} mW")

if __name__ == "__main__":
    main()
