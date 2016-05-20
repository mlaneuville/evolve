import argparse 
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("datafile")

args = parser.parse_args()

print(args.datafile)

df = pd.read_csv(args.datafile)
print(df.head())

for feature in df:
    if feature == "iter" or feature == "time":
        continue
    if df[feature].mean() > 0.:
        plt.plot(df['time'], df[feature], lw=2, label=feature)

plt.legend(loc='best')
plt.yscale('log')
plt.grid()
plt.savefig("report.png", format="png", bbox_inches="tight")
