

import matplotlib.pyplot as plt
import pandas as pd

carat = [5, 10, 20, 30, 5, 10, 20, 30, 5, 10, 20, 30]
price = [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600]
color =['D', 'D', 'D', 'E', 'E', 'E', 'F', 'F', 'F', 'G', 'G', 'G',]

df = pd.DataFrame(dict(carat=carat, price=price, color=color))

fig, ax = plt.subplots()

colors = {'D':'red', 'E':'blue', 'F':'green', 'G':'black'}

ax.scatter(df['carat'], df['price'], c=df['color'].apply(lambda x: colors[x]))

# c1, = ax.plot(1, "o", color="red")
# c2, = ax.plot(1, "o", color="blue")
# c3, = ax.plot(1, "o", color="pink")
c1, = ax.plot("o", color="red")
c2, = ax.plot("o", color="blue")
c3, = ax.plot("o", color="pink")


ax.legend([c1,c2,c3], ['c111', 'c2', 'cIII'], numpoints=1)
plt.show()