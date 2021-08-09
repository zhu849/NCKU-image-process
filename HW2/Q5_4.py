import matplotlib.pyplot as plt
import numpy as np
plt.bar(["Before Resize","After Resize"],
        [93.86,84.92],
        width = 0.5,
        align='center', 
        color=['lightsteelblue', 'cornflowerblue'])
plt.grid(linewidth=1, axis='y')
plt.title('Resize augmentation comparison')
plt.ylim(60,100)
plt.yticks(np.arange(60, 100, 5))
plt.show()