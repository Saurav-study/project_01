
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================
# 1. PROJECT SETUP
# ==========================================

OUTPUT_DIR = Path("charts")
OUTPUT_DIR.mkdir(exist_ok=True)

url = "https://raw.githubusercontent.com/fralfaro/MAT281/main/docs/labs/data/netflix_titles.csv"

df = pd.read_csv(url)

print("\n" + "=" * 45)
print("       NETFLIX DATA ANALYTICS")
print("=" * 45)
print(f"\nDataset loaded: {df.shape[0]:,} rows")
print(f"Total columns: {df.shape[1]}")

# ==========================================
# 2. PROFESSIONAL THEME
# ==========================================

BACKGROUND = "#181818"
RED = "#E50914"
BLUE = "#5DADE2"
GREY = "#B3B3B3"
GRID = "#555555"

plt.rcParams["figure.facecolor"] = BACKGROUND
plt.rcParams["axes.facecolor"] = BACKGROUND
plt.rcParams["axes.labelcolor"] = "#E5E5E5"
plt.rcParams["text.color"] = "#FFFFFF"
plt.rcParams["xtick.color"] = GREY
plt.rcParams["ytick.color"] = GREY
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.titlesize"] = 16
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.left"] = False
plt.rcParams["axes.edgecolor"] = GRID
plt.rcParams["savefig.facecolor"] = BACKGROUND

def save_chart(filename):
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=300,
        bbox_inches="tight",
        facecolor=BACKGROUND
    )
    plt.show()
    plt.close()


# ==========================================
# 3. DATASET EXPLORATION
# ==========================================

print("\nDATASET OVERVIEW")
print("-" * 45)

print("\nFirst five records:")
print(df.head().to_string(index=False))

print("\nColumn information:")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\nMissing values:")
print(df.isnull().sum().to_string())

print(f"\nDuplicate records: {df.duplicated().sum():,}")

print("\nContent type summary:")
print(df["type"].value_counts().to_string())


# ==========================================
# 4. DATA CLEANING
# ==========================================

df.drop_duplicates(inplace=True)

text_columns = [
    "director", "cast", "country",
    "rating", "duration", "listed_in", "description"
]

for column in text_columns:
    if column in df.columns:
        df[column] = df[column].fillna("Unknown")

df["date_added"] = pd.to_datetime(
    df["date_added"].astype("string").str.strip(),
    errors="coerce"
)

df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month

print("\nDATA CLEANING")
print("-" * 45)
print(f"Rows after removing duplicates: {len(df):,}")
print("Cleaning completed successfully.")


# ==========================================
# 5. CONTENT TYPE DISTRIBUTION
# ==========================================

content_counts = df["type"].value_counts()

plt.figure(figsize=(8, 5))

bars = plt.bar(
    content_counts.index,
    content_counts.values,
    color=[RED, BLUE],
    width=0.5
)

plt.title("Netflix Content Distribution", pad=18)
plt.xlabel("Content Type")
plt.ylabel("Number of Titles")
plt.grid(axis="y", color=GRID, linestyle="--", alpha=0.25)
plt.gca().set_axisbelow(True)

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{int(height):,}",
        ha="center",
        va="bottom",
        fontsize=10
    )

save_chart("01_content_distribution.png")


# ==========================================
# 6. CONTENT RELEASES BY YEAR
# ==========================================

year_counts = df["release_year"].value_counts().sort_index()
year_counts = year_counts[year_counts.index >= 2000]

plt.figure(figsize=(11, 5))

plt.plot(
    year_counts.index,
    year_counts.values,
    color=RED,
    linewidth=2.2,
    marker="o",
    markersize=3
)

plt.title("Netflix Titles by Release Year", pad=18)
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.grid(axis="y", color=GRID, linestyle="--", alpha=0.25)
plt.gca().set_axisbelow(True)

save_chart("02_releases_by_year.png")


# ==========================================
# 7. TOP 10 COUNTRIES
# ==========================================

country_data = (
    df[df["country"] != "Unknown"]["country"]
    .str.split(", ")
    .explode()
)

top_countries = country_data.value_counts().head(10).sort_values()

plt.figure(figsize=(10, 6))

plt.barh(
    top_countries.index,
    top_countries.values,
    color=RED,
    height=0.65
)

plt.title("Top 10 Countries by Netflix Titles", pad=18)
plt.xlabel("Number of Titles")
plt.ylabel("")
plt.grid(axis="x", color=GRID, linestyle="--", alpha=0.25)
plt.gca().set_axisbelow(True)

save_chart("03_top_countries.png")


# ==========================================
# 8. TOP 10 GENRES
# ==========================================

genre_data = (
    df[df["listed_in"] != "Unknown"]["listed_in"]
    .str.split(", ")
    .explode()
)

top_genres = genre_data.value_counts().head(10).sort_values()

plt.figure(figsize=(10, 6))

plt.barh(
    top_genres.index,
    top_genres.values,
    color=BLUE,
    height=0.65
)

plt.title("Top 10 Netflix Genres", pad=18)
plt.xlabel("Number of Titles")
plt.ylabel("")
plt.grid(axis="x", color=GRID, linestyle="--", alpha=0.25)
plt.gca().set_axisbelow(True)

save_chart("04_top_genres.png")


# ==========================================
# 9. CONTENT ADDED BY YEAR
# ==========================================

added_years = df["year_added"].dropna().astype(int)
added_counts = added_years.value_counts().sort_index()

plt.figure(figsize=(11, 5))

plt.bar(
    added_counts.index,
    added_counts.values,
    color=RED,
    width=0.7
)

plt.title("Netflix Content Added by Year", pad=18)
plt.xlabel("Year Added")
plt.ylabel("Number of Titles")
plt.grid(axis="y", color=GRID, linestyle="--", alpha=0.25)
plt.gca().set_axisbelow(True)

save_chart("05_content_added_by_year.png")


# ==========================================
# 10. MOVIE DURATION DISTRIBUTION
# ==========================================

movies = df[df["type"] == "Movie"].copy()

movies["duration_minutes"] = pd.to_numeric(
    movies["duration"].str.extract(r"(\d+)")[0],
    errors="coerce"
)

movie_duration = movies["duration_minutes"].dropna()

plt.figure(figsize=(10, 5))

plt.hist(
    movie_duration,
    bins=25,
    color=RED,
    edgecolor=BACKGROUND,
    alpha=0.95
)

plt.title("Distribution of Movie Durations", pad=18)
plt.xlabel("Duration (Minutes)")
plt.ylabel("Number of Movies")
plt.grid(axis="y", color=GRID, linestyle="--", alpha=0.25)
plt.gca().set_axisbelow(True)

save_chart("06_movie_duration.png")


# ==========================================
# 11. TV SHOW SEASON DISTRIBUTION
# ==========================================

tv_shows = df[df["type"] == "TV Show"].copy()

tv_shows["seasons"] = pd.to_numeric(
    tv_shows["duration"].str.extract(r"(\d+)")[0],
    errors="coerce"
)

season_counts = tv_shows["seasons"].dropna().value_counts().sort_index()

plt.figure(figsize=(9, 5))

plt.bar(
    season_counts.index.astype(int).astype(str),
    season_counts.values,
    color=BLUE,
    width=0.65
)

plt.title("TV Show Season Distribution", pad=18)
plt.xlabel("Number of Seasons")
plt.ylabel("Number of TV Shows")
plt.grid(axis="y", color=GRID, linestyle="--", alpha=0.25)
plt.gca().set_axisbelow(True)

save_chart("07_tv_show_seasons.png")


# ==========================================
# 12. CONTENT RATINGS
# ==========================================

rating_counts = (
    df[df["rating"] != "Unknown"]["rating"]
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

plt.barh(
    rating_counts.index,
    rating_counts.values,
    color=RED,
    height=0.65
)

plt.title("Most Common Netflix Content Ratings", pad=18)
plt.xlabel("Number of Titles")
plt.ylabel("")
plt.grid(axis="x", color=GRID, linestyle="--", alpha=0.25)
plt.gca().set_axisbelow(True)

save_chart("08_ratings_distribution.png")


# ==========================================
# 13. KEY INSIGHTS
# ==========================================

print("\n" + "=" * 45)
print("             PROJECT INSIGHTS")
print("=" * 45)

if not content_counts.empty:
    print(f"\nMost common content: {content_counts.idxmax()}")

if not top_countries.empty:
    print(f"Leading country: {top_countries.idxmax()}")

if not top_genres.empty:
    print(f"Popular genre: {top_genres.idxmax()}")

if not movie_duration.empty:
    print(f"Average movie duration: {movie_duration.mean():.1f} minutes")

if not added_counts.empty:
    print(f"Peak year for content additions: {added_counts.idxmax()}")

print("\n" + "-" * 45)
print(f"Charts saved in: {OUTPUT_DIR.resolve()}")
print("Analysis completed successfully!")
print("=" * 45)
