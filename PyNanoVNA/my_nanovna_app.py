# Want a program to take S11 measurements and store them - boom, simple as
# maybe plot ...

import nanovna
import numpy as np
import matplotlib.pyplot as plt


#---------------------------------------- VNA CLASS -------------------------------------------------------

class VNA:
    def __init__(self):     # constructor doesnt do anything right now, init is the constructor and intializes the data members of the class when an object is created
        
        pass        # current set-up does nothing


    #method to get reflection measurements, measures s11 parameter, scans over frequency range takes multiple measurements
    # returns a mean and a standard deviation
    def get_s11_measurements(self, min_freq, max_freq, n_integrations=5):    # 5 repeat measurements
        vna = nanovna.NanoVNA(nanovna.getport())                # creates a new vna object using the nanovna API, vna is now object representing the NanoVNA                                    
        vna.open()                                              # opens the connection to the device 
        vna.resume()                                            # device ready to start taking measurements
        vna.set_frequencies(start=min_freq, stop=max_freq)      # sets frequency range of measurements: min freq to max freq
        vna.set_sweep(start=min_freq, stop=max_freq)            # tells the NanoVNA device to to sweep over that frequency range (API requirement?)
        scans = [vna.scan() for i in np.arange(n_integrations)] # list comprehension, compact way to make list, this basically tells the VNA to perform n_integrations numbers of sweeps
                                                                # results of each sweep stored as element in list called scans
        scan_s11 = []                                           # empty list to hold the s11 measurements frome each scan
        for scan in scans:                                      # each 'scan' is the data returned by one sweep (one call to vna.scan())
            s11 = scan[0]                                       #scan[0] is the first element of scan, the first element is the s11 measurement 
            scan_s11.append(s11)                                # adds the extraced s11 data to the scan_s11 list, when loop finishes it will contain the s11s from each sweep
        scan_s11 = np.array(scan_s11)                           # converts this list to a numpy array 
        scan_s11_mean, scan_s11_std = np.mean(scan_s11, axis=0), np.std(scan_s11, axis=0)       # calculates the mean and std variation of s11 across the repeated sweeps 
        vna.pause()                                             # get one average s11 value and one standard deviation value for every frequency point 
        
    
        return scan_s11_mean, scan_s11_std, vna.frequencies
    
    def get_s12_measurements(self, min_freq, max_freq, n_integrations=5):     # this does the same but for the s12 measurements
        vna = nanovna.NanoVNA(nanovna.getport())
        vna.open()
        vna.set_frequencies(start=min_freq, stop=max_freq)
        vna.set_sweep(start=min_freq, stop=max_freq)
        scans = [vna.scan() for i in np.arange(n_integrations)]

        scan_s12 = []
        for scan in scans:
            s12 = scan[1]                           # second element of scan is s12 ( the transmission coeff from port 1 to port 2 )
            scan_s12.append(s12)
        scan_s12 = np.array(scan_s12)
        scan_s12_mean, scan_s12_std = np.mean(scan_s12, axis=0), np.std(scan_s12, axis=0)
        
    
        return scan_s12_mean, scan_s12_std, vna.frequencies
    
# -------- Main Function ----------------------------------------------------------------------------------------------------------

vna_object = VNA()


_min_freq = float(input(" Start freq (MHz): \n"))   # user defined start and stop frequencies 
_max_freq = float(input(" Stop freq (MHz) : \n"))
_min_freq *= 1000000
_max_freq *= 1000000

action = int(input("What action would you like to carry out:\n 1 - s11 measurements \n 2 - s12 measurements\n 3 - calibration \n"))  # user chooses action

match action:

    case 1:    #  Get s11 measurements

        label = input("Label for measurements: \n")  # user defined label

        m, std, f = vna_object.get_s11_measurements(_min_freq, _max_freq)
                                        
        np.save(f'vna_data2/{label}_mean.npy', m)
        np.save(f'vna_data2/{label}_std.npy', std)
        np.save(f'vna_data2/{label}_freq.npy', f)
        print('------done-------')


        # plot
        plt.figure(figsize=(10, 5))
        plt.plot(f / 1e6, 20 * np.log10(np.abs(m)))
        plt.title("S11 Magnitude (dB)")
        plt.xlabel("Frequency (MHz)")
        plt.ylabel("Magnitude (dB)")
        plt.grid(True)
        plt.ylim(-50, 0)
        plt.show()

    case 2:     # Get s12 measurements

        label = input("Label for measurements: \n")  # user defined label
         
        m, std, f = vna_object.get_s12_measurements(_min_freq, _max_freq)
        np.save(f'vna_data2/{label}_mean.npy', m)
        np.save(f'vna_data2/{label}_std.npy', std)
        np.save(f'vna_data2/{label}_freq.npy', f)
        print('------done-------') 

        #  Plot s12 magnitude
        plt.figure(figsize=(10, 5))
        plt.plot(f / 1e6, 20 * np.log10(np.abs(m)))
        plt.title("S12 Magnitude (dB)")
        plt.xlabel("Frequency (MHz)")
        plt.ylabel("Magnitude (dB)")
        plt.grid(True)
        plt.ylim(-50, 0)
        plt.show()

    case 3: # calibration

        caltype = input("Choose calibration type - S O L \n").upper()
        cal_data, _, freqs = vna_object.get_s11_measurements(_min_freq, _max_freq)

        np.save(f'vna_data2/cal_{caltype}_s11.npy', cal_data)
        np.save(f'vna_data2/cal_{caltype}_freq.npy', freqs)

        print('------ Calibration data saved for {caltype} -------')

        plt.plot(freqs / 1e6, 20 * np.log10(np.abs(cal_data)))
        plt.title(f'{caltype} Calibration S11 (logmag)')
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('S11 (dB)')
        plt.grid(True)
        plt.ylim(-50, 0)
        plt.show()