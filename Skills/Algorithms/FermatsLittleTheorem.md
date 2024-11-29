
# Uses
When a does not divide P
Helps us find the Modular Multiplicative Inverse.
$$P^{a-2}= P^{-1} $$
where $P^{-1}$ is the <span style="color:rgb(0, 176, 80)">MMI(Modular Multiplicative Inverse)</span> of P.

# [<span style="color:rgb(255, 0, 0)">Concept</span>](https://www.youtube.com/watch?v=XPMzosLWGHo)

For a prime number P when 'a' type of different entities are fixed into P positions, the number $a^P - a$ is divisible by P.

Using that we can say that $a^P$ mod P is equal to a, and so $a^{P-1}$ mod P is 1 and hence

$a^{P-2}=a^{-1}$ where $a^{-1}$ is the MMI of a.


### <span style="color:rgb(0, 176, 240)">NOTE  </span> 
Use binary exponentiation instead of normal exponentiation since normal exponentiation is lossy because of overflowing of data types and takes O(n) time where as binary exp. takes O(logb(n)) time.

## <span style="color:rgb(0, 176, 80)">Code</span> 
```c++
long long binexp(long long a, long long b, long long m = MOD){
    long long ans = 1;
    while(b){
        if(b&1){
            ans = (ans%m * 1LL * a%m)%m;
        }
        a = (a%m * 1LL * a%m)%m;
        b = b >> 1;
    }
    return ans;
}

int main () {
    cout << binexp(a, MOD - 2) << endl;
}

// MOD = 1e9 + 7 for values under 10^9 and 10^18 + 3 for values under 10^18
```
