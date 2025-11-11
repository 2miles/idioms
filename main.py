from connectors.supabase import get_idioms_missing_definitions


def main():
    idioms = get_idioms_missing_definitions(limit=10)
    if idioms:
        print(f"Retrieved {len(idioms)} idioms with no definition:\n")
        for row in idioms:
            print(f"{row['id']:>4}  {row['idiom']}")
    else:
        print("No idioms without definitions found!")


if __name__ == "__main__":
    main()
