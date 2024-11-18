import ipywidgets as widgets
import matplotlib.pyplot as plt
from matplotlib import colormaps
from IPython.display import clear_output, display
from ipywidgets import Output


def plot_batch_data(data, x_axis_name='Time (h)'):
    '''
    A function to plot batch data in this notebook.
    '''
    
    # Dropdown to select variable
    variable_list = data.columns
    variable_plot_selection = widgets.Dropdown(
        options=variable_list,
        value=variable_list[1],
        description='Variable:'
    )

    # Multi-select widget to choose multiple batches
    batch_references = data['Batch reference'].unique()
    batch_multi_select = widgets.SelectMultiple(
        options=batch_references,
        value=[batch_references[0]],  # Default selection
        description='Batches:',
        layout=widgets.Layout(height='150px')  # Adjust height for better display
    )

    # Create an Output widget for displaying the plot
    plot_output = Output()

    # Function to update the plot
    def update_plot_multi(variable_name, batches, x_axis_name='Time (h)'):
        with plot_output:
            clear_output(wait=True)  # Clear the output area for the plot

            fig, ax = plt.subplots(figsize=(8, 6))

            # Generate colormaps
            cmap_NOC = colormaps['Blues']  # Non-faulty batches
            cmap_faults = colormaps['Reds']  # Faulty batches

            # Create colors for the batches
            colors_NOC = [cmap_NOC(0.15 + (i * 0.85 / len(batches))) for i in range(len(batches))]
            colors_faults = [cmap_faults(0.15 + (i * 0.85 / len(batches))) for i in range(len(batches))]

            for i, batch in enumerate(batches):
                batch_data = data[data['Batch reference'] == batch]

                # Check if the batch is faulty
                if batch_data['Faulty batch'].all():  # All 1's means it's faulty
                    color = colors_faults[i]
                else:
                    color = colors_NOC[i]

                batch_data.plot(
                    x=x_axis_name,
                    y=variable_name,
                    ax=ax,
                    color=color,  # Assign the appropriate color
                    label=f'Batch {batch}'
                )

            ax.set_title(f'Variable: {variable_name}')
            ax.set_xlabel(x_axis_name)
            ax.set_ylabel(variable_name)
            ax.legend(title='Batch Reference')
            plt.show()

    # Create interactive widget for multi-batch selection
    interactive_plot_multi = widgets.interactive(
        update_plot_multi,
        variable_name=variable_plot_selection,
        batches=batch_multi_select
    )

    # Display the interactive widget
    display(variable_plot_selection, batch_multi_select, plot_output)
