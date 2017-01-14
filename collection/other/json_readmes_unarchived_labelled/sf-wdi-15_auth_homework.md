# Auth HW

## Description

Use the `auth_examples` repo and the `passport-2` branch to reimplement a basic passport authentication scheme.

## Getting started

You'll be working from scratch today. It will be as much of a copy and paste assignment as you want it to be. However, this is your opportunity to form questions for tomorrows review and explanation of todays materials.

* fork and clone this repo
* then do the following just get the right packages installed

```
npm init

```

```
npm install --save express ejs body-parser
npm install --save pg sequelize
npm install --save cookie-session passport passport-local
```

> NOTE: Here we are installing `cookie-session` to start sessions on our application using cookies sent from the browser. The `passport` module is for passports general authentication library tools. The `passport-local` tool is for authenticating a user based on a `username` and `password`. Passport local differs from passport  in that passport can be used for many strategies for logging someone in. 
