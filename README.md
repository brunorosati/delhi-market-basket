# Price and basket, more than foot traffic

What explains revenue differences across 27 brands at one Delhi market. Bruno Fajardo Rosati, October 2026.

**Question.** At a market organized by TETR College of Business in Vasant Kunj, New Delhi, on 12 April 2026, did the revenue ranking of 27 brands come from more customers, more units per customer, or a higher price per unit?

**Answer.** Price per unit carries 51 percent of the cross-brand variance in log revenue, customer count 25 percent and units per customer 24 percent. The basket share comes almost entirely from one brand, Montrega, the fragrance brand I co-founded: it ranked first with the median number of customers (16) and 6.1 bottles per customer, four times its basket at the other market it won. With 27 brands and one evening of trading, these numbers describe one market and identify no cause.

The full note, with figures, robustness checks and limits: [`note/data_note.pdf`](note/data_note.pdf).

## Files

| Path | Contents |
|---|---|
| `data/source/` | The two leaderboard images as published by the organizer. |
| `data/market_data.csv` | Both leaderboards as printed: 27 brands at Vasant Kunj (22:00, 12 April 2026) and 18 at Galleria Market (21:00, date not printed). Customers, units, revenue in INR. `brand_id` links the same brand across the two markets. |
| `analysis.ipynb` | Every number in the note: data checks, Table 1 (variance shares, Spearman), leave-one-out and bootstrap, Table 2, and the checks in Section 5. |
| `figures.py` | Figures 1 and 2. |
| `output/results.json` | Table values written by the notebook. |
| `note/` | The note in PDF and its LaTeX source. |

## Method in three lines

Revenue = customers × units per customer × price per unit. In logs the product becomes a sum, so the variance of log revenue across brands splits into three covariances. Each part's share is cov(ln part, ln revenue) / var(ln revenue), the slope from regressing the log part on log revenue, and the three shares add to one (the same split trade economists use for export margins: Hummels and Klenow 2005; Bernard et al. 2009).

## Reproduce

```
pip install pandas numpy scipy matplotlib jupyter
jupyter nbconvert --to notebook --execute analysis.ipynb --output analysis.ipynb
python figures.py
cd note && pdflatex data_note.tex
```

## Data notes

- I typed both leaderboards by hand from the images in `data/source/` and checked every row against them.
- The total printed on the Vasant Kunj leaderboard (534 customers, 1,067 units, INR 516,029) is the sum of ranks 1 to 26; it leaves out Bumba, ranked 27th. All results use the 27 brands.
- The organizer did not publish how it counted unique customers.
- Four brand names differ between the two leaderboards in capitalization or spelling; `brand_id` treats each pair as one brand.

## Tools

Python (pandas, NumPy, SciPy, matplotlib) and LaTeX. I used an AI coding assistant while writing the code and checked every number against the source leaderboards.

Contact: brunofajardorosati@gmail.com
