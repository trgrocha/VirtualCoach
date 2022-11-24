import matplotlib.pyplot as plt

x = [1,2,3,4,5,6,7,8]  #fake data
y = [1,2,3,4,3,2,9,12]

plt.subplots()

plt.plot(x, y, 'k')
plt.grid()
plt.margins(0) # remove default margins (matplotlib verision 2+)

plt.axhspan(0, 4, facecolor='green', alpha=0.5)
plt.axhspan(4, 9, facecolor='yellow', alpha=0.5)
plt.axhspan(9, 12, facecolor='red', alpha=0.5)

plt.show()