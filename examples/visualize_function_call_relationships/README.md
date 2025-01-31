# Function Relationship Visualizations

This example demonstrates four different approaches to visualizing code relationships using Codegen. Each visualization script creates a graph to help developers understand different aspects of code structure and dependencies.

## Visualization Types

### 1. Function Call Relationships (run_1.py)
Traces downstream function call relationships from a target method:
```python
# Example starting from a specific method
target_class = codebase.get_class("SharingConfigurationViewSet")
target_method = target_class.get_method("patch")
```
- Shows all functions called by the target method
- Tracks nested function calls up to a configurable depth
- Distinguishes between regular functions, methods, and external calls
- Color codes different types of functions for better visualization

### 2. Symbol Dependencies (run_2.py)
Maps symbol dependencies throughout the codebase:
```python
# Example starting from a specific function
target_func = codebase.get_function("get_query_runner")
```
- Visualizes both direct symbol references and imports
- Tracks relationships between functions, classes, and external modules
- Prevents circular dependencies through cycle detection
- Uses distinct colors to differentiate symbol types

### 3. Function Blast Radius (run_3.py)
Shows the impact radius of potential changes:
```python
# Example analyzing impact of changes to a function
target_func = codebase.get_function("export_asset")
```
- Identifies all usages of a target function
- Highlights HTTP method handlers specially
- Shows how changes might propagate through the codebase
- Limited to a configurable maximum depth

### 4. Class Method Relationships (run_4.py)
Creates a comprehensive view of class method interactions:
```python
# Example analyzing an entire class
target_class = codebase.get_class("_Client")
```
- Shows all methods within a class
- Maps relationships between class methods
- Tracks external function calls
- Creates a hierarchical visualization of method dependencies

## Common Features

All visualizations share these characteristics:

1. **Configurable Depth**
   - MAX_DEPTH setting controls recursion
   - Prevents infinite loops in circular references

2. **Color Coding**
   ```python
   COLOR_PALETTE = {
       "StartFunction": "#9cdcfe",  # Entry point
       "PyFunction": "#a277ff",     # Regular functions
       "PyClass": "#ffca85",        # Classes
       "ExternalModule": "#f694ff"  # External calls
   }
   ```

3. **Edge Metadata**
   - Tracks file paths
   - Records source locations
   - Maintains call relationships

## Running the Visualizations

```bash
# Install dependencies
pip install codegen networkx

# Run any visualization script
python run_1.py  # Function call relationships
python run_2.py  # Symbol dependencies
python run_3.py  # Function blast radius
python run_4.py  # Class method relationships
```

Each script will:
1. Initialize the codebase
2. Create the appropriate graph
3. Generate visualization data
4. Output the graph for viewing in codegen.sh

## Customization Options

Each visualization can be customized through global settings:

```python
IGNORE_EXTERNAL_MODULE_CALLS = True/False  # Filter external calls
IGNORE_CLASS_CALLS = True/False           # Filter class references
MAX_DEPTH = 10                           # Control recursion depth
```

## View Results

After running any script, use codegen.sh to view the interactive visualization of the generated graph.

## Contributing

Feel free to submit issues and enhancement requests to improve these visualizations!
