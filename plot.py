import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot.py <Merged csv>")
        sys.exit(1)
    
    merged = sys.argv[1]
    merged_df = system_df = pd.read_csv(merged, parse_dates=['Timestamp'])

    # Calculate the network rates 
    merged_df['Net_RX_Rate'] = merged_df['Net_RX_Bytes'].diff().abs()
    merged_df['Net_TX_Rate'] = merged_df['Net_TX_Bytes'].diff().abs()
    merged_df['Net_Combined_Rate'] = merged_df['Net_RX_Rate'] + merged_df['Net_TX_Rate']

    # List of plots
    plots = [
        ('Power', merged_df['Power'], 'green'),
        ('Network Absolute Bytes', merged_df['Net_RX_Bytes'], 'blue', merged_df['Net_TX_Bytes'], 'red'),
        ('Network Combined Rate', merged_df['Net_Combined_Rate'], 'purple'),
        ('CPU System', merged_df['CPU_System'], 'purple'),
        ('CPU Idle', merged_df['CPU_Idle'], 'orange'),
        ('RAM Free', merged_df['RAM_Free'], 'brown'),
        ('RX-TX Bytes Ratio', merged_df['Net_RX_Bytes'] / merged_df['Net_TX_Bytes'], 'pink'),
        ('RX-TX Bytes Difference', merged_df['Net_RX_Bytes'] - merged_df['Net_TX_Bytes'], 'cyan')
    ]

    # Create the pdf for the plots
    for plot_info in plots:
        name = plot_info[0]
        with PdfPages(f'{name.replace(" ", "_")}_plot.pdf') as pdf:
            plt.figure(figsize=(10, 6))
            
            if len(plot_info) == 3:  
                plt.plot(merged_df['Timestamp'], plot_info[1], color=plot_info[2])
            elif len(plot_info) == 5:  
                plt.plot(merged_df['Timestamp'], plot_info[1], label='RX', color=plot_info[2])
                plt.plot(merged_df['Timestamp'], plot_info[3], label='TX', color=plot_info[4])
                plt.legend()
            
            plt.title(name)
            plt.xlabel('Timestamp')
            plt.ylabel('Value')
            plt.xticks(rotation=45)
            plt.tight_layout()
            pdf.savefig()
            plt.close()