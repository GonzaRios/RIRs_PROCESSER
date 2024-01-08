import numpy as np


class Lund():
    def __init__(self):
        self.new_signal = None


    def lundeby_algorithm(impulse_response, fs):
        # if impulse_response.all() == None:
        #     return impulse_response

        interval_length = int(0.05 * fs)  # Interval length in samples (50 ms)

        # Step 1: Convert signal to dB to find noise level
        # Create a 1D array of ones with the specified window size for filter
        window = np.ones(interval_length) / interval_length

        # Apply squared moving average filter
        filtered_data = np.convolve((impulse_response**2), window, mode='same')

        # Convert filtered data to dB:
        filtered_data_dB = 20*np.log10(filtered_data/filtered_data.max())

        
        # Step 2: Estimate background noise level using the tail where is not -inf
        min_index = np.argmin(filtered_data_dB)                                             # index where the first -inf is shown
        filtered_data_dB = filtered_data_dB[0:min_index-1]                                  # cut the response from 0 to the first non -inf index
        noise_length = int(0.1 * len(filtered_data_dB))                                     # Length of noise segment (10% of response)
        noise_level = np.mean(filtered_data_dB[(min_index - noise_length):min_index-1])     # average noise level in the 10%
        
        
        # Step 3: Estimate slope of decay from 0 dB to noise level
        left_index = np.argmax(filtered_data_dB >= 0)                                       # Find index where response is above 0 dB
        right_index = np.argmax(filtered_data_dB <= (noise_level + 10))                     # Find index where response is above noise level + 10 dB

        x = np.arange(len(filtered_data_dB[left_index:right_index]))                        # lenght of x for lin regresion
        coefficients = np.polyfit(x, filtered_data_dB[left_index:right_index], deg=1)       # lin reg coefficient evaluated between the index found before
        x = np.arange(len(filtered_data_dB))
        regression_line = np.polyval(coefficients, x)                                       # linear regression line


        # Step 4: Find preliminary crosspoint
        crosspoint_index = np.argmax(regression_line < (noise_level + 5))                   # Find index where response is above noise level + 5 dB

        n = 2
        safe_zone = 0
        while crosspoint_index == 0:                                                        # Change the limits of the regression until a cross-point is found.
            regression_line = np.polyval(coefficients, n*x)
            crosspoint_index = np.argmax(regression_line < (noise_level + 5))
            n = n+1
            safe_zone = n
        
        # Step 5: Cut the frequency response
        Truncated_signal = filtered_data_dB[0:crosspoint_index]

        # Safety cut zone trigger
        if safe_zone >= 4:                                                                  # Stop recursive algorithm if more than 4 regression lines where necessary
            new_signal = impulse_response[0:crosspoint_index]
            return new_signal

        # Iteration loop
        n=0
        while n != 3:
            noise_length = int(0.1 * len(Truncated_signal))
            min_index = np.argmin(Truncated_signal)
            noise_level = np.mean(Truncated_signal[min_index:])
            left_index = np.argmax(Truncated_signal >= 0)                       
            right_index = np.argmax(Truncated_signal <= (noise_level + 10))


            x = np.arange(len(Truncated_signal[left_index:right_index]))
            coefficients = np.polyfit(x, Truncated_signal[left_index:right_index], deg=1)
            x = np.arange(len(Truncated_signal))
            regression_line = np.polyval(coefficients, x)
            
            crosspoint_index = np.argmax(regression_line < (noise_level + 5))

            if crosspoint_index == 0:
                new_signal = impulse_response[0:len(Truncated_signal)]
                return new_signal

            Truncated_signal = filtered_data_dB[0:crosspoint_index]
            n=n+1

        new_signal = impulse_response[0:crosspoint_index]
        
        return new_signal
