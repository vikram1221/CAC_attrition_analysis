import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Manually recorded odds ratios from your runs
    data = {
        'feature': [
            'team_size',
            'reg_month',
            'reg_dow',
            'median_income',
            'rural_proxy',
        ],

        'Baseline': [
            0.61,
            1.95,
            1.22,
            None, 
            None,
        ], 

        'Census_Adjusted': [
            0.67,
            1.68,
            1.20,
            0.61,
            0.83,
        ],
    }

    df = pd.DataFrame(data)

    # Drop features not present in baseline
    plot_df = df.set_index('feature')

    fig, ax = plt.subplots(figsize=(8, 5))

    plot_df.plot.barh(ax=ax)

    # Reference line at no-effect
    ax.axvline(1.0)

    ax.set_xlabel('Odds Ratio')
    ax.set_title('Attrition Odds Ratios: Baseline vs Census-Adjusted Models')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()