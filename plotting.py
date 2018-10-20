import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import seaborn as sns
import scipy.stats as scs

def plot_histogram_with_dist(symbol, data, distribution):
    '''
    Histogram of data plotted against provided distribution and
    Kolmogorov-Smirnov test metrics

    Parameters:
    --------------
    symbol: (str)
        Security symbol
    data: (pd.Series)
        Daily returns
    distribution: (str)
        Continuous distribution used in K-S test, either 'norm' or 'laplace'

    Returns:
    --------------
    p-value: (int)
        p-value of K-S test, null hypothesis= distributions are the same
    '''

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    x_range = np.linspace(scs.norm.ppf(0.0001, data.mean(), data.std()),scs.norm.ppf(0.9999, data.mean(), data.std()), 100)
    ax.hist(data, normed=True, bins=100, color='blue')
    if distribution == 'norm':
        dist = scs.norm.pdf(x_range, data.mean(), data.std())
    elif distribution == 'laplace':
        dist = scs.laplace.pdf(x_range, data.mean(), data.std())
    ax.plot(x_range, dist, label='normal pmf', color='r')
    test_stat = '{:.4f}'.format(scs.kstest(data, distribution,args=[data.mean(), data.std()])[0])
    # p_value = '{:.4f}'.format(scs.kstest(data, distribution,args=[data.mean(), data.std()])[1])
    p_value = scs.kstest(data, distribution,args=[data.mean(), data.std()])[1]
    ax.set_title(f'{symbol} Returns: mean:{data.mean():.4f} std:{data.std():.4f}\ntest statistic: {test_stat}, p-value: {p_value}')
    ax.set_xlabel(f'{symbol} Returns')

    return float(p_value)


def corr_heatmap_with_values(df):
    '''
    Plots correlation heatmap w/ correlation values

    Parameters:
    ------------
    df : (df)
        index: (pd.datetime Series), columns: (security symbols)

    Returns:
    ------------
    None

    '''
    corr = df.corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(10,10))
#     cmap = sns.color_palette('coolwarm')
    sns.heatmap(corr, mask=mask, center=0, square=True, linewidths=.5,
                yticklabels=True, annot=True, fmt='.2f', cbar_kws={'shrink':.5})
    plt.title('Correlation Matrix', fontsize=20)
    plt.xticks(rotation=90, fontsize=11)
    plt.yticks(rotation=0, fontsize=11)
    plt.tight_layout()

if __name__ == '__main__':
    pass
