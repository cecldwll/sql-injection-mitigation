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


if __name__ == "__main__":
    # entry point for testing
    run_valid_input_tests()
