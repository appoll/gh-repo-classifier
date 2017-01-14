
# data

  attach data to elements. think $.data().

## Installation

    $ component install yields/data

## API

### api = data(el)

Get new data api for the given element.

### api.set(key[, val])

Merge the provided `obj` or set
`key` to `val`.

```javascript
data(el).set({ foo: 'bar' })
data(el).set({ bar: 'foo' });
data(el).get();
// > { foo: 'bar', bar: 'foo' }
```

### api.get([key])

Get all data or a single value by `key`,
if the `key` does not exists it will be looked-up
in the element `data-*` attributes, when found
it will be cached and then returned.

```javascript
data(el).get('foo');
// > null
data(el).get();
// > {}
```

### api.has(key)

Whether or not `key` exists

```
data(el).set('foo', 'bar').has('foo');
// > true
```

### api.del([key])

Delete all data or a single `key` from cache.

```javascript
data(el).del('some key');
data(el).del(); // everything!
```

### api.cache

the element cache

### api.el

the element.

### add custom methods.

```javascript
data.api.getUserAge = function () {
  return this.cache.user
    && this.cache.user.age;
};

data(el).set({ user: { age: 99 } }).getUserAge();
// > 99
```


## License

  MIT
