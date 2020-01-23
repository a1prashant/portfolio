# C++ cast

1. static_cast
- when implicit casting is possible
    > ```int x = static_cast<int>(3.14);```
- when convertors are available
    > ```Box b = static_cast<Box>("10,20,30");```
- related down-cast or up-cast
    > ```Base * bp = static_cast<Base*>(new Derived());```
- inverse of implicit conversion
    > ```int * np = static_cast< int* >( void_ptr_x );```
- enum to int
    > ```int one = static_cast<int>( ENUM_NUMBERS );```
- int to enum
    > ```ENUM_NUMBER n = static_cast<ENUM_NUMBERS>( one );```
- enum to another enum
    > ```ARABIC_NUMBERS an = static_cast< ARABIC_NUMBERS >( enumbers );```

2. dynamic_cast
- only on pointers or references
- for polymorphic types
- specially used for downcast
    > ```Derived *pd = dynamic_cast< Derived* >( basePtr );```
- does run-time check if down-cast succeeds
    > ```if( Derived * pd = dynamic_cast < Derived* >( basePtr ) ) { /// success, can use pd }```
- can be used to add 'const'ness

3. const_cast
- cast away the constness or volatility
```
    int h = 10;
    const int &o = h;
    const_cast<int &>(o) = 20;
```
 - works on pointers and references only
- destination-type also has to be of same type
- BUT, if the value itself is 'const' then result is undefined
```
    const int ci = 4;
    int * pi = const_cast< int* >( &ci );
    // cannot use pi to modify value, undefined behavior
```

4. reinterpret_cast
- only for pointers and references
- from any type to any other type of pointer
- reinterprets types from the bit pattern
    > ```int i = 10; char* p = reinterpret_cast< char* >( i );```

