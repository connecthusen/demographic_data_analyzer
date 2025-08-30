import pandas as pd

def calculate_demographic_data(print_data=True):
    # Column names
    column_names = [
        "age", "workclass", "fnlwgt", "education", "education-num",
        "marital-status", "occupation", "relationship", "race",
        "sex", "capital-gain", "capital-loss", "hours-per-week",
        "native-country", "salary"
    ]

    # Load dataset with raw string for regex separator
    df = pd.read_csv("adult.data.data", header=None, names=column_names, sep=r',', engine='python')

    # Clean missing values
    df = df.replace('?', pd.NA)

    # 1. Count of each race
    race_count = df['race'].value_counts()

    # 2. Average age of men
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3. Percentage with Bachelors
    percentage_bachelors = round((df['education'] == 'Bachelors').mean() * 100, 1)

    # 4. Higher vs lower education rich
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    lower_education = ~higher_education

    higher_edu_rich = df[higher_education & (df['salary'] == '>50K')]
    lower_edu_rich = df[lower_education & (df['salary'] == '>50K')]

    higher_education_rich = round(len(higher_edu_rich) / len(df[higher_education]) * 100, 1) if len(df[higher_education]) > 0 else 0
    lower_education_rich = round(len(lower_edu_rich) / len(df[lower_education]) * 100, 1) if len(df[lower_education]) > 0 else 0

    # 5. Min work hours
    min_work_hours = df['hours-per-week'].min()

    # 6. Percentage rich among those who work min hours
    min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_min_workers = min_workers[min_workers['salary'] == '>50K']
    rich_percentage = round(len(rich_min_workers) / len(min_workers) * 100, 1) if len(min_workers) > 0 else 0

    # 7. Country with highest percentage of rich
    country_counts = df['native-country'].value_counts()
    rich_country_counts = df[df['salary'] == '>50K']['native-country'].value_counts()
    country_earnings = (rich_country_counts / country_counts * 100).dropna()
    if not country_earnings.empty:
        highest_earning_country = country_earnings.idxmax()
        highest_earning_country_percentage = round(country_earnings.max(), 1)
    else:
        highest_earning_country = None
        highest_earning_country_percentage = 0

    # 8. Top occupation in India earning >50K
    india_rich = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation']
    top_IN_occupation = india_rich.value_counts().idxmax() if not india_rich.empty else None

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print("Min work hours per week:", min_work_hours)
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupation in India among those earning >50K:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }