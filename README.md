### Concrete Strength Prediction

This Python script predicts the strength of concrete cubes at 28 days given certain parameters of the concrete at a given age. Calculations are made using the BS EN 1992-1-1 standard. It takes into account the characteristic strength, age of the cubes, and the type of cement used.

### Usage:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Install Dependencies:**
   Ensure you have the required dependencies installed by running:
   ```bash
   pip install numpy pandas seaborn matplotlib
   ```

3. **Run the Script:**
   Open the script in a Jupyter Notebook or any Python environment and execute the code.

   ```python
   # Enter cube test results
   results = [38.76, 27.89, 25.42]

   mean = np.mean(results)
   characteristic_strength = mean - 4
   age = 26
   cement_type = "N"

   # Predict 28-day strength and print output
   expected_strength = predict(characteristic_strength, age, cement_type)[1]

   data = {
       "Age": age,
       "Mean Strength (Mpa)": round(mean, 2),
       "Characteristic Strength (Mpa)": round(characteristic_strength, 2),
       "Expected Strength at 28 days (Mpa)": round(expected_strength, 2),
   }
   table_of_results = pd.DataFrame(data, index=[1])

   table_of_results
   ```

##### Parameters:

- **`results`**: List of cube test results.
- **`mean`**: Mean strength calculated from test results.
- **`characteristic_strength`**: Characteristic strength calculated from the mean.
- **`age`**: Age of the concrete cubes.
- **`cement_type`**: Type of cement used (choose from "R", "N", or "S").

##### Output:

The script will output a table with information including age, mean strength, characteristic strength, and the expected strength of the cubes at 28 days.