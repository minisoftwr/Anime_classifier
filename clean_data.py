import pandas as pd
import csv


def clean_anime():
    file_path = "anime_classifier/myanilist.csv"
    rows = []
    skipped = 0

    with open(file_path,"r",encoding="utf-8",newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            #Header
            if row[0] == "ID":
                rows.append(row)
                continue
            #Normal row
            if len(row) == 21:
                rows.append(row)
            # Rows containing an extra comma
            else:
                skipped += 1
    print(f"Rows skipped for wrong length : {skipped}")
    #Create dataframe
    df = pd.DataFrame(
        rows[1:],
        columns=rows[0]
    )
  
    df = df.drop_duplicates(subset=["ID"])
    df = df.dropna(subset=["Title_Romaji"])


    #the text columns
    text_col= ["Title_Romaji","Title_English","Type","Genres","Studios"]

    # cleaning the Text columns   
    for col in text_col:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")
            df[col] = df[col].astype("string").str.strip()
    #Ensure the follwing columns are numerical
    num_col =["ID","Episodes","Average_Score","Mean_Score"]


    # Cleaning the  numerical columns
    for col in num_col:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col],errors="coerce")
        
    df.loc[df["Episodes"] <= 0, "Episodes"] = pd.NA 

    for col in ["Average_Score","Mean_Score"]:
        df.loc[~df[col].between(0,100),col] = pd.NA
    # clean date using datetime()
    for col in ["Start","End"]:
        df[col] = df[col].replace("None-None-None",pd.NA)
        df[col] = pd.to_datetime(df[col],errors="coerce")

    # Resitng the old index number to the new one 
    df = df.reset_index(drop=True)
    necessary_columns = [
        "ID","Title_Romaji","Title_English","Type","Genres","Studios"
    ]
    df = df[necessary_columns]
    return df

if __name__ == "__main__":
    print(" Data Cleaning")
    anime = clean_anime()
    print("\nFinal Columns:")
    print(anime.columns.tolist())
    anime.to_csv("anime_classifier/cleaned_anime.csv",index=False)
    print("The Cleaned Data is saved as cleaned_anime")





     


