# Write a program that converts a Roman numeral to an integer
def roman_to_int(s: str) -> int:
    roman_numerals = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    total = 0
    prev_value = 0
    
    for char in reversed(s):
        value = roman_numerals[char]
        
        if value < prev_value:
            total -= value
        else:
            total += value
            
        prev_value = value
        
    return total


# Example usage
if __name__ == "__main__":
    roman_numeral = "XIV"
    integer_value = roman_to_int(roman_numeral)
    print(f"The integer value of the Roman numeral {roman_numeral} is {integer_value}.")    



# Write a program that calculates the factorial of a number
def factorial(n: int) -> int:
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Example usage
if __name__ == "__main__":
    num = 5
    result = factorial(num)
    print(f"The factorial of {num} is {result}.")


# Write a program that generates a blog
def generate_blog(title: str, content: str) -> str:
    blog_template = f"""
    <html>
    <head>
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        <p>{content}</p>
    </body>
    </html>
    """
    return blog_template

# Example usage
if __name__ == "__main__":
    blog_title = "My First Blog"
    blog_content = "This is the content of my first blog post."
    blog_html = generate_blog(blog_title, blog_content)
    print(blog_html)

