C++ Smart pointers
==================

# unique_ptr
- owns a object
- dispose of the owned object when goes out-of-scope
- Create using: ```auto p = std::make_unique<Shape>();```
- Transfer ownership using ```auto q = std::move(p);```
- Follows runtime polymorphism ```std::unique_ptr<Base> p = std::make_unique<Derived>();```
- custom lambda-expression deleter ```std::unique_ptr<D, void(*)(D*)> p(new D, [](D * dp) { delete dp; } );```
- Arrays of it, ```std::unique_ptr<A[]> p(new A[5]);``` This will create 5 elements, and when p goes out of scope it will call destructor for all 5 elements.


# shared_ptr
- multiple shared_ptr can have shared ownership an object ```auto p = std::make_shared<U>();```
- object is destroyed when the last remaining shared_ptr is destroyed
- a reference count is maintained. With every extra share count is increased, and with every release of the ownership the counter is decreased.

# weak_ptr
- non-owning reference to an object which is managed by shared_ptr. The weak_ptr must be converted to 'shared_ptr' before accessing the object - using 'lock' function' ```std::weak_ptr<U> wp; std::shared_ptr<U> sp = std::make_shared<U>(); wp = sp; if( auto sp2 = wp.lock()) { use with sp2 } else { wp is expired }```
- use function 'use_count()' to check the count.