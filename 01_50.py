# %% [markdown]
# # Project Euler

# %%
from collections.abc import Callable
from datetime import date
from functools import cache, reduce
from io import StringIO
from itertools import combinations
from math import comb, gcd, isqrt, lcm, prod, factorial

import numpy as np
import pandas as pd
import pyperclip

# from icecream import ic
# from IPython.display import Latex, Markdown, display
from more_itertools import sieve
from sympy import prevprime


def print_and_copy_answer(func: Callable):

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(result)
        pyperclip.copy(str(result))
        return result

    return wrapper


# %% [markdown]
# ## 1. Multiples of 3 or 5
#
# If we list all the natural numbers below 10 that are multiples of 3 or 5, we
# get 3, 5, 6 and 9. The sum of these multiples is 23.
#
# Find the sum of all the multiples of 3 or 5 below 1000.


# %%
def multiples_of_3_or_5(limit: int) -> int:
    print(f"The sum of multiples of 3 or 5 up to {limit}: ", end="")
    return sum(filter(lambda n: n % 3 == 0 or n % 5 == 0, range(limit)))


print(multiples_of_3_or_5(10))
print(multiples_of_3_or_5(1000))

# %% [markdown]
# ## 2. Even Fibonacci numbers
#
# Each new term in the Fibonacci sequence is generated by adding the previous
# two terms. By starting with 1 and 2, the first 10 terms will be:
#
# 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...
#
# By considering the terms in the Fibonacci sequence whose values do not exceed
# four million, find the sum of the even-valued terms.


# %%
def fibonacci_rec(n: int) -> int:
    if n in {0, 1}:
        return n
    return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)


def understandable(limit):
    fib = [1, 2]
    x = 0
    while x < limit:
        x = sum(fib[-2:])
        fib.append(x)

    return sum((n for n in fib if not n % 2))


def PE002(limit=4000000):
    a, b, S = 0, 2, 0
    while b <= limit:
        a, b, S = b, a + 4 * b, S + b
    return S


# %%
def understandable_faster(limit):
    a, b = 1, 2
    total = (
        2 if b <= limit else 0
    )  # Initialize with 2, as the first even Fibonacci number

    while True:
        a, b = b, a + b
        if b >= limit:
            break
        if b % 2 == 0:
            total += b

    return total


# %%
def PE002_optimized(limit=4000000):
    a, b, S = 2, 8, 2
    while b <= limit:
        S += b
        a, b = b, 4 * b + a
    return S


# %% [markdown]
# ## 3. Largest prime factor
#
# The prime factors of 13195 are 5, 7, 13 and 29.
#
# What is the largest prime factor of the number 600,851,475,143 ?


# %%
def is_prime(num: int) -> bool:
    if num < 2:
        return False
    square_root = isqrt(num)
    return all(num % i != 0 for i in range(2, square_root + 1))


def find_factor(n, g):
    x = 2  # starting value
    y = x
    d = 1

    while d == 1:
        x = g(x)
        y = g(g(y))
        d = gcd(abs(x - y), n)

    if d == n:
        return "failure"
    else:
        return d


# %%
find_factor(600851475143, lambda x: (x**2 + 1) % 600851475143)

# %%
find_factor(600851475143, lambda x: (x**2) % 600851475143)


# %%
def find_largest_prime_factor(n):
    p = (n**0.5) + 1
    while p > 2:
        p = prevprime(p)
        if n % p == 0:
            return p
    return n  # n is prime


# %% [markdown]
# ## 4. Largest Palindrome Product
#
# A palindromic number reads the same both ways. The largest palindrome made
# from the product of two 2-digit numbers is 9009 = 91 × 99
#
# Find the largest palindrome made from the product of two 3-digit numbers.


# %%
def largest_palindrome_product(number_digits: int = 2) -> int:
    number_range = range(10 ** (number_digits - 1), 10**number_digits)
    return max(
        a * b
        for a, b in combinations(number_range, 2)
        if (str_prod := str(a * b)) == str_prod[::-1]
    )


assert largest_palindrome_product(2) == 9009
largest_palindrome_product(3)


# %% [markdown]
# ## 5. Smallest Multiple
#
# 2520 is the smallest number that can be divided by each of the numbers from 1
# to 10 without any reminder.
#
# What is the smallest positive number that is **evenly divisible** by all of
# the numbers from 1 to 20?


# %%
@print_and_copy_answer
def smallest_multiple(limit: int) -> int:
    return lcm(*range(1, limit + 1))


assert smallest_multiple(10) == 2520, "Wrong! Answer should be 2520"

smallest_multiple(20)

# %% [markdown]
# ## 6. Sum Square Difference
#
# The sum of the squares of the first ten natural numbers is,
#
# 1² + 2² + ⋯ + 10² = 385
#
# The square of the sum of the first ten natural numbers is,
#
# (1 + 2 + ⋯ + 10)² = 55² = 3025
#
# Hence the difference between the sum of the squares of the first ten natural
# numbers and the square of the sum is 3025 - 385 = 2640.
#
# Find the difference between the sum of the squares of the first one hundred
# natural numbers and the square of the sum.


# %%
def sum_square_difference(limit: int) -> int:
    nums = range(1, limit + 1)
    return sum(nums) ** 2 - sum(n**2 for n in nums)


assert sum_square_difference(10) == 2640
sum_square_difference(100)
# %% [markdown]
# ## 7. 10001st Prime
#
# By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see
# that the 6th prime is 13.
#
# What is the 10001st prime number?


# %%
is_prime(13)


def generate_nth_prime_number(n: int) -> int:
    count = 0
    candidate = 2  # Starting from the first prime number
    while count < n:
        if is_prime(candidate):
            count += 1
            if count == n:
                return candidate
        candidate += 1


assert generate_nth_prime_number(6) == 13
generate_nth_prime_number(10001)

# %% [markdown]
# ## Largest Product in a Series
#
# The four adjacent digits in the 1000-digit number that have the greatest
# product are 9 × 9 × 8 × 9 = 5832.

# %%
thousand_digits = """73167176531330624919225119674426574742355349194934
96983520312774506326239578318016984801869478851843
85861560789112949495459501737958331952853208805511
12540698747158523863050715693290963295227443043557
66896648950445244523161731856403098711121722383113
62229893423380308135336276614282806444486645238749
30358907296290491560440772390713810515859307960866
70172427121883998797908792274921901699720888093776
65727333001053367881220235421809751254540594752243
52584907711670556013604839586446706324415722155397
53697817977846174064955149290862569321978468622482
83972241375657056057490261407972968652414535100474
82166370484403199890008895243450658541227588666881
16427171479924442928230863465674813919123162824586
17866458359124566529476545682848912883142607690042
24219022671055626321111109370544217506941658960408
07198403850962455444362981230987879927244284909188
84580156166097919133875499200524063689912560717606
05886116467109405077541002256983155200055935729725
71636269561882670428252483600823257530420752963450
"""
print(thousand_digits)

# %%


# %%
@print_and_copy_answer
# @test_case(4, 5832)
def largest_product_series(n: int) -> int:
    digit_sequence: str = thousand_digits
    digits_cleaned = digit_sequence.replace("\n", "")
    return max(
        prod(map(int, (digits_cleaned[i : i + n])))
        for i, _ in enumerate(digits_cleaned)
    )


# %%
def largest_product_series_gpt(n: int) -> int:
    # 4 times faster
    digit_sequence: str = thousand_digits
    digits_cleaned = digit_sequence.replace("\n", "")
    digits = [int(d) for d in digits_cleaned]

    max_product = 0
    current_product = prod(digits[:n])

    for i in range(n, len(digits)):
        if digits[i - n] != 0:  # Avoid division by zero
            current_product = (current_product // digits[i - n]) * digits[i]
        else:  # Recalculate product from scratch if a zero was present in the previous window
            current_product = prod(digits[i - n + 1 : i + 1])

        max_product = max(max_product, current_product)

    return max_product


# %% [markdown]
# ## Special Pythagorean Triplet
#
# A Pythagorean triplet is a set of three natural numbers, **a < b < c**, for
# which,
#
# **a² + b² = c²**,
#
# For example, **3² + 4² = 9 + 16 = 25 = 5²**
#
# There exists exactly one Pythagorean triplet for which **a + b + c = 1000**.
#
# Find the product **abc**.


# %%
@print_and_copy_answer
def pythagorean_triplet_sum_gpt(goal: int = 1000) -> int:
    for a in range(1, goal // 3):
        for b in range(a + 1, (goal - a) // 2):
            c = goal - a - b
            if a * a + b * b == c * c:
                return a * b * c


# %%
pythagorean_triplet_sum_gpt(1000)

# %% [markdown]
# ## 10. Summation of Primes
#
# The sum of the primes below **10** is **2 + 3 + 5 + 7 = 17**.
#
# Find the sum of all the primes below two million.


# %%
# @print_and_copy_answer
def primes_sum_to_limit(limit: int) -> int:
    return sum(x for x in range(limit) if is_prime(x))


# %%
# # %time primes_sum_to_limit(int(2e6))


# %%
def primes_to_limit_eratosthenes_sieve(n: int):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return (i for i in range(n + 1) if is_prime[i])


# %%
@print_and_copy_answer
def euler_10(limit: int) -> int:
    return sum(primes_to_limit_eratosthenes_sieve(limit))


# %%
sum(sieve(int(2e6)))

# %%
# %time euler_10(int(2e6))

# %% [markdown]
# ## 11. Largest Product in a Grid
#
# In the 20×20 grid below, four numbers along a diagonal line have been marked
# in red.
#
# <p><samp>
# 08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08<br />
# 49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00<br />
# 81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65<br />
# 52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91<br />
# 22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80<br />
# 24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50<br />
# 32 98 81 28 64 23 67 10 <strong>26</strong> 38 40 67 59 54 70 66 18 38 64 70<br />
# 67 26 20 68 02 62 12 20 95 <strong>63</strong> 94 39 63 08 40 91 66 49 94 21<br />
# 24 55 58 05 66 73 99 26 97 17 <strong>78</strong> 78 96 83 14 88 34 89 63 72<br />
# 21 36 23 09 75 00 76 44 20 45 35 <strong>14</strong> 00 61 33 97 34 31 33 95<br />
# 78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92<br />
# 16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57<br />
# 86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58<br />
# 19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40<br />
# 04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66<br />
# 88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69<br />
# 04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36<br />
# 20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16<br />
# 20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54<br />
# 01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48<br /></samp></p>
#
#
# The product of these numbers is **26×63×78×14 = 1788696**
#
# What is the greatest product of four adjacent numbers in the same direction
# (up, down, left, right, or diagonally) in the 20×20 grid?

# %%
grid = """08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08
49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00
81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65
52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91
22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80
24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50
32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70
67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21
24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72
21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95
78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92
16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57
86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58
19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40
04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66
88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69
04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36
20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16
20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54
01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48"""


# %%
# @print_and_copy_answer
def largest_product_grid(blocksize: int, grid: str = grid) -> int:
    np_grid = np.loadtxt(StringIO(grid))
    m, n = np_grid.shape

    arr = np.zeros((m + blocksize, n + 1), int)  # pad with the right amount of zeros.
    arr[:m, :n] = np_grid
    flat = arr.ravel()
    usefulsize = np_grid.size + m  # indice of last non zero value + 1

    shifts = [1, n, n + 1, n + 2]  # - / | \ , the four directions
    blocks = np.array(
        [[flat[i * s :][:usefulsize] for s in shifts] for i in range(blocksize)]
    )  # 15µs
    scores = blocks.prod(axis=0)  # 8µs

    return scores.max()


# %%
def largest_product_grid_dict_approach(numbers: int = 4, grid: str = grid) -> int:

    # first generate a dictionary with key = (row,col) and value = int(n)
    grid_dict: dict[tuple[int], int] = {
        (row, col): int(n)
        for row, r in enumerate(grid.split("\n"))
        for col, n in enumerate(r.split())
    }

    # then define a function that returns the max_product of the next <numbers>
    # adjacent numbers in any direction starting from (row, col)

    def prod_adjacent(row: int, col: int, numbers: int = numbers) -> int:
        max_prod = 0
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            prod = 1
            for i in range(numbers):
                prod *= grid_dict.get((row + dr * i, col + dc * i), 0)
            max_prod = max(max_prod, prod)
        return max_prod

    # generate for every position in the dictionary the max_prod and print the
    # max of this maxima

    return max(prod_adjacent(row, col) for row, col in grid_dict)


# %%
# %timeit largest_product_grid_dict_approach()

# %%
# %timeit largest_product_grid(4)

# %% [markdown]
# ## 12. Highly Divisible Triangular Number
#
# The sequence of triangle numbers is generated by adding the natural numbers.
# So the $7$<sup>th</sup> triangle number would be
# $1 + 2 + 3 + 4 + 5 + 6 + 7 = 28$. The first ten terms would be:
#
# $$1, 3, 6, 10, 15, 21, 28, 36, 45, 55, \dots$$
#
# Let us list the factors of the first seven triangle numbers:
#
# $$
# \begin{align}
# \mathbf 1 &\colon 1\\
# \mathbf 3 &\colon 1,3\\
# \mathbf 6 &\colon 1,2,3,6\\
# \mathbf{10} &\colon 1,2,5,10\\
# \mathbf{15} &\colon 1,3,5,15\\
# \mathbf{21} &\colon 1,3,7,21\\
# \mathbf{28} &\colon 1,2,4,7,14,28
# \end{align}
# $$
#
# We can see that $28$ is the first triangle number to have over five divisors.
#
# What is the value of the first triangle number to have over five hundred
# divisors?


# %%
def triangle_number(n: int) -> int:
    return n * (n + 1) / 2


def generate_divisors(n: int) -> list[int]:
    divisors = []
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            divisors.append(d)
            if (
                d != n // d
            ):  # Avoid adding the square root twice if n is a perfect square
                divisors.append(n // d)
    return divisors


@print_and_copy_answer
def highly_divisible_triangular_number(n_divisors: int = 500) -> int:
    triangle_index = 1
    triangle_number = 1  # First triangular number

    while True:
        # ic(triangle_number)
        divisors = generate_divisors(triangle_number)
        if len(divisors) >= n_divisors:
            return triangle_number

        # Move to the next triangular number
        triangle_index += 1
        triangle_number += (
            triangle_index  # Update triangular number by adding the next index
        )


# %% [markdown]
# ## 13. Large Sum
#
# Work out the first ten digits of the sum of the following one-hundred 50-digit
# numbers.

# %%
large_number = """37107287533902102798797998220837590246510135740250
46376937677490009712648124896970078050417018260538
74324986199524741059474233309513058123726617309629
91942213363574161572522430563301811072406154908250
23067588207539346171171980310421047513778063246676
89261670696623633820136378418383684178734361726757
28112879812849979408065481931592621691275889832738
44274228917432520321923589422876796487670272189318
47451445736001306439091167216856844588711603153276
70386486105843025439939619828917593665686757934951
62176457141856560629502157223196586755079324193331
64906352462741904929101432445813822663347944758178
92575867718337217661963751590579239728245598838407
58203565325359399008402633568948830189458628227828
80181199384826282014278194139940567587151170094390
35398664372827112653829987240784473053190104293586
86515506006295864861532075273371959191420517255829
71693888707715466499115593487603532921714970056938
54370070576826684624621495650076471787294438377604
53282654108756828443191190634694037855217779295145
36123272525000296071075082563815656710885258350721
45876576172410976447339110607218265236877223636045
17423706905851860660448207621209813287860733969412
81142660418086830619328460811191061556940512689692
51934325451728388641918047049293215058642563049483
62467221648435076201727918039944693004732956340691
15732444386908125794514089057706229429197107928209
55037687525678773091862540744969844508330393682126
18336384825330154686196124348767681297534375946515
80386287592878490201521685554828717201219257766954
78182833757993103614740356856449095527097864797581
16726320100436897842553539920931837441497806860984
48403098129077791799088218795327364475675590848030
87086987551392711854517078544161852424320693150332
59959406895756536782107074926966537676326235447210
69793950679652694742597709739166693763042633987085
41052684708299085211399427365734116182760315001271
65378607361501080857009149939512557028198746004375
35829035317434717326932123578154982629742552737307
94953759765105305946966067683156574377167401875275
88902802571733229619176668713819931811048770190271
25267680276078003013678680992525463401061632866526
36270218540497705585629946580636237993140746255962
24074486908231174977792365466257246923322810917141
91430288197103288597806669760892938638285025333403
34413065578016127815921815005561868836468420090470
23053081172816430487623791969842487255036638784583
11487696932154902810424020138335124462181441773470
63783299490636259666498587618221225225512486764533
67720186971698544312419572409913959008952310058822
95548255300263520781532296796249481641953868218774
76085327132285723110424803456124867697064507995236
37774242535411291684276865538926205024910326572967
23701913275725675285653248258265463092207058596522
29798860272258331913126375147341994889534765745501
18495701454879288984856827726077713721403798879715
38298203783031473527721580348144513491373226651381
34829543829199918180278916522431027392251122869539
40957953066405232632538044100059654939159879593635
29746152185502371307642255121183693803580388584903
41698116222072977186158236678424689157993532961922
62467957194401269043877107275048102390895523597457
23189706772547915061505504953922979530901129967519
86188088225875314529584099251203829009407770775672
11306739708304724483816533873502340845647058077308
82959174767140363198008187129011875491310547126581
97623331044818386269515456334926366572897563400500
42846280183517070527831839425882145521227251250327
55121603546981200581762165212827652751691296897789
32238195734329339946437501907836945765883352399886
75506164965184775180738168837861091527357929701337
62177842752192623401942399639168044983993173312731
32924185707147349566916674687634660915035914677504
99518671430235219628894890102423325116913619626622
73267460800591547471830798392868535206946944540724
76841822524674417161514036427982273348055556214818
97142617910342598647204516893989422179826088076852
87783646182799346313767754307809363333018982642090
10848802521674670883215120185883543223812876952786
71329612474782464538636993009049310363619763878039
62184073572399794223406235393808339651327408011116
66627891981488087797941876876144230030984490851411
60661826293682836764744779239180335110989069790714
85786944089552990653640447425576083659976645795096
66024396409905389607120198219976047599490197230297
64913982680032973156037120041377903785566085089252
16730939319872750275468906903707539413042652315011
94809377245048795150954100921645863754710598436791
78639167021187492431995700641917969777599028300699
15368713711936614952811305876380278410754449733078
40789923115535562561142322423255033685442488917353
44889911501440648020369068063960672322193204149535
41503128880339536053299340368006977710650566631954
81234880673210146739058568557934581403627822703280
82616570773948327592232845941706525094512325230608
22918802058777319719839450180888072429661980811197
77158542502016545090413245809786882778948721859617
72107838435069186155435662884062257473692284509516
20849603980134001723930671666823555245252804609722
53503534226472524250874054075591789781264330331690"""


# %%
@print_and_copy_answer
def large_sum_first_digits(large_num: str = large_number) -> str:
    return f"{sum(map(int, large_num.splitlines()))}"[:10]


large_sum_first_digits()

# %% [markdown]
# ## 14. Longest Collatz Sequence
#
# The following iterative sequence is defined for the set of positive integers:
#
# * **n → n/2** (**n** is even)
# * **n → 3n + 1** (**n** is odd)
#
#
# Using the rule above and starting with **13**, we generate the following
# sequence:
#
# **13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1.**
#
# It can be seen that this sequence (starting at **13** and finishing at **1**)
# contains **10** terms. Although it has not been proved yet (Collatz Problem),
# it is thought that all starting numbers finish at **1**.
#
# Which starting number, under one million, produces the longest chain?
#
# **NOTE:** Once the chain starts the terms are allowed to go above one million.


# %%
@cache
def collatz_sequence(n: int) -> int:
    if n == 1:
        return 1
    if n % 2 == 0:
        return 1 + collatz_sequence(n // 2)
    return 1 + collatz_sequence(3 * n + 1)


@print_and_copy_answer
def longest_collatz_sequence(limit: int) -> int:
    return max(range(2, int(limit)), key=collatz_sequence)


longest_collatz_sequence(1e6)


# %% [markdown]
# ## 15. Lattice Paths
#
# Starting in the top left corner of a **2×2** grid, and only being able to move
# to the right and down, there are exactly **6** routes to the bottom right
# corner.
#
# <img src="https://projecteuler.net/resources/images/0015.png?1678992052" style="background-color:white;" />
#
# How many such routes are there through a **20×20** grid?


# %%
@print_and_copy_answer
def lattice_paths(grid_size: int) -> int:
    """
    The number of lattice paths from
    .. math:: (0,0) \\to (n,k) = \\binom{n+k}{n}
    """
    return comb(grid_size + grid_size, grid_size)


# %%
assert lattice_paths(2) == 6
lattice_paths(20)


# %% [markdown]
# ## 16. Power Digit Sum
#
# $2^{15} = 32768$ and the sum of its digits is $3 + 2 + 7 + 6 + 8 = 26$
#
# What is the sum of the digits of the number $2^{1000}$?


# %%
@print_and_copy_answer
def power_digit_sum(digit: int, power: int) -> int:
    return sum(map(int, f"{digit ** power}"))


# %%
assert power_digit_sum(2, 15) == 26
power_digit_sum(2, 1000)


# %% [markdown]
# ## 17. Number Letter Counts
#
# If the numbers **1** to **5** are written out in words: one, two, three, four,
# five, then there are **3 + 3 + 5 + 4 + 4 = 19** letters used in total.
#
# If all the numbers from **1** to **1000** (one thousand) inclusive were
# written out in words, how many letters would be used?
#
# NOTE: Do not count spaces or hyphens. For example, **342** (three hundred and
# forty-two) contains **23** letters and **115** (one hundred and fifteen)
# contains **20** letters. The use of "and" when writing out numbers is in
# compliance with British usage.


# %%
@cache
def number_to_words(n):
    if not (1 <= n <= 1000):
        return "Number out of range"

    # Words for basic numbers
    ones = [
        "",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
    ]
    tens = [
        "",
        "",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety",
    ]

    if n == 1000:
        return "one thousand"
        # return 2

    result = ""

    # Handle hundreds
    if n >= 100:
        result += ones[n // 100] + " hundred"
        n %= 100
        if n > 0:
            result += " and "

    # Handle tens and ones
    if n >= 20:
        result += tens[n // 10]
        n %= 10
        if n > 0:
            result += " " + ones[n]
    elif n > 0:
        result += ones[n]

    return result


# %%
assert len(number_to_words(342).replace(" ", "")) == 23
assert len(number_to_words(115).replace(" ", "")) == 20


# %%
@print_and_copy_answer
def number_letter_counts(limit: int) -> int:
    return sum(len(number_to_words(i).replace(" ", "")) for i in range(1, limit + 1))


# %%
assert number_letter_counts(5) == 19
number_letter_counts(1000)

# %% [markdown]
# ## 19. Maximum Path Sum I
#
# By starting at the top of the triangle below and moving to adjacent numbers on
# the row below, the maximum total from top to bottom is **23**.
#
#
# <div align="center"><samp>
# <b>3</b><br>
# <b>7</b> 4<br>
# 2 <b>4</b> 6<br>
# 8 5 <b>9</b> 3</samp>
# </div>
#
# That is, **3 + 7 + 4 + 9 = 23**.
#
# Find the maximum total from top to bottom of the triangle below:
#
# <div align="center"><samp>
# 75<br>
# 95 64<br>
# 17 47 82<br>
# 18 35 87 10<br>
# 20 04 82 47 65<br>
# 19 01 23 75 03 34<br>
# 88 02 77 73 07 63 67<br>
# 99 65 04 28 06 16 70 92<br>
# 41 41 26 56 83 40 80 70 33<br>
# 41 48 72 33 47 32 37 16 94 29<br>
# 53 71 44 65 25 43 91 52 97 51 14<br>
# 70 11 33 28 77 73 17 78 39 68 17 57<br>
# 91 71 52 38 17 14 91 43 58 50 27 29 48<br>
# 63 66 04 68 89 53 67 30 73 16 69 87 40 31<br>
# 04 62 98 27 23 09 70 98 73 93 38 53 60 04 23</p>
# </samp></div>
#
# **NOTE:** As there are only **16384** routes, it is possible to solve this
# problem by trying every route. However, [Problem
# 67](https://projecteuler.net/problem=67), is the same challenge with a
# triangle containing one-hundred rows; it cannot be solved by brute force, and
# requires a clever method! ;o)

# %%
test_triangle = """3
7 4
2 4 6
8 5 9 3"""

triangle = """75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23"""


def triangle_to_array(triangle_str: str) -> list[list[int]]:
    return [[int(num) for num in row.split()] for row in triangle_str.splitlines()]


def max_sum(row: list[int], next_row: list[int]) -> list[int]:
    a = [x[0] + x[1] for x in zip(row, next_row)]
    b = [x[0] + x[1] for x in zip(row[1:], next_row)]
    return [max(x) for x in zip(a, b)]


@print_and_copy_answer
def solution(triangle_str: str) -> int:
    triangle_array = triangle_to_array(triangle_str)
    return reduce(max_sum, triangle_array[::-1])[0]


solution(triangle)

# %% [markdown]
# ## 19. Counting Sundays
#
# You are given the following information, but you may prefer to do some
# research for yourself.
#
# * 1 Jan 1900 was a Monday.
# * Thirty days has September,<br>
#   April, June and November.<br>
#   All the rest have thirty-one, Saving February alone,<br>
#   Which has twenty-eight, rain or shine.<br>
#   And on leap years, twenty-nine.<br>
# * A leap year occurs on any year evenly divisible by 4, but not on a century
#   unless it is divisible by 400.
#
# How many Sundays fell on the first of the month during the twentieth century
# (1 Jan 1901 to 31 Dec 2000)?

# %%
nums, _ = (
    pd.DataFrame(index=pd.date_range("1/1/1901", "12/31/2000", freq="W-SUN"))
    .loc[lambda d: d.index.day == 1]
    .shape
)


@print_and_copy_answer
def count_weekday_date_range(
    lower_limit_year: int = 1901,
    upper_limit_year: int = 2000,
    weekday: int = 6,
    calendar_day: int = 1,
) -> int:
    """
    Return count of days given the following:

    Parameters
    ----------
    lower_limit_year : int, optional
        by default 1901
    upper_limit_year : int, optional
        by default 2000
    weekday : int, optional
        day of the week as an integer, where Monday is 0 and Sunday is 6.
        by default 6 (Sunday)
    calendar_day : int, optional
        by default 1

    Returns
    -------
    int
    """
    return sum(
        date(year, month, calendar_day).weekday() == weekday
        for year in range(lower_limit_year, upper_limit_year + 1)
        for month in range(1, 12 + 1)
    )


count_weekday_date_range()

# %% [markdown]
# ## 20. Factorial Digit Sum
#
# **n!** means **n × (n - 1) × ⋯ × 3 × 2 × 1**.
#
# For example, **10! = 10 × 9 × ⋯ × 3 × 2 × 1 = 3628800**, and the sum of the
# digits in the number **10!** is **3 + 6 + 2 + 8 + 8 + 0 + 0 = 27**.
#
# Find the sum of the digits in the number **100!**.


# %%
@cache
def factorial(num: int):
    result = 1
    if num == 0 or num == 1:
        return result
    for i in range(1, num + 1):
        result *= i
    return result


@print_and_copy_answer
def factorial_digit_sum(number: int) -> int:
    return sum(map(int, f"{factorial(number)}"))


factorial_digit_sum(100)