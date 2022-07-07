def fibonacci(n):
   """function to display a list of the 
      Fibonacci sequence up to n-th term

   Args:
       n (int): n-th term of sequence

   Returns:
       list: a list of the 
      Fibonacci sequence up to n-th term
   """
   # first two terms
   n1, n2 = 0, 1
   # empty list to keep the terms in
   terms_list = list()
   
   # check if the number of terms is valid
   if n <= 0:
      return "Please enter a positive integer"
   
   # generate fibonacci sequence
   else:
      print(f"Fibonacci sequence upto {n} terms:")
      for i in range(n):
         terms_list.append(n1)
         nth = n1 + n2
         # update values
         n1 = n2
         n2 = nth
   return terms_list
   
if __name__ == "__main__":
   n = int(input("How many terms? "))
   print(fibonacci(n))