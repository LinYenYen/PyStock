from matplotlib import pyplot as plt



####################################################################################################
#                                             Setting                                              #
####################################################################################################
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']



####################################################################################################
#                                             Variable                                             #
####################################################################################################



####################################################################################################
#                                             Function                                             #
####################################################################################################
def dataframe2image(df):
    # Create fig, ax
    fig, ax = plt.subplots()
    # Setting
    ax.axis('tight')
    ax.axis('off')
    # Plot table
    img = plt.table(
        colLabels=df.columns,
        cellText=df.values,
        loc='center',
        cellLoc='center',
        fontsize=100.0
    )

    plt.savefig('stock.png')
    plt.close()
    # plt.show()

    return img



