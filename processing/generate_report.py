import argparse 
import pandas as pd
import matplotlib.pyplot as plt

PARSER = argparse.ArgumentParser()
PARSER.add_argument("datafile")

ARGS = PARSER.parse_args()

print(ARGS.datafile)

DF = pd.read_csv(ARGS.datafile)
print(DF.head())

for feature in DF:
    if feature == "iter" or feature == "time":
        continue
    if DF[feature].mean() > 0.:
        plt.plot(DF['time'], DF[feature], lw=2, label=feature)

plt.legend(loc='best')
plt.yscale('log')
plt.grid()
plt.savefig("report.pdf", format="pdf", bbox_inches="tight")
