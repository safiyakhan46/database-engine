from database import Database


def main():

    db = Database()

    print("=" * 45)
    print(" Mini Database Engine")
    print(" Type EXIT to quit.")
    print("=" * 45)

    while True:

        sql = input("\ndb> ").strip()

        if not sql:
            continue

        if sql.upper() == "EXIT":
            break

        try:

            result = db.execute(sql)

            if result is not None:

                if isinstance(result, list):

                    if len(result) == 0:
                        print("No rows found.")
                    else:

                        for row in result:
                            print(row)

                else:
                    print(result)

            else:
                print("OK")

        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    main()