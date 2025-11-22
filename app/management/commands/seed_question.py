from django.core.management.base import BaseCommand
from app.models import Question
import random

# Each tuple: (text, option_a, option_b, option_c, option_d, correct)
SAMPLE_QUESTIONS = {

    # ------------------------- APTITUDE -------------------------
    'aptitude': [
        ("If x and y are positive integers with lcm(x,y)=840 and gcd(x,y)=14, and x<y, what is x?", "20", "28", "42", "60", 'c'),
        ("A and B can do a job in 12 and 15 days respectively. If they work alternately starting with A, how many days to finish?", "8", "9", "10", "11", 'b'),
        ("If 3^a = 81 and 2^b = 64, what is a/b?", "1", "4/3", "3/2", "5/4", 'c'),
        ("A box contains 6 red, 5 blue and 4 green balls. If two balls picked at random, probability both are red?", "1/3", "1/11", "5/21", "1/15", 'c'),
        ("Solve for n: n! is divisible by 1000 but (n-1)! is not. Minimum n = ?", "10", "11", "12", "8", 'b'),
        ("If arithmetic progression has 5th term 20 and 12th term 47, find first term.", "-1", "2", "-3", "5", 'a'),
        ("If the roots of x^2 - sx + p = 0 are reciprocals, what is relationship between s and p?", "s=p", "s^2=4p", "p=1", "s=0", 'c'),
        ("A and B invest in ratio 3:5. Profit after 1 year is 1600. A's share?", "600", "800", "480", "720", 'a'),
        ("If log_2(x) + log_2(x-2)=3, x = ?", "4", "5", "6", "8", 'b'),
        ("A train 150m long crosses a platform in 30s at speed v. It crosses another train 200m long moving opposite in 10s. Find v in m/s.", "15", "20", "25", "30", 'b'),
        ("If (x-1)(x-2)(x-3)=x, sum of possible x?", "6", "5", "4", "7", 'b'),
        ("In a triangle, sides are in GP with ratio r, r^2, r^3 and perimeter 60, and smallest side 6. r=?", "2", "3", "4", "1.5", 'a'),
        ("A mixture of 30L is 20% alcohol. How much pure alcohol to add to make 40%?", "6L", "8L", "10L", "12L", 'b'),
        ("If S = 1 + 1/2 + 1/3 + ... + 1/50, which is greater: S or ln 50 + 1?", "S > ln50+1", "S < ln50+1", "S = ln50+1", "Cannot determine", 'b'),
        ("If two numbers are in ratio 4:9 and their HCF is 7, numbers are?", "28 and 63", "14 and 31.5", "28 and 63 only", "Cannot be integers", 'a'),
        ("If a fair die rolled 6 times, probability of exactly two sixes?", "(6 choose2)*(1/6)^2*(5/6)^4", "1/6", "(1/6)^2", "(6 choose2)/6^6", 'a'),
        ("Sum of first 20 odd numbers is?", "400", "380", "420", "440", 'a'),
        ("If harmonic mean of 6 and x is 8, find x.", "12", "9", "16", "24", 'c'),
        ("Numbers 1..9 placed; number of 3-digit numbers divisible by 5 and digits distinct?", "72", "108", "36", "24", 'a'),
        ("If probability an event happens on a day is 0.2 independently for 5 days, probability it never happens?", "0.8^5", "0.2^5", "(1-0.2)/5", "0.5", 'a'),
        ("If x^2 + y^2 = 50 and xy = 21, find (x+y)^2.", "100", "92", "82", "110", 'b'),
        ("If sequence defined by a_{n+1}=3a_n -2 and a_1=2, find a_4.", "80", "50", "40", "62", 'c'),
        ("Two pipes A and B fill a tank in 6 and 8 hours. A open 2 hrs then B alone finishes in 3 hrs more. Fraction of tank filled by A?", "1/2", "1/3", "2/5", "3/5", 'a'),
        ("If population grows 10% annually, approximate doubling time?", "7 years", "10 years", "5 years", "8 years", 'a'),
        ("If 5x ≡ 1 (mod 26), x = ?", "21", "21", "21", "21", 'a')
    ],

    # ------------------------- REASONING -------------------------
    'reasoning': [
        ("Find next in series: 2, 3, 5, 9, 17, ?", "31", "33", "35", "29", 'b'),
        ("If in a code, CAT->XZG, DOG->WLJ, then BAT->?", "YXF", "YWE", "YVG", "YXF", 'd'),
        ("Clock angle: At 3:15, angle between hands?", "7.5 degrees", "0 degrees", "15 degrees", "97.5 degrees", 'a'),
        ("A cube painted on all faces then cut into 27 small cubes; number with exactly one painted face?", "6", "12", "8", "0", 'b'),
        ("If statements: P->Q true; Q false. Which must be false?", "P", "Q", "Both", "Neither", 'a'),
        ("From statements: All A are B. Some B are C. Which true?", "Some A are C", "All A are C", "Cannot conclude", "No relation", 'c'),
        ("Which shape will come next in pattern: square, triangle, pentagon, ?", "hexagon", "circle", "octagon", "heptagon", 'a'),
        ("Word analogy: Finger is to Hand as Leaf is to ?", "Tree", "Branch", "Twig", "Stem", 'a'),
        ("If every third person is selected from 60, how many selected?", "20", "19", "21", "18", 'a'),
        ("If five statements, exactly two true, which combinations possible?", "Multiple", "None", "Unique", "Cannot determine", 'a'),
        ("River crossing minimal trips for 4 people?", "7 trips", "9 trips", "5 trips", "11 trips", 'a'),
        ("Distinct permutations of 'MISSISSIPPI'?", "34650", "83160", "13860", "27720", 'c'),
        ("Which digit replaces ? in 123?357 for divisibility by 3?", "6", "3", "9", "0", 'a'),
        ("Two weights balance three weights; inference?", "inequalities", "equalities", "cannot tell", "proportions", 'a'),
        ("Find odd one out: 2,3,5,7,11,12", "12", "11", "7", "5", 'a'),
        ("If someone says 'I always lie', truth value?", "Impossible", "True", "False", "Both", 'a'),
        ("Area ↑20% width same => length ↑?", "20%", "16.67%", "18%", "Not enough info", 'b'),
        ("Magic square missing number puzzle", "varies", "see explanation", "cannot determine", "unique", 'd'),
        ("Identify bulbs with 3 switches 1 visit?", "Turn on 1&2 wait, off 2", "Impossible", "Turn on 1", "Random", 'a'),
        ("Two trains meet; ratio distances?", "use speed ratio", "cannot determine", "equal", "none", 'a'),
        ("Transform ABC→A'B'C'?", "rotation 90°", "reflection", "translation", "scaling", 'a'),
        ("6 people handshake count?", "15", "12", "18", "20", 'a'),
        ("Next number: 1,1,2,3,5,8,?", "13", "12", "10", "15", 'a'),
        ("Least composite divisible by 2,3,5?", "30", "60", "90", "120", 'a')
    ],

    # ------------------------- JAVA -------------------------
    'java': [
        ("What is output of: int x=5; System.out.println(x++ + ++x);", "11", "12", "10", "13", 'd'),
        ("Which collection is synchronized by default in Java?", "ArrayList", "Vector", "HashMap", "LinkedList", 'b'),
        ("What is result of: Integer a = 127; Integer b = 127; a==b?", "true", "false", "compile error", "depends", 'a'),
        ("What does volatile keyword guarantee?", "Atomicity", "Visibility", "Ordering and visibility", "None", 'b'),
        ("Which exception thrown by Integer.parseInt(\"9999999999\")?", "NumberFormatException", "NullPointerException", "ClassCastException", "ArithmeticException", 'a'),
        ("What prints: System.out.println(\"Hello\\nWorld\".split(\"\\\\n\").length);", "2", "1", "0", "Error", 'a'),
        ("Given: List<String> l = Arrays.asList(\"a\",\"b\"); l.add(\"c\"); what happens?", "Adds c", "UnsupportedOperationException", "Compile error", "Runtime null", 'b'),
        ("What is output: System.out.println(Objects.equals(null,null));", "true", "false", "NullPointerException", "compile error", 'a'),
        ("Which is functional interface?", "Comparator", "Runnable", "ActionListener", "All of above", 'd'),
        ("What is output of: System.out.println(5/2);", "2", "2.5", "3", "Compile error", 'a'),
        ("What happens when Thread.run() is called directly?", "Runs in same thread", "New thread created", "Compile error", "Throws exception", 'a'),
        ("Which keyword prevents method overriding?", "static", "final", "private", "volatile", 'b'),
        ("What does 'transient' do?", "Prevents serialization", "Makes it final", "Ensures thread safety", "None", 'a'),
        ("Which map allows null keys?", "HashMap", "TreeMap", "Hashtable", "ConcurrentHashMap", 'a'),
        ("What prints: \"abc\".charAt(3)?", "Throws StringIndexOutOfBoundsException", "Prints null", "Prints empty", "Prints space", 'a'),
        ("Output: int[] a={1,2}; System.out.println(a instanceof Object);", "true", "false", "Compile error", "Runtime error", 'a'),
        ("Which is unchecked exception?", "IOException", "SQLException", "NullPointerException", "InterruptedException", 'c'),
        ("For Java String s=null; s.equals(\"x\"); what happens?", "NullPointerException", "false", "true", "compile error", 'a'),
        ("Result of bitwise: 5 & 3 ?", "1", "7", "8", "0", 'a'),
        ("Which method sorts list?", "Collections.sort(list)", "List.sort()", "Arrays.sort()", "Collections.order()", 'a'),
        ("Keyword for constant?", "final", "const", "static", "immutable", 'a'),
        ("Which JVM memory stores class info?", "Heap", "Stack", "Method Area", "PC Register", 'c'),
        ("Output: Math.round(2.5)?", "3", "2", "2.0", "Error", 'a'),
        ("Default methods introduced in?", "Serializable", "Comparable", "Runnable", "Interfaces (Java 8)", 'd'),
        ("Output: String s = \"a\"+1+2;", "a12", "3a", "a3", "Error", 'a')
    ],

    # ------------------------- PYTHON -------------------------
    'python': [
        ("What is output: print([i for i in range(5) if i%2==0])", "[0,2,4]", "[1,3]", "[0,1,2,3,4]", "[2,4]", 'a'),
        ("Output of: x = [1,2]; print(x*2)", "[1,2,1,2]", "[2,4]", "[1,2]*2", "Error", 'a'),
        ("What does list.sort() return?", "None", "Sorted list", "Iterator", "New list", 'a'),
        ("Output: print(''.join(sorted('cba')))", "abc", "cba", "bac", "Error", 'a'),
        ("Output: print(0.1 + 0.2 == 0.3)", "False", "True", "Error", "Depends", 'a'),
        ("Output: d = {'a':1}; print(d.get('b',0))", "0", "None", "KeyError", "\"\"", 'a'),
        ("Output: print((lambda x: x*x)(3))", "9", "3", "None", "Error", 'a'),
        ("Output: print(type(lambda:0))", "<class 'function'>", "<class 'lambda'>", "<class 'object'>", "Error", 'a'),
        ("Result: bool('False')", "True", "False", "Error", "None", 'a'),
        ("What does 'is' compare?", "Identity", "Equality", "Type only", "Both", 'a'),
        ("Output: a=[1]; b=a; b.append(2); print(a)", "[1,2]", "[1]", "[2]", "Error", 'a'),
        ("Output: print({i:i*i for i in range(3)})", "{0:0,1:1,2:4}", "{0:0,1:1,2:4}", "{0:0,1:1,2:4}", "Error", 'a'),
        ("Output: print(''.join([str(i) for i in range(3)]))", "012", "123", "['0','1','2']", "None", 'a'),
        ("What does *args do?", "Collects positional args", "Collects keyword args", "Unpacks dict", "None", 'a'),
        ("Output: print((1,2)+(3,))", "(1,2,3)", "(1,2)(3)", "[1,2,3]", "Error", 'a'),
        ("Access missing key d['x']?", "KeyError", "IndexError", "TypeError", "None", 'a'),
        ("Output: print(sum([0.1]*3))", "0.30000000000000004", "0.3", "0.3000", "Error", 'a'),
        ("Output: print(list(map(lambda x:x+1, [1,2,3])))", "[2,3,4]", "[1,2,3]", "[1,3,5]", "Error", 'a'),
        ("Iterator over dict keys?", "iter(d)", "keys(d)", "items(d)", "values(d)", 'a'),
        ("Output: print('abc'[::-1])", "cba", "abc", "Error", "None", 'a'),
        ("Effect of 'nonlocal'?", "Bind outer var", "Declare global", "Create new var", "Error", 'a'),
        ("Output: print({1,2,2,3})", "{1,2,3}", "{1,2,2,3}", "[1,2,3]", "Error", 'a'),
        ("Output: type((x for x in range(3)))", "<class 'generator'>", "<class 'list'>", "<class 'tuple'>", "Error", 'a'),
        ("Output: print([i for i in range(10) if i%3==0])", "[0,3,6,9]", "[3,6,9]", "[0,1,2,3]", "[0,3,6]", 'a'),
    ],
}

class Command(BaseCommand):
    help = "Seed 25 questions per category (total 100) with advanced-level content"

    def handle(self, *args, **options):
        Question.objects.all().delete()
        per_cat = 25
        for cat, samples in SAMPLE_QUESTIONS.items():
            i = 0
            while i < per_cat:
                question = samples[i % len(samples)]
                Question.objects.create(
                    text=question[0],
                    category=cat,
                    option_a=question[1],
                    option_b=question[2],
                    option_c=question[3],
                    option_d=question[4],
                    correct_option=question[5]
                )
                i += 1

        self.stdout.write(self.style.SUCCESS("Seeded 100 questions (25 per category)."))
