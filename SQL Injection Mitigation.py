

import re


# simulate vulnerable login system 
def generate_auth_query(username, password):
    # build sql query using direct string concatenation
    # intentionally vulnerable to injection 
    query = (
        "SELECT * FROM users "
        "WHERE username = '" + username + "' "
        "AND password = '" + password + "';"
    )
    return query


def get_valid_test_cases():
    # inputs: letters, numbers, underscores only
    return [
        ("caitlyn_user", "password_123"),
        ("celeste_w", "secure_pass1"),
        ("jeremy_s", "login_456"),
        ("grant_jones", "pass_word_789")
    ]


def run_valid_input_tests():
    # run all valid test cases
    print("running input test cases:\n")

    # taking username & password as strings --> inserting them into query
    for username, password in get_valid_test_cases():
        query = generate_auth_query(username, password)
        print("username:", username)
        print("password:", password)
        print("generated sql query:")
        print(query)
        print()

#-------------------------------------------------------------------------------

#Write a function to accept two strings (username and a password) and return a single string (SQL) representing the query used to determine if a user is authenticated on a given system.
def genTautologyCommentQuery(usrname, passwd):
    query = (
        "SELECT authenticate\n"
        "FROM passwordList\n"
        "WHERE name='$" + usrname + "' and passwd='$" + passwd + "'"
    )
    return query
def TautologyAttacks():
    tautology_attack = [
        "OR '1'='1'\nFROM passwordList;",
        "OR 'x'='x'\nFROM passwordList;",
        "OR 'admin'='admin'",
        "OR 'x'='x'"
    ]
    for user in testValid:
        username = user["username"]
        password = user["password"]
        query = genTautologyCommentQuery(username, password)
        for attack in tautology_attack:
            new_query = query + attack
            print(new_query)

        print()
def genCommentQuery(usrname, passwd):
    query = (
        "SELECT authenticate\n"
        "FROM passwordList\n"
        "WHERE name='" + usrname + "'; -- and passwd='" + passwd + "';\n\n"
    )
    return query
def CommentAttacks():
    comment_attack = [
        "-- ",
        "-- username"
        "'; -- and passwd='"
        "'; -- and passwd='passwd'"
    ]
    for user in testValid:
        username = user["username"]
        password = user["password"]
        query = genCommentQuery(username, password)

        for attack in comment_attack:
            new_query = query.replace(
                f"name='{username}'",
                f"name='{username}' {attack}"
            )
            print(new_query)

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


#----------------------------------------------------------------------------


def generate_auth_query(username, password):
    # build sql query using direct string concatenation
    # intentionally vulnerable to injection
    query = (
        "SELECT * FROM users "
        "WHERE username = '" + username + "' "
        "AND password = '" + password + "';"
    )
    return query


def get_valid_test_cases():
    # inputs: letters, numbers, underscores only
    return [
        ("caitlyn_user", "password_123"),
        ("celeste_w", "secure_pass1"),
        ("jeremy_s", "login_456"),
        ("grant_jones", "pass_word_789")
    ]


def run_valid_input_tests():
    # run all valid test cases
    print("running input test cases:\n")

    # taking username & password as strings --> inserting them into query
    for username, password in get_valid_test_cases():
        query = generate_auth_query(username, password)
        print("username:", username)
        print("password:", password)
        print("generated sql query:")
        print(query)
        print()


def Union_Attacks():
    """
    Gets test cases from get_valid_test_cases() and injects Union
    attacks into the output strings.
    """
    test_cases = get_valid_test_cases()

    attacks = [
        " UNION SELECT username,password FROM users;",
        " UNION SELECT username,password FROM users LIMIT 1;",
        " UNION SELECT 'admin','password123';",
        " UNION SELECT authenticate FROM passwordList;"
    ]
    
    for username, password in test_cases:
        sql_query = generate_auth_query(username, password)
        mod = sql_query.replace(";", "")

        for attack in attacks:
            new_query = mod + attack
            print(new_query)
        
        print()


def Add_Statement_Attacks():
    """
    Gets test cases from get_valid_test_cases() and injects Additional Statement
    attacks into the output strings.
    """
    test_cases = get_valid_test_cases()

    attacks = [
               " INSERT INTO passwordList (name, password) VALUES ('nefarious', 'malicious123');",
               " SELECT username,password FROM users;",
               " DELETE FROM users;",
               " DROP TABLE users;"
               ]
    
    for username, password in test_cases:
        sql_query = generate_auth_query(username, password)

        for attack in attacks:
            new_query = sql_query + attack
            print(new_query)
        
        print()







#-------------------------------------------------------------------------------
# WEAK Sanitize
def weak_sanitize_input(user_input):
    """
    Weak mitigation against common SQL injection attacks.
    Attempts to remove dangerous keywords, comments, and special characters.
    """

    # Remove common SQL keywords (case-insensitive) for UNION ATTACK and TAUTOLOGY
    dangerous_keywords = [
        "UNION", "SELECT", "DROP", "INSERT",
        "DELETE", "UPDATE", "OR", "AND"
    ]

    for keyword in dangerous_keywords:
        pattern = re.compile(keyword, re.IGNORECASE)
        user_input = pattern.sub("", user_input)

    # Remove all non-alphanumeric characters
    # For TAUTOLOGY, COMMENT, and ADDITIONAL STATEMENT
    # We remove symbols such as ' ; - 
    # This way we can't concat or comment
    user_input = re.sub(r"[^a-zA-Z0-9]", "", user_input) 
    return user_input

#  TEST WEAK
def test_weak_sanitize_input():
    print("\n")
    tests = [
    "admin' OR '1'='1'",                         # TAUTOLOGY
    "admin' --",                                # COMMENT
    "'; DROP TABLE users; --",                  # ADDITIONAL STATEMENT
    "admin UNION SELECT password FROM users"    # UNION
    ]

    for test in tests:
        print("Original:", test)
        print("Sanitized:", weak_sanitize_input(test))
        print("-" * 40)



# STRONG Sanitize
def strong_authenticated_query(username, password):
    """
    Strong mitigation simulation.
    Removing SQL from the workflow.
    """
    # INPUT from the user will be treated as a string, having removed SQL from the workflow
    query = "SELECT * FROM users WHERE username = ? AND password = ?;"
    parameters = (username, password)

    return query, parameters

# TEST STRONG
def test_strong_query():
    # Malicious inputs
    malicious_inputs = [
        "admin' OR '1'='1",
        "admin' --",
        "'; DROP TABLE users; --",
        "admin UNION SELECT password FROM users"
    ]
    print("=== Testing Malicious Inputs ===")
    for user_input in malicious_inputs:
        query, params = strong_authenticated_query(user_input, "any_password")
        print("Input:", user_input)
        print("Query:", query)
        print("Parameters:", params)
        print("-"*40)

    # Valid inputs
    valid_inputs = [
        ("alice", "password123"),
        ("bob_smith", "P@ssw0rd!")
    ]
    print("\n=== Testing Valid Inputs ===")
    for username, password in valid_inputs:
        query, params = strong_authenticated_query(username, password)
        print("Username:", username, "Password:", password)
        print("Query:", query)
        print("Parameters:", params)
        print("-"*40)



#----------------------------------------------------------------


# MAIN 
def main():

    choice = 0
    while (choice != 7):
        print("\n")
        print("""
Hello and welcome to SQL Injection Mitigation

Select 1-6 to choose the demostration. 
1. Valid Test Cases
2. Tautology Attack Test Cases
3. Comment Attack Test Cases
4. UNION
5. Weak Mitigation
6. Strong Mitigation
7. Exit
""")       
        
        choice = int(input("Enter choice (1-7): "))
        print("\n")

        match choice:
            case 1:
                print("---------------------Valid Inputs---------------------\n")
                run_valid_input_tests()
            
            case 2:
                print("---------------------Tautology Queries---------------------\n")
                for test in testValid:
                    TautologyAttacks()
            
            case 3:     
                print("---------------------Comment Queries---------------------\n")
                CommentAttacks()

            case 4:
                print("-------------------Union Attacks----------------------------")
                Union_Attacks()
            
            case 5:
                print("-------------------Weak Mitigation----------------------------")
                test_weak_sanitize_input()

            case 6:
                print("-------------------Strong Mitigation----------------------------")
                test_strong_query()

            case 7:
                print("Exiting...")
                break


# RUN CODE
if __name__ == '__main__':
    main()
