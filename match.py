import pandas as pd
import sys



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python match.py <Power csv> <System csv> <Output csv>")
        sys.exit(1)
    
    power = sys.argv[1]
    system = sys.argv[2]
    out = sys.argv[3]
    
    system_df = pd.read_csv(system, parse_dates=['Timestamp'])
    power_df = pd.read_csv(power,parse_dates=['Timestamp'])

    merged_df = pd.merge_asof(system_df.sort_values('Timestamp'), 
                            power_df.sort_values('Timestamp'), 
                            on='Timestamp', 
                            direction='nearest')

    merged_df.to_csv(out, index=False)

    print(merged_df)