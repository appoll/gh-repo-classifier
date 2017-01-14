This app is a showcase of Github projects for an organization or a user, all in Javascript.

It uses [AuraJS](https://github.com/aurajs/aura) and an [aura-github](https://github.com/hull/hull.github.io/blob/master/assets/js/extensions/aura-github.js) extension that allows our Widgets to talk directly to Github's API, and [2 Aura widgets](https://github.com/hull/hull.github.io/tree/master/widgets) : 

* [user](https://github.com/hull/hull.github.io/blob/master/widgets/user/main.js) to load and display a user's profile. (In our case, [hull's organization](https://github.com/hull))
* [repos](https://github.com/hull/hull.github.io/blob/master/widgets/repos/main.js) to load and display a list of repos.

If you want to know more how it was done, read [the blog post](http://blog.hull.io/post/46504817377/how-to-build-your-own-twitter-like-open-source-page).

## Using on your own github homepage

1. First, clone this repository (or fork it directly on Github) :

        git clone git://github.com/hull/hull.github.io.git

2. Create a repository named ``you.github.io``, where ``you`` is your username (If you have fork the repository, don't forget to rename it!)

3. Whitelist your domain on your github applications settings [https://github.com/settings/applications](https://github.com/settings/applications)

   Click on **Register a new application**
   
   Fill **Main URL** and **Callback URL** with your github homepage url. (i.e. ``http://you.github.io``)

4. Configure ```index.html``` with the correct settings.

   If you are an organization:

        <header data-aura-widget="user" data-aura-org="hull"></header> 
        <ul data-aura-widget="repos" data-aura-org="hull"></ul>
    
    else you are a simple user:

        <header data-aura-widget="user" data-aura-user="victa"></header> 
        <ul data-aura-widget="repos" data-aura-user="victa"></ul>

5. ``git push`` to your github page repository and you’re done!


[More about github pages](https://github.com/blog/272-github-pages)


## Using locally

Install [node.js](http://nodejs.org) **(Only used for developing the app locally, not needed for deployment)**

Install [grunt-cli](https://github.com/gruntjs/grunt-cli) as a global module.

    [sudo] npm install grunt-cli -g


then install grunt and it's modules in the project's folder.

    cd hull.github.io
    npm install


### Running the app

Start grunt

    grunt

Open in your browser

    open http://localhost:3010

## Options

### User widget

* `style`: Optional, could be **small** or **complete** depending on what do you want to show.

##### Example:

    <ul data-aura-widget="repos" data-aura-style="complete" data-aura-user="victa"></ul>
        
## Next steps

Here are a few ideas for further improvement :

* Add statistics widgets
* Add more details about an user, an organization, a repository…
* ...

Feel free to fork the project and add your own widget.
