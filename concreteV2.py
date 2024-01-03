import numpy as np
import pandas as pd
import re
from scipy.interpolate import interp1d


def main():
    """
    Main function that runs the program
    """

    print("\n", end="")
    print("\t\t\t\tAnalysis of Compressive Strength Test Results")
    print("\n", end="")

    # Get test results
    result_list = get_results()

    for result in result_list:
        id = list(result.keys())
        values = (list(result.values()))[0]
        age, cement_type, _, characteristic_strength = values

        # Predict characteristics at 28 days
        predicted_characteristic_strength = predict(
            characteristic_strength, age, cement_type
        )

        # Generate and print summary table
        pandas_summary = get_summary(*id, *values, predicted_characteristic_strength)

        print(pandas_summary)
        print("\n", end="")


def get_results():
    """
    Function to get results of the compressive strength tests from the user
    """
    result_list = []
    while True:
        id = input("Test ID/Location: ")
        print("\n", end="")
        try:
            while True:
                try:
                    print("Compressive Strength Test Results (MPa)")
                    results = input("Enter comma-separated values: ")

                    if matches := re.search(
                        r"^\d+\.?\d+,\d+\.?\d+,\d+\.?\d+$", results
                    ):
                        results = [float(result) for result in results.split(",")]
                        print("\n", end="")
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Check that results are entered correctly e.g 23,24,25")

            while True:
                try:
                    print("Age of Concrete Cubes (days)")
                    age = int(input("Enter single value: "))
                    print("\n", end="")
                    break
                except ValueError:
                    print("Check that age is entered correctly e.g 23")

            while True:
                try:
                    print("Cement Type (N, R, or S)")
                    cement_type = input("Input Cement Type: ")

                    if cement_type in ["N", "R", "S"]:
                        mean_strength = round(np.mean(results), 2)
                        characteristic_strength = round((mean_strength - 4), 2)
                        result_dict = {
                            id: [
                                age,
                                cement_type,
                                mean_strength,
                                characteristic_strength,
                            ]
                        }
                        result_list.append(result_dict)

                        print("\n", end="")
                        input(
                            "Press ENTER to add more results or CTRL + Z to compute: "
                        )
                        print("\n", end="")
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Check that cement type is entered correctly e.g N")
        except EOFError:
            break

    return result_list


def get_summary(
    id,
    age,
    cement_type,
    mean_strength,
    characteristic_strength,
    predicted_characteristic_strength,
):
    """
    Function to create a dataframe holding the concrete tests analysis
    """

    data = {
        "ID": id,
        "Age": age,
        "Cement Type": cement_type,
        "Mean Strength": mean_strength,
        "Characteristic Strength": characteristic_strength,
        "Predicted 28-day Strength": predicted_characteristic_strength,
    }
    pandas_summary = pd.DataFrame(data, index=[1])

    return pandas_summary


def predict(characteristic_strength, age, cement_type):
    """
    Function to predict the characteristic strength of concrete cubes at 28 days.

    params:
        - characteristic_strength: Characteristic strength (pre-calculated from the average value of the 3 sample cubes)
        - age: Age of the cubes
        - cement_type: R,N,S defined below;
        cement of strength classes CEM 42.5R, CEM 52.5N and CEM 52.5R (Class R)
        cement of strength classes CEM 32.5R, CEM 42.5N (Class N)
        cement of strength classes CEM 32.5N (Class S)

    returns:
        - predicted characteristic_strength of the concrete cube samples at 28 days
    """

    # Coefficients and following calculations are based on BS EN 1992-1-1, sub-clause 3.1.2(6);
    #  0.20 for cement of characteristic_strength classes CEM 42.5R, CEM 52.5N and CEM 52.5R (Class R)
    #  0.25 for cement of characteristic_strength classes CEM 32.5R, CEM 42.5N (Class N)
    #  0.38 for cement of characteristic_strength classes CEM 32.5N (Class S)
    s = [0.2, 0.25, 0.38]

    # Time array from 0 to 28 days
    t = np.linspace(1, 28, 28)

    # Strength proportion achieved in time t
    proportions = {}

    # Characteristic_strength proportion achieved in time t, saved in a dictionary with each coeff as key
    for coeff in s:
        proportion_characteristic_strength_gained_per_day = list(
            np.exp(coeff * (1 - (np.sqrt(28 / t))))
        )
        proportions[coeff] = proportion_characteristic_strength_gained_per_day

    # Create dataframes holding data for R, N and S classes
    R = {
        "Days": t,
        "Proportion of 28-day characteristic_strength": proportions[0.2],
    }
    N = {
        "Days": t,
        "Proportion of 28-day characteristic_strength": proportions[0.25],
    }
    S = {
        "Days": t,
        "Proportion of 28-day characteristic_strength": proportions[0.38],
    }

    R = pd.DataFrame(R)
    N = pd.DataFrame(N)
    S = pd.DataFrame(S)

    if cement_type == "R":
        selected_cement = R
    elif cement_type == "N":
        selected_cement = N
    elif cement_type == "S":
        selected_cement = S

    # Interpolate the 28 day characteristic_strength proportion of the concrete cubes for a given age
    x = selected_cement["Days"]
    y = selected_cement["Proportion of 28-day characteristic_strength"]

    f = interp1d(x, y, kind="linear")
    predicted_proportion = f(age)

    # Calculate the predicted concrete characteristic_strength of the sample cubes at 28 days
    predicted_characteristic_strength = round(
        (characteristic_strength / predicted_proportion), 2
    )

    return predicted_characteristic_strength


if __name__ == "__main__":
    main()
