###########################################
#PORTIONS OF THIS NOTEBOOK ARE DUPLICATED
#FROM UDACITY CUSTOMER SEGMENTS PROJECT
#VISUALS 
#
#Suppress matplotlib user warnings
# Necessary for newer version of matplotlib
import warnings
warnings.filterwarnings("ignore", category = UserWarning, module = "matplotlib")
#
# Display inline matplotlib plots with IPython
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
###########################################
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import numpy as np

def pca_results(good_data, pca):
	'''
	Create a DataFrame of the PCA results
	Includes dimension feature weights and explained variance
	Visualizes the PCA results
	'''

	# Dimension indexing
	dimensions = dimensions = ['Dimension {}'.format(i) for i in range(1,len(pca.components_)+1)]

	# PCA components
	components = pd.DataFrame(np.round(pca.components_, 4), columns = good_data.keys())
	components.index = dimensions

	# PCA explained variance
	ratios = pca.explained_variance_ratio_.reshape(len(pca.components_), 1)
	variance_ratios = pd.DataFrame(np.round(ratios, 4), columns = ['Explained Variance'])
	variance_ratios.index = dimensions

	# Create a bar plot visualization
	fig, ax = plt.subplots(figsize = (14,8))

	# Plot the feature weights as a function of the components
	components.plot(ax = ax, kind = 'bar');
	ax.set_ylabel("Feature Weights")
	ax.set_xticklabels(dimensions, rotation=0)


	# Display the explained variance ratios
	for i, ev in enumerate(pca.explained_variance_ratio_):
		ax.text(i-0.40, ax.get_ylim()[1] + 0.05, "Explained Variance\n%.4f"%(ev))

	# Return a concatenated DataFrame
	return pd.concat([variance_ratios, components], axis = 1)

def histPlot(Data,featureNames,Title,bins):
    '''
    Create a histogram plot using a Dataframe of data, list/array of feature names,
    a title, and number of bins as inputs.
    '''
    # Create figure
    fig = plt.figure(figsize = (11,5));

    #feature plotting
    for i, feature in enumerate(featureNames):
        ax = fig.add_subplot(3, 2, i+1)
        ax.hist(Data[feature],bins, color = '#00A0A0')
        ax.set_title("'%s' Feature Distribution"%(feature), fontsize = 14)
        ax.set_xlabel("Value")
        ax.set_ylabel("Number of Records")
        ax.set_ylim((0, 200))
        ax.set_yticks([0, 75, 150, 225, 300])
        ax.set_yticklabels([0, 75, 150, 225, ">300"])

    # Plot aesthetics
    fig.suptitle(Title, \
        fontsize = 16, y = 1.03)
    fig.tight_layout() 
    fig.show()
                   
def biplot(good_data,reduced_data, labels, pca, Title):
    '''
    Produce a biplot that shows a scatterplot of the reduced
    data and the projections of the original features.
    
    good_data: original data, before transformation.
               Needs to be a pandas dataframe with valid column names
    reduced_data: the reduced data (the first two dimensions are plotted)
    pca: pca object that contains the components_ attribute
    return: a matplotlib AxesSubplot object (for any additional customization)
    
    This procedure is inspired by the script:
    https://github.com/teddyroland/python-biplot
    '''
    
    plot_data = pd.concat([labels, reduced_data], axis = 1)

    # Generate the cluster plot
    fig, ax = plt.subplots(figsize = (14,8))

    # Color map
    cmap = cm.get_cmap('gist_rainbow')
    centers=2
    # Color the points based on assigned cluster
    for i, label in plot_data.groupby('StageLabel'):   
        label.plot(ax = ax, kind = 'scatter', x = 'Dimension 1', y = 'Dimension 2', \
                     color = cmap((i)*1.0/2), label = 'StageLabel %i'%(i), s=30);
    
    feature_vectors = pca.components_.T
    # we use scaling factors to make the arrows easier to see
    #arrow_size, text_pos = 7.0, 8.0,
    arrow_size=0.75
    text_pos=1.0
    # projections of the original features
    for i, v in enumerate(feature_vectors):
        ax.arrow(0, 0, arrow_size*v[0], arrow_size*v[1], 
                  head_width=0.05, head_length=0.05, linewidth=1, color='red')
        ax.text(v[0]*text_pos, v[1]*text_pos, good_data.columns[i], color='black', 
                 ha='center', va='center', fontsize=12)

    ax.set_xlabel("Dimension 1", fontsize=14)
    ax.set_ylabel("Dimension 2", fontsize=14)
    ax.set_title(Title, fontsize=16);
    return ax

def biplot3D(reduced_data, labels,Title):
    '''
    Create a 3D scatterplot in a similar manner to the biplot above
    Inputs reduced pca (of 3 components) daa, true labels, and Title
    '''
    plot_data = pd.concat([labels, reduced_data], axis = 1)
    # Generate the cluster plot
    fig = plt.figure(figsize= (14,8))
    ax = fig.add_subplot(111, projection='3d')
    # Color map
    cmap = cm.get_cmap('gist_rainbow')
    centers=2
    # Color the points based on assigned cluster
    for i, label in plot_data.groupby('StageLabel'):   
        xs = label['Dimension 1']
        ys = label['Dimension 2']
        zs = label['Dimension 3']
        if i == 1:
            c = 'r'
            ax.scatter(xs, ys, zs, c='r', label = 'StageLabel {}'.format(i), s=30, alpha = 0.5)
        if i == 2:
            c = 'g'
            ax.scatter(xs, ys, zs, c='b', label = 'StageLabel {}'.format(i), s=30, alpha = 0.5)
    #plot aesthetic
    ax.set_xlabel("Dimension 1", fontsize=14)
    ax.set_ylabel("Dimension 2", fontsize=14)
    ax.set_zlabel("Dimension 3", fontsize=14)
    ax.legend(bbox_to_anchor = (1.5, 1))
    ax.set_title(Title, fontsize=16);

    return ax


def clustplot3D(reduced_data, labels, clusterLabels,Title):
    '''
    Produce a 3d scatterplot of clustered results on a 3 component pca feature set

    reduced_data: the reduced data (the first three dimensions are plotted)
    return: a matplotlib AxesSubplot object (for any additional customization)
    '''
    plot_data = pd.concat([clusterLabels, labels, reduced_data], axis = 1)
    # Generate the cluster plot
    fig = plt.figure(figsize= (14,10))
    ax = fig.add_subplot(111, projection='3d')
    # Color map
    cmap = cm.get_cmap('gist_rainbow')
    colors = ['r','b','g','y']
    centers=2
    # Color the points based on assigned cluster
    for i, label in plot_data.groupby('Cluster'):   


        #Stage 1 
        xs = label['Dimension 1'][label['StageLabel']==1]
        ys = label['Dimension 2'][label['StageLabel']==1]
        zs = label['Dimension 3'][label['StageLabel']==1]
        marker = 'o'
        ax.scatter(xs, ys, zs, c=colors[i-1],marker = marker, label = 'Cluster {} Stage 1'.format(i), s=30, alpha = 0.5)
        #Stage 2
        xs = label['Dimension 1'][label['StageLabel']==2]
        ys = label['Dimension 2'][label['StageLabel']==2]
        zs = label['Dimension 3'][label['StageLabel']==2]
        marker = 'x'
        ax.scatter(xs, ys, zs, c=colors[i-1],marker = marker, label = 'Cluster {} Stage 2'.format(i), s=30, alpha = 0.5)
    #Plot aesthetics
    ax.set_xlabel("Dimension 1", fontsize=14)
    ax.set_ylabel("Dimension 2", fontsize=14)
    ax.set_zlabel("Dimension 3", fontsize=14)
    ax.legend(bbox_to_anchor = (1.5, 1))
    ax.set_title(Title, fontsize=16)

    return ax

def isomap2D(reduced_data, labels, Title):
    """2d scatterplot of 2 isomap components
    """
    
    plot_data = pd.concat([labels, reduced_data], axis = 1)

    # Generate the cluster plot
    fig, ax = plt.subplots(figsize = (14,8))

    # Color map
    cmap = cm.get_cmap('gist_rainbow')
    centers=2
    # Color the points based on assigned cluster
    for i, label in plot_data.groupby('StageLabel'):   
        label.plot(ax = ax, kind = 'scatter', x = 'Dimension 1', y = 'Dimension 2', \
                     color = cmap((i)*1.0/2), label = 'StageLabel %i'%(i), s=30,alpha =0.5);
    #Plot aesthetic
    ax.set_xlabel("Dimension 1", fontsize=14)
    ax.set_ylabel("Dimension 2", fontsize=14)
    ax.set_title(Title, fontsize=16)
    
    return ax

 
