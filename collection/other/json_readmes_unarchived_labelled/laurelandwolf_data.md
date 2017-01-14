# data

Laurel & Wolf Data

![Data](https://cloud.githubusercontent.com/assets/974723/10259350/ded875a8-691b-11e5-8d71-39b0db46c117.gif)

## Install

```
npm install lw-data --save
```

## Usage

**HTTP**

```js
import {sdk, serialize} from 'lw-data'

let api = sdk({
  headers: {
    custom : 'header'
  }
})

api()
  .projects()
  .get()
  .then(res => {

    let resources = serialize.response(res.body);
    console.log(resources);
  })
```

**Streaming**

```js
import {sdk} from 'lw-data'

let api = sdk({
  headers: {
    custom : 'header'
  }
})

api.createStream(({headers}) => {

	// return observable
})

api()
  .projects()
  .stream('created')
  .subscribe(res => {


  })

api.createStream(({headers}) => {

	// return observable
})

api()
  .submissions()
  .stream()
  .subscribe(res => {


  })
```
