# global variables

#Write a function to accept two strings (username and a password) and return a single string (SQL) representing the query used to determine if a user is authenticated on a given system.
def genTautologyQuery(usrname, passwd):
    query = (
        "SELECT authenticate\n"
        "FROM passwordList\n"
        "WHERE name='$" + usrname + "' and passwd='$" + passwd + "'\n\n"
    )
    return query
def genCommentQuery(usrname, passwd):
    query = (
        "SELECT authenticate\n"
        "FROM passwordList\n"
        "WHERE name='" + usrname + "'; -- and passwd='" + passwd + "';\n\n"
    )
    return query

#Generate a set of cases (one for each member of your team) that represent valid input where the username and the password consist of letters, numbers, and underscores.
testValid = [
    {
        "username": "caitlin",
        "password": "caldwell_is_kewl123", },
    {
        "username": "grant",
        "password": "jonesing_4_code", },
    {
        "username": "celeste",
        "password": "bangingmyheadona_wahl78", },
    {
        "username": "jeremy",
        "password": "sander_man67", }
]

def main():
    print("---------------------Tautology Queries---------------------\n")
    for test in testValid:
        print(genTautologyQuery(test["username"], test["password"]))
    print("---------------------Comment Queries---------------------\n")
    for test in testValid:
        print(genCommentQuery(test["username"], test["password"]))

if __name__ == "__main__":
    main()