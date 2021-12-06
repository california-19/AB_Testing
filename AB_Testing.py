import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
np.random.seed(42)

# Load the data file
df = pd.read_excel('AB Test.xlsx')


'''
# We don't need the following lines
df.info()
df['group'].value_counts()
df['action'].value_counts()
'''

# We build a new dataframe with the people in the control group
filt1 = df['group'] == 'control'
control_df = df[filt1]

# We build a new dataframe with the people from the control group who clicked the new ad
filt2 = control_df['action'] == 'view and click'
control_clickers = control_df[filt2]

# Now we find click through rate of the control group
control_click_rate = control_clickers.index.nunique() / control_df.index.nunique()

# We build a new dataframe with the people in the experiment group
filt3 = df['group'] == 'experiment'
experiment_df = df[filt3]

# We build a new dataframe with the people from the experiment group who clicked the new ad
filt4 = experiment_df['action'] == 'view and click'
experiment_clickers = experiment_df[filt4]

# Now we find click through rate of the experiment group
experiment_click_rate = experiment_clickers.index.nunique() / experiment_df.index.nunique()

# The difference in between the click rates
diff = experiment_click_rate - control_click_rate

# ### Bootstrapping
# Bootstrapping is a method to sample with replacement from the dataset. We will use bootstrapping to test our hypothesis if there is a difference between the experiment and the control group. We will run the sampling process 10,000 times to get create a list of differences from each sample.
differences = []
size = df.shape[0]
for i in range(1000):
    sample = df.sample(size, replace=True)
    
    control_df_ = sample[sample['group'] == 'control']
    control_clickers_ = control_df_[control_df_['action'] == 'view and click']
    control_click_rate_ = control_clickers_.index.nunique() / control_df_.index.nunique()
    
    experiment_df_ = sample[sample['group'] == 'experiment']
    experiment_clickers_ = experiment_df_[experiment_df_['action'] == 'view and click']
    experiment_click_rate_ = experiment_clickers_.index.nunique() / experiment_df_.index.nunique()
    
    differences.append(experiment_click_rate_ - control_click_rate_)


# According to the Centrol Limit Theorem, the distribution of the difference in means should have a normal distribution.
# Plot the histogram and see if it looks like a normal distribution.
differences = np.array(differences)
plt.hist(differences);

null_hypothesis = np.random.normal(0, differences.std(), differences.size)

plt.hist(null_hypothesis)
plt.axvline(diff, c = 'red')


# p-value is the probability of observing your statistic if the null hypothesis is true. It corresponds to the area to the right of the red vertical line. Since our significance level is 5%, if the area to the right of the red line is more than 0.05, which is very likely looking at the graph, then we fail to reject the null. This implies that our new ad does not work.

# Compute the p-value
p_value = (null_hypothesis > diff).mean()
# print(p_value)


# # Conclusion
# We fail to reject the null when alpha is 0.05. Our conclusion is not to go for the new ad.

class ABTesting:
    
    def check(self, alpha):
        if p_value <= alpha:
            return True
        else:
            return False


abtesting = ABTesting()
pickle.dump(p_value, open('model.pkl', 'wb'))